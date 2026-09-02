"""
修复 GMM 概率分布过于尖锐的问题:
1. 给协方差加最小方差 floor(防止塌缩)
2. 温度缩放软化 predict_proba
3. 重新生成 prototype_assignment.parquet
4. 重新生成 country_culture_dist.csv
"""
import os, sys, json, pickle, numpy as np, pandas as pd
sys.stdout.reconfigure(line_buffering=True)

BASE = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集'
RES = os.path.join(BASE, 'result')

# === 1. 加载 GMM,修复协方差 ===
print('[Fix] 加载 GMM 模型...')
with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
    bundle = pickle.load(f)

gmm = bundle['gmm']
scaler = bundle['scaler']
feat_cols = bundle['feat_cols']
prototypes = bundle['prototypes']
n_proto = gmm.n_components

# 给每个原型的 diag 方差加 floor
MIN_VAR = 0.05  # 最小方差
for i in range(n_proto):
    gmm.covariances_[i] = np.maximum(gmm.covariances_[i], MIN_VAR)

# 重新计算 cholesky 分解(因为 cov 变了)
gmm.precisions_cholesky_ = np.array([
    np.linalg.cholesky(np.diag(1.0 / gmm.covariances_[i]))
    for i in range(n_proto)
])
print(f'  协方差 floor={MIN_VAR} 已应用')

# === 2. 加载特征,重新计算软分配 ===
print('[Fix] 加载特征...')
feat_df = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
meta_cols = ['B_COUNTRY_ALPHA', 'A_YEAR', 'W_WEIGHT', 'S018']

print('[Fix] 重新计算软分配(温度缩放 T=3.0)...')
X = feat_df[feat_cols].values.astype(float)
X_scaled = scaler.transform(X)

# 手动计算 GMM 对数概率 + 温度缩放
# log p(x|k) = -0.5 * sum(log(2*pi*var)) - 0.5 * sum((x-mean)^2 / var)
TEMPERATURE = 3.0
n = X_scaled.shape[0]
log_probs = np.zeros((n, n_proto))
for k in range(n_proto):
    diff = X_scaled - gmm.means_[k]  # (n, d)
    log_det = np.sum(np.log(2 * np.pi * gmm.covariances_[k]))
    mahal = np.sum(diff ** 2 / gmm.covariances_[k], axis=1)
    log_probs[:, k] = -0.5 * (log_det + mahal) + np.log(gmm.weights_[k])

# 温度缩放
log_probs = log_probs / TEMPERATURE
log_probs -= log_probs.max(axis=1, keepdims=True)
exp_probs = np.exp(log_probs)
probs = exp_probs / exp_probs.sum(axis=1, keepdims=True)

labels = probs.argmax(axis=1)

# === 3. 检查日本 ===
jpn_mask = feat_df['B_COUNTRY_ALPHA'] == 'JPN'
jpn_probs = probs[jpn_mask]
print(f'\n  日本样本软分配 (T={TEMPERATURE}):')
for i in range(n_proto):
    pct = jpn_probs[:, i].mean() * 100
    if pct > 0.1:
        print(f'    P{i} {prototypes[i]["name"]}: {pct:.2f}%')
max_jpn = jpn_probs.max(axis=1)
print(f'    max_prob: min={max_jpn.min():.4f}, median={np.median(max_jpn):.4f}')

# === 4. 保存 assignment ===
print('\n[Fix] 保存新的软分配...')
assign = pd.DataFrame(probs, columns=[f'P{i}' for i in range(n_proto)])
assign['main_prototype'] = labels
assign['main_prototype_name'] = [prototypes[l]['name'] for l in labels]
assign['max_prob'] = probs.max(axis=1)
assign['context_flexibility'] = feat_df['context_flexibility'].values
for c in meta_cols:
    assign[c] = feat_df[c].values
assign.to_parquet(os.path.join(RES, 'prototype_assignment.parquet'), index=False)
print(f'  已保存: prototype_assignment.parquet ({assign.shape})')

# === 5. 重新生成 country_culture_dist.csv ===
print('[Fix] 重新生成国家级分布...')
w = assign['S018'].fillna(1).values
w = np.where(w > 0, w, 1)
country = assign['B_COUNTRY_ALPHA'].values
p_cols = [f'P{i}' for i in range(n_proto)]

import sys
sys.path.insert(0, os.path.join(BASE, 'code'))
from country_names import COUNTRY_CN

dist_rows = []
for c in pd.unique(country):
    mask = country == c
    wc = w[mask][:, None]
    probs_c = assign.loc[mask, p_cols].values
    dist = (probs_c * wc).sum(axis=0) / wc.sum()
    main_p = int(np.argmax(dist))
    dist_rows.append({
        'country': c,
        'country_cn': COUNTRY_CN.get(c, c),
        'country_label': f'{c}({COUNTRY_CN.get(c, c)})',
        'n': int(mask.sum()),
        'main_prototype_id': main_p,
        'main_prototype_name': prototypes[main_p]['name'],
        'main_prototype_prob': round(float(dist[main_p]), 4),
        **{p_cols[i]: round(float(dist[i]), 4) for i in range(n_proto)},
    })

country_dist = pd.DataFrame(dist_rows).sort_values('main_prototype_name')
country_dist.to_csv(os.path.join(RES, 'country_culture_dist.csv'), index=False, encoding='utf-8-sig')
print(f'  已保存: country_culture_dist.csv ({country_dist.shape})')

# === 6. 保存修复后的模型 ===
with open(os.path.join(RES, 'model.pkl'), 'wb') as f:
    pickle.dump(bundle, f)
print('  模型已更新(带协方差 floor)')

# === 7. 打印关键国家 ===
print('\n[Fix] 关键国家分布 (T={}):'.format(TEMPERATURE))
for c in ['CHN', 'JPN', 'KOR', 'USA', 'DEU', 'GBR', 'EGY', 'RUS', 'BRA', 'IRN']:
    row = country_dist[country_dist['country'] == c]
    if len(row) == 0: continue
    r = row.iloc[0]
    dist_str = ' '.join(f'P{i}={r[p_cols[i]]:.2f}' for i in range(n_proto) if r[p_cols[i]] >= 0.05)
    print(f'  {c}({r["country_cn"]}): 主={r["main_prototype_name"]}({r["main_prototype_prob"]:.2f}) | {dist_str}')

print('\n[Fix] 完成')
