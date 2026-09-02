"""
Step 2: GMM 软分配 + 文化原型发现
输入: result/culture_features.parquet
输出:
  - result/culture_prototypes.json (12 原型 × 特征画像 + 自动命名)
  - result/prototype_assignment.parquet (97,220 × 12 概率 + 主原型 + 情境弹性)
  - result/bic_curve.png (BIC 选 K 曲线)
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

sys.stdout.reconfigure(line_buffering=True)  # 实时输出

# 中文字体配置(macOS)
for _f in ['PingFang SC', 'Heiti TC', 'Arial Unicode MS', 'STHeiti', 'Songti SC']:
    try:
        from matplotlib.font_manager import FontProperties
        fp = FontProperties(family=_f)
        if fp.get_name():
            matplotlib.rcParams['font.sans-serif'] = [_f, 'DejaVu Sans']
            matplotlib.rcParams['axes.unicode_minus'] = False
            break
    except Exception:
        continue

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(BASE, 'result')

# 元信息列(不参与建模)
META_COLS = ['B_COUNTRY_ALPHA', 'A_YEAR', 'W_WEIGHT', 'S018']

# 聚类用核心连续特征(约 40 维,排除整数编码的分类变量和高基数 ID)
CLUSTER_FEATS = [
    # 地区
    'urban', 'townsize', 'longitude', 'latitude',
    # 语言
    'lang_home_eq_interview', 'lang_official_match',
    # 价值观
    'SACSECVAL', 'RESEMAVAL', 'I_AUTHORITY', 'I_NATIONALISM', 'I_DEVOUT',
    'I_TRUSTARMY', 'I_TRUSTPOLICE', 'I_TRUSTCOURTS',
    'I_NORM1', 'I_NORM2', 'I_NORM3',
    'AUTONOMY', 'EQUALITY', 'CHOICE', 'VOICE',
    'DEFIANCE', 'DISBELIEF', 'RELATIVISM', 'SCEPTICISM',
    'Y001', 'Y002', 'Y003',
    # 社会规范
    'trust_general', 'trust_family', 'trust_neighbor', 'trust_acquaintance',
    'trust_stranger', 'trust_other_religion', 'trust_foreign', 'trust_decay',
    'institutional_trust', 'ethical_flexibility', 'work_ethic', 'gov_power_acceptance',
    # 关系结构
    'n_children', 'household_size', 'family_importance', 'friend_importance', 'leisure_importance',
    'immigrant_generations', 'org_density', 'identity_radius',
    'autonomy_vs_obedience', 'exclusion_index',
    # 宗教
    'god_importance', 'believe_god', 'believe_afterlife', 'believe_hell', 'believe_heaven',
    'service_attendance', 'church_trust', 'relig_importance', 'relig_belief', 'relig_practice',
    # 社会经济(连续)
    'age', 'social_class', 'income_level', 'log_gdp', 'gini', 'hdi', 'internet_users',
    'context_flexibility',
]


def auto_name_prototypes(prototype_profiles):
    """基于跨原型相对 z-score 自动命名每个原型。

    每种文化类型有一组"签名特征"(应高/应低)。对每个原型计算其签名特征相对
    全体原型均值的标准化偏离,得分最高的类型即为其命名。这样命名能真正区分原型。
    """
    n = len(prototype_profiles)
    global_mean = prototype_profiles.mean()

    # 每种类型的签名特征:[(特征, 方向)]  方向 +1=越高越典型, -1=越低越典型
    type_signatures = {
        '传统宗教型': [
            ('god_importance', +1), ('relig_belief', +1), ('relig_practice', +1),
            ('I_DEVOUT', +1), ('exclusion_index', +1),
            ('ethical_flexibility', -1), ('SACVALVAL', -1) if False else ('SACSECVAL', -1),
            ('autonomy_vs_obedience', -1),
        ],
        '世俗自主型': [
            ('SACSECVAL', +1), ('AUTONOMY', +1), ('ethical_flexibility', +1),
            ('autonomy_vs_obedience', +1), ('DISBELIEF', +1),
            ('god_importance', -1), ('relig_practice', -1), ('I_DEVOUT', -1),
        ],
        '集体权威型': [
            ('I_AUTHORITY', +1), ('I_NATIONALISM', +1), ('org_density', +1),
            ('trust_family', +1), ('I_TRUSTARMY', +1),
            ('AUTONOMY', -1), ('trust_foreign', -1), ('identity_radius', -1),
        ],
        '个人表达型': [
            ('VOICE', +1), ('EQUALITY', +1), ('CHOICE', +1), ('RESEMAVAL', +1),
            ('trust_foreign', +1),
            ('I_AUTHORITY', -1), ('exclusion_index', -1),
        ],
        '生存焦虑型': [
            ('I_NATIONALISM', +1), ('exclusion_index', +1), ('gov_power_acceptance', +1),
            ('RESEMAVAL', -1), ('trust_general', -1), ('institutional_trust', -1),
            ('trust_foreign', -1),
        ],
        '开放世界型': [
            ('identity_radius', +1), ('trust_foreign', +1), ('ethical_flexibility', +1),
            ('trust_stranger', +1),
            ('exclusion_index', -1), ('I_NATIONALISM', -1),
        ],
    }

    # 计算每个特征在原型间的标准差(用于 z-score)
    stds = prototype_profiles.std()
    stds = stds.replace(0, 1)  # 避免除零

    names = []
    for i in range(n):
        row = prototype_profiles.iloc[i]
        type_scores = {}
        for tname, sig in type_signatures.items():
            zs = []
            for feat, direction in sig:
                if feat not in prototype_profiles.columns:
                    continue
                z = (row[feat] - global_mean[feat]) / stds[feat]
                zs.append(direction * z)
            type_scores[tname] = np.mean(zs) if zs else 0
        best = max(type_scores, key=type_scores.get)
        names.append((best, type_scores))
    return names


def main():
    print('[Step2] 读取特征...', flush=True)
    df = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
    print(f'  形状: {df.shape}', flush=True)

    feat_cols = [c for c in CLUSTER_FEATS if c in df.columns]
    print(f'  聚类特征数: {len(feat_cols)}', flush=True)
    X_raw = df[feat_cols].values.astype(float)

    # 标准化
    print('[Step2] 标准化特征...', flush=True)
    scaler = StandardScaler()
    X = scaler.fit_transform(X_raw)

    # === BIC 选 K (diag 协方差,n_init=1 加速) ===
    print('[Step2] BIC 选 K (diag 协方差, K=8..14)...', flush=True)
    bic_results = {}
    for k in range(8, 15):
        gmm = GaussianMixture(n_components=k, covariance_type='diag',
                              random_state=42, max_iter=100, n_init=1)
        gmm.fit(X)
        bic_results[k] = gmm.bic(X)
        print(f'  K={k}: BIC={bic_results[k]:.0f}', flush=True)

    best_k = min(bic_results, key=bic_results.get)
    print(f'  最优 K = {best_k}', flush=True)

    # BIC 曲线图
    plt.figure(figsize=(8, 4))
    plt.plot(list(bic_results.keys()), list(bic_results.values()), 'o-', color='#2E5C8A')
    plt.axvline(best_k, color='r', linestyle='--', label=f'Best K={best_k}')
    plt.xlabel('Number of Prototypes (K)')
    plt.ylabel('BIC (lower is better)')
    plt.title('GMM BIC vs K - 文化原型数选择')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'bic_curve.png'), dpi=150)
    plt.close()
    print(f'  BIC 曲线已保存: result/bic_curve.png', flush=True)

    # === 最终 GMM (diag, n_init=3 稳定结果) ===
    print(f'[Step2] 训练最终 GMM (K={best_k}, diag)...', flush=True)
    gmm = GaussianMixture(n_components=best_k, covariance_type='diag',
                           random_state=42, max_iter=200, n_init=3)
    gmm.fit(X)
    probs = gmm.predict_proba(X)
    labels = gmm.predict(X)
    print(f'  软分配矩阵: {probs.shape}', flush=True)

    # 原型画像(反标准化到原始尺度,便于解读)
    means_orig = scaler.inverse_transform(gmm.means_)
    prototype_profiles = pd.DataFrame(means_orig, columns=feat_cols)

    # 自动命名(跨原型相对 z-score)
    print('[Step2] 自动命名原型...', flush=True)
    names_scores = auto_name_prototypes(prototype_profiles)
    prototype_info = []
    name_counts = {}
    for i in range(best_k):
        name, scores = names_scores[i]
        # 处理重名:加编号后缀
        if name in name_counts:
            name_counts[name] += 1
            name = f'{name}II'
        else:
            name_counts[name] = 1
        size = int((labels == i).sum())
        pct = size / len(labels) * 100
        top_type = max(scores, key=scores.get)
        print(f'  P{i} {name}: {size} 人 ({pct:.1f}%) | top: {top_type}={scores[top_type]:.2f}', flush=True)
        prototype_info.append({
            'id': i,
            'name': name,
            'size': size,
            'pct': round(pct, 2),
            'top_score': round(max(scores.values()), 3),
            'scores': {k: round(v, 3) for k, v in scores.items()},
        })

    # 保存原型画像 JSON
    prototypes_out = {
        'n_prototypes': best_k,
        'feature_cols': feat_cols,
        'prototypes': prototype_info,
        'profiles': prototype_profiles.round(4).to_dict(orient='records'),
    }
    with open(os.path.join(RES, 'culture_prototypes.json'), 'w', encoding='utf-8') as f:
        json.dump(prototypes_out, f, ensure_ascii=False, indent=2)
    print(f'  原型画像已保存: result/culture_prototypes.json')

    # 保存个体软分配
    assign = pd.DataFrame(probs, columns=[f'P{i}' for i in range(best_k)])
    assign['main_prototype'] = labels
    assign['main_prototype_name'] = [prototype_info[l]['name'] for l in labels]
    assign['max_prob'] = probs.max(axis=1)
    assign['context_flexibility'] = df['context_flexibility'].values
    assign['B_COUNTRY_ALPHA'] = df['B_COUNTRY_ALPHA'].values
    assign['A_YEAR'] = df['A_YEAR'].values
    assign['W_WEIGHT'] = df['W_WEIGHT'].values
    assign['S018'] = df['S018'].values
    assign.to_parquet(os.path.join(RES, 'prototype_assignment.parquet'), index=False)
    print(f'  软分配已保存: result/prototype_assignment.parquet ({assign.shape})')

    # 保存 scaler 与 gmm(供查询 API 用)
    import pickle
    with open(os.path.join(RES, 'model.pkl'), 'wb') as f:
        pickle.dump({'scaler': scaler, 'gmm': gmm, 'feat_cols': feat_cols,
                    'prototypes': prototype_info}, f)
    print(f'  模型已保存: result/model.pkl')

    print(f'\n[Step2] 完成。{best_k} 个文化原型,覆盖 {len(df)} 个个体。')


if __name__ == '__main__':
    main()
