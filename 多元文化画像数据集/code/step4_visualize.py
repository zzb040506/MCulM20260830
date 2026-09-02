"""
Step 4 (v2): 可视化 - 14 原型 + 国家中文名
输出图片到 result/:
  - fig1_prototype_radar.png       14 原型雷达图(小多图)
  - fig2_country_heatmap.png       66 国 × 14 原型概率分布热力图
  - fig3_inglehart_map.png         SACSECVAL × RESEMAVAL 文化地图
  - fig4_country_bars.png          代表国家 14 原型分布柱状图
  - fig5_individual_fingerprint.png  个体文化指纹示例
  - fig6_context_flexibility.png   情境弹性分布
"""
import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.colors as mcolors

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from country_names import COUNTRY_CN, country_label, country_cn

RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')

# === 中文字体 ===
CJK_PATH = '/System/Library/Fonts/Hiragino Sans GB.ttc'
CJK_FONT = FontProperties(fname=CJK_PATH) if os.path.exists(CJK_PATH) else None
if CJK_FONT:
    matplotlib.rcParams['font.sans-serif'] = [CJK_FONT.get_name(), 'DejaVu Sans']
    matplotlib.rcParams['axes.unicode_minus'] = False

# 14 原型配色
PROTO_COLORS = plt.cm.tab20(np.linspace(0, 1, 14))


def load():
    assign = pd.read_parquet(os.path.join(RES, 'prototype_assignment.parquet'))
    feat = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
    with open(os.path.join(RES, 'culture_prototypes.json'), encoding='utf-8') as f:
        proto = json.load(f)
    country_dist = pd.read_csv(os.path.join(RES, 'country_culture_dist.csv'))
    return assign, feat, proto, country_dist


def fig1_prototype_radar(feat, proto):
    """图1: 14 原型雷达图(4×4 小多图)。"""
    print('[Step4] 图1: 14 原型雷达图...', flush=True)
    profiles = pd.DataFrame(proto['profiles'])
    proto_names = [p['name'] for p in proto['prototypes']]
    sizes = [p['size'] for p in proto['prototypes']]
    n = proto['n_prototypes']

    dims = {
        '世俗理性': 'SACSECVAL', '自我表达': 'RESEMAVAL', '自主性': 'AUTONOMY',
        '平等观': 'EQUALITY', '权威服从': 'I_AUTHORITY', '民族主义': 'I_NATIONALISM',
        '宗教虔诚': 'I_DEVOUT', '信任外国人': 'trust_foreign',
        '伦理弹性': 'ethical_flexibility', '排他性': 'exclusion_index',
    }
    dim_names = list(dims.keys())
    n_dim = len(dim_names)
    angles = np.linspace(0, 2 * np.pi, n_dim, endpoint=False).tolist()
    angles += angles[:1]

    # 全局 min/max 归一化(使各子图可比)
    global_min = {d: profiles[c].min() for d, c in dims.items() if c in profiles.columns}
    global_max = {d: profiles[c].max() for d, c in dims.items() if c in profiles.columns}

    rows, cols = 4, 4
    fig, axes = plt.subplots(rows, cols, figsize=(18, 18), subplot_kw=dict(polar=True))
    axes = axes.flatten()

    for i in range(n):
        ax = axes[i]
        vals = []
        for dname, col in dims.items():
            if col in profiles.columns:
                v = profiles.loc[i, col]
                lo, hi = global_min[dname], global_max[dname]
                v = (v - lo) / (hi - lo + 1e-9)  # 归一化到 0-1
                vals.append(max(0, min(1, v)))
            else:
                vals.append(0)
        vals += vals[:1]
        color = PROTO_COLORS[i]
        ax.plot(angles, vals, 'o-', linewidth=1.5, color=color)
        ax.fill(angles, vals, alpha=0.15, color=color)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dim_names, fontproperties=CJK_FONT, fontsize=6.5)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.33, 0.66])
        ax.set_yticklabels([])
        ax.set_title(f'P{i} {proto_names[i]}\n({sizes[i]}人)', fontproperties=CJK_FONT, fontsize=9, pad=8)

    # 隐藏多余子图
    for i in range(n, len(axes)):
        axes[i].set_visible(False)

    plt.suptitle('14 个文化原型画像(各维度归一化)', fontproperties=CJK_FONT, fontsize=16, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(RES, 'fig1_prototype_radar.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig1_prototype_radar.png', flush=True)


def fig2_country_heatmap(country_dist, proto):
    """图2: 66 国 × 14 原型概率分布热力图。"""
    print('[Step4] 图2: 国家×14原型热力图...', flush=True)
    n_proto = proto['n_prototypes']
    proto_names = [p['name'] for p in proto['prototypes']]
    p_cols = [f'P{i}' for i in range(n_proto)]

    df = country_dist.sort_values(['main_prototype_id', 'main_prototype_prob'],
                                   ascending=[True, False]).reset_index(drop=True)
    mat = df[p_cols].values
    labels = [f'{r["country"]}({r["country_cn"]})' for _, r in df.iterrows()]

    fig, ax = plt.subplots(figsize=(10, 16))
    im = ax.imshow(mat, aspect='auto', cmap='YlOrRd', vmin=0, vmax=1)
    ax.set_xticks(range(n_proto))
    ax.set_xticklabels([f'P{i}\n{proto_names[i]}' for i in range(n_proto)],
                       fontproperties=CJK_FONT, fontsize=7, rotation=0, ha='center')
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=6)
    ax.set_xlabel('文化原型', fontproperties=CJK_FONT, fontsize=12)
    ax.set_title('66 国 × 14 原型 概率分布热力图', fontproperties=CJK_FONT, fontsize=14, pad=12)

    for i in range(len(labels)):
        for j in range(n_proto):
            v = mat[i, j]
            if v >= 0.08:
                ax.text(j, i, f'{v:.2f}', ha='center', va='center',
                        fontsize=5, color='white' if v > 0.5 else 'black')

    plt.colorbar(im, ax=ax, label='概率', shrink=0.4).ax.tick_params(labelsize=7)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'fig2_country_heatmap.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig2_country_heatmap.png', flush=True)


def fig3_inglehart_map(assign, country_dist, proto):
    """图3: Inglehart 文化地图,国家点按主原型着色。"""
    print('[Step4] 图3: Inglehart 文化地图...', flush=True)
    w = assign['S018'].fillna(1).values
    w = np.where(w > 0, w, 1)
    country = assign['B_COUNTRY_ALPHA'].values

    rows = []
    for c in pd.unique(country):
        mask = country == c
        wc = w[mask]
        rows.append({
            'country': c,
            'country_cn': COUNTRY_CN.get(c, c),
            'sacsecval': np.average(assign.loc[mask, 'SACSECVAL'], weights=wc),
            'resemaval': np.average(assign.loc[mask, 'RESEMAVAL'], weights=wc),
            'n': mask.sum(),
        })
    sdf = pd.DataFrame(rows).merge(
        country_dist[['country', 'main_prototype_id', 'main_prototype_name']], on='country')

    fig, ax = plt.subplots(figsize=(13, 10))
    for pid in range(proto['n_prototypes']):
        sub = sdf[sdf['main_prototype_id'] == pid]
        if len(sub) == 0:
            continue
        color = PROTO_COLORS[pid]
        pname = proto['prototypes'][pid]['name']
        ax.scatter(sub['sacsecval'], sub['resemaval'], s=sub['n'] / 8,
                   c=[color], alpha=0.75, edgecolors='white', linewidth=0.5,
                   label=f'P{pid} {pname}')

    for _, r in sdf.iterrows():
        ax.annotate(f'{r["country"]}({r["country_cn"]})',
                    (r['sacsecval'], r['resemaval']),
                    fontsize=5.5, ha='center', va='bottom', fontproperties=CJK_FONT)

    ax.set_xlabel('世俗-传统 (SACSECVAL, ←传统/宗教  世俗理性→)', fontproperties=CJK_FONT, fontsize=11)
    ax.set_ylabel('自我表达 (RESEMAVAL, ←生存取向  自我表达→)', fontproperties=CJK_FONT, fontsize=11)
    ax.set_title('Inglehart-Welzel 文化地图:66 国 × 14 原型', fontproperties=CJK_FONT, fontsize=14, pad=12)
    ax.axhline(0.5, color='gray', linestyle='--', alpha=0.3)
    ax.axvline(0.5, color='gray', linestyle='--', alpha=0.3)
    ax.legend(prop=CJK_FONT, fontsize=7, loc='lower right', ncol=2, framealpha=0.8)
    ax.grid(alpha=0.2)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'fig3_inglehart_map.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig3_inglehart_map.png', flush=True)


def fig4_country_bars(country_dist, proto):
    """图4: 代表国家 14 原型分布堆叠柱状图。"""
    print('[Step4] 图4: 代表国家分布柱状图...', flush=True)
    n_proto = proto['n_prototypes']
    proto_names = [p['name'] for p in proto['prototypes']]
    p_cols = [f'P{i}' for i in range(n_proto)]

    reps = ['CHN', 'JPN', 'KOR', 'USA', 'DEU', 'GBR', 'FRA' if False else 'FRA',
            'SWE' if False else 'NLD', 'RUS', 'EGY', 'JOR', 'IRN', 'NGA', 'BRA',
            'MEX', 'IDN', 'THA', 'TUR', 'VNM', 'ZWE']
    reps = [c for c in reps if c in country_dist['country'].values]
    sub = country_dist[country_dist['country'].isin(reps)].copy()
    # 按 P5(传统宗教型1) 排序
    sub = sub.sort_values('P5', ascending=True)

    mat = sub[p_cols].values
    labels = [f'{r["country"]}({r["country_cn"]})' for _, r in sub.iterrows()]

    fig, ax = plt.subplots(figsize=(12, 8))
    left = np.zeros(len(labels))
    for j in range(n_proto):
        color = PROTO_COLORS[j]
        ax.barh(labels, mat[:, j], left=left, color=color,
                label=f'P{j} {proto_names[j]}', edgecolor='white', linewidth=0.3)
        for i, v in enumerate(mat[:, j]):
            if v >= 0.08:
                ax.text(left[i] + v / 2, i, f'{v:.0%}', ha='center', va='center',
                        fontsize=6, color='white', fontweight='bold')
        left += mat[:, j]

    ax.set_xlabel('文化原型概率', fontproperties=CJK_FONT, fontsize=11)
    ax.set_title('代表国家的 14 原型文化分布', fontproperties=CJK_FONT, fontsize=14, pad=12)
    ax.set_xlim(0, 1)
    ax.set_yticklabels(labels, fontproperties=CJK_FONT, fontsize=9)
    ax.legend(prop=CJK_FONT, fontsize=6.5, loc='upper right', bbox_to_anchor=(1.0, -0.06), ncol=7)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'fig4_country_bars.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig4_country_bars.png', flush=True)


def fig5_individual_fingerprint(assign, proto):
    """图5: 个体文化指纹示例(4 个群体,14 原型饼图)。"""
    print('[Step4] 图5: 个体文化指纹...', flush=True)
    n_proto = proto['n_prototypes']
    proto_names = [p['name'] for p in proto['prototypes']]
    p_cols = [f'P{i}' for i in range(n_proto)]
    country = assign['B_COUNTRY_ALPHA'].values
    age = assign['age'].values

    samples = [
        ('CHN(<35岁青年)', (country == 'CHN') & (age < 35)),
        ('JPN(日本)', country == 'JPN'),
        ('EGY(埃及)', country == 'EGY'),
        ('DEU(德国)', country == 'DEU'),
    ]

    fig, axes = plt.subplots(1, len(samples), figsize=(6 * len(samples), 5))
    if len(samples) == 1:
        axes = [axes]

    for ax, (label, mask) in zip(axes, samples):
        idx = np.where(mask.values if hasattr(mask, 'values') else mask)[0]
        probs = assign.loc[idx, p_cols].values.mean(axis=0)
        # 只显示 >=5% 的
        show = probs >= 0.05
        labels_pie = [f'P{i} {proto_names[i]}\n{probs[i]:.0%}' for i in range(n_proto) if show[i]]
        vals = probs[show]
        colors = [PROTO_COLORS[i] for i in range(n_proto) if show[i]]
        wedges, texts = ax.pie(vals, labels=labels_pie, colors=colors, startangle=90,
                               textprops={'fontproperties': CJK_FONT, 'fontsize': 7})
        ax.set_title(f'{label}\n(n={len(idx)})', fontproperties=CJK_FONT, fontsize=11)

    plt.suptitle('个体文化指纹:14 原型概率分布', fontproperties=CJK_FONT, fontsize=15, y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'fig5_individual_fingerprint.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig5_individual_fingerprint.png', flush=True)


def fig6_context_flexibility(assign):
    """图6: 各国情境弹性分数(中文名)。"""
    print('[Step4] 图6: 情境弹性分布...', flush=True)
    country = assign['B_COUNTRY_ALPHA'].values
    ctx = assign['context_flexibility'].values
    w = assign['S018'].fillna(1).values
    w = np.where(w > 0, w, 1)

    rows = []
    for c in pd.unique(country):
        mask = country == c
        rows.append({'country': c, 'country_cn': COUNTRY_CN.get(c, c), 'ctx': np.average(ctx[mask], weights=w[mask])})
    df = pd.DataFrame(rows).sort_values('ctx')

    labels = [f'{r["country"]}({r["country_cn"]})' for _, r in df.iterrows()]
    fig, ax = plt.subplots(figsize=(8, 14))
    colors = plt.cm.RdYlGn((df['ctx'] - df['ctx'].min()) / (df['ctx'].max() - df['ctx'].min() + 1e-9))
    ax.barh(labels, df['ctx'].values, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_xlabel('情境弹性分数(高=能在不同情境切换文化模式)', fontproperties=CJK_FONT, fontsize=10)
    ax.set_title('66 国情境弹性分数(加权均值)', fontproperties=CJK_FONT, fontsize=13, pad=10)
    ax.set_yticklabels(labels, fontproperties=CJK_FONT, fontsize=6.5)
    plt.tight_layout()
    plt.savefig(os.path.join(RES, 'fig6_context_flexibility.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print('  已保存 fig6_context_flexibility.png', flush=True)


def main():
    assign, feat, proto, country_dist = load()
    # 补充可视化需要的列
    for c in ['SACSECVAL', 'RESEMAVAL', 'age']:
        assign[c] = feat[c].values
    print(f'[Step4] 数据: {len(assign)} 个体, {len(country_dist)} 国, {proto["n_prototypes"]} 原型', flush=True)

    fig1_prototype_radar(feat, proto)
    fig2_country_heatmap(country_dist, proto)
    fig3_inglehart_map(assign, country_dist, proto)
    fig4_country_bars(country_dist, proto)
    fig5_individual_fingerprint(assign, proto)
    fig6_context_flexibility(assign)
    print('\n[Step4] 全部图表已生成', flush=True)


if __name__ == '__main__':
    main()
