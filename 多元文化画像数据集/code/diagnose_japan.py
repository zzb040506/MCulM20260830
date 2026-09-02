"""排查日本为什么是 100% 单一原型。"""
import os, sys, pickle, numpy as np, pandas as pd
sys.stdout.reconfigure(line_buffering=True)

BASE = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集'
RES = os.path.join(BASE, 'result')

with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
    bundle = pickle.load(f)
gmm = bundle['gmm']
scaler = bundle['scaler']
feat_cols = bundle['feat_cols']
prototypes = bundle['prototypes']
n_proto = gmm.n_components

feat_df = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
jpn_mask = feat_df['B_COUNTRY_ALPHA'] == 'JPN'
print(f'日本样本数: {jpn_mask.sum()}')

jpn_features = feat_df.loc[jpn_mask, feat_cols].values.astype(float)
jpn_scaled = scaler.transform(jpn_features)

print(f'\n=== GMM 信息 ===')
print(f'covariance_type: {gmm.covariance_type}')
print(f'covariances_ shape: {gmm.covariances_.shape}')
# 检查 diag 方差
for i in range(min(5, n_proto)):
    var_vec = gmm.covariances_[i]
    print(f'  P{i} {prototypes[i]["name"]}: var min={var_vec.min():.2e}, median={np.median(var_vec):.2e}, max={var_vec.max():.2e}')

# 日本样本的软分配概率
jpn_probs = gmm.predict_proba(jpn_scaled)
print(f'\n=== 日本样本软分配 ===')
print(f'形状: {jpn_probs.shape}')
avg_probs = jpn_probs.mean(axis=0)
for i in range(n_proto):
    print(f'  P{i} {prototypes[i]["name"]}: {avg_probs[i]:.4f} ({avg_probs[i]*100:.2f}%)')

max_probs = jpn_probs.max(axis=1)
print(f'\n最大概率统计:')
print(f'  min={max_probs.min():.4f}, median={np.median(max_probs):.4f}, max={max_probs.max():.4f}')
print(f'  > 0.99 的比例: {(max_probs > 0.99).mean():.2%}')

# 极端样本
if (max_probs > 0.99).any():
    extreme = jpn_probs[max_probs > 0.99]
    print(f'\n极端样本({len(extreme)}人)的各原型概率:')
    for i in range(n_proto):
        print(f'  P{i}: {extreme[:, i].mean():.4f}')

# 对比其他国家
print(f'\n=== 其他国家 Top3 ===')
for c in ['CHN', 'DEU', 'GBR', 'USA']:
    mask = feat_df['B_COUNTRY_ALPHA'] == c
    probs = gmm.predict_proba(scaler.transform(feat_df.loc[mask, feat_cols].values.astype(float)))
    avg = probs.mean(axis=0)
    top3 = np.argsort(avg)[-3:][::-1]
    print(f'{c}: top3 = ' + ', '.join(f'P{i}={avg[i]:.2%}' for i in top3))
