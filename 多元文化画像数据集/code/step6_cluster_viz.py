"""
多元文化画像 - GMM 14 原型聚类结构可视化
展示 68 维特征空间中 14 个聚类"如何聚在一起"：
  - fig8_pca_scatter.png   PCA 降维全量散点(最忠实于聚类结构)
  - fig8_tsne_scatter.png  t-SNE 降维抽样散点(展示局部邻近结构)
  - fig8_pca_centers.png   PCA 空间 14 个聚类中心 + 95% 置信椭圆
"""
import os, sys, pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Ellipse
import warnings
warnings.filterwarnings('ignore')

BASE = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集'
RES = os.path.join(BASE, 'result')

CJK_PATH = '/System/Library/Fonts/PingFang.ttc'
CJK_FONT = FontProperties(fname=CJK_PATH) if os.path.exists(CJK_PATH) else None
if CJK_FONT:
    plt.rcParams['font.sans-serif'] = [CJK_FONT.get_name(), 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 14 原型配色(tab20 循环)
PROTO_COLORS = plt.cm.tab20(np.linspace(0, 1, 20))[::1]
COLORS = [plt.cm.tab20(i % 20) for i in range(14)]


def load():
    """加载标准化特征、GMM 模型、原型名。"""
    print('[Load] 加载数据...')
    feat = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
    with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
        bundle = pickle.load(f)
    scaler = bundle['scaler']
    gmm = bundle['gmm']
    feat_cols = bundle['feat_cols']
    proto_names = [p['name'] for p in bundle['prototypes']]
    X = feat[feat_cols].values.astype(float)
    X_scaled = scaler.transform(X)
    labels = gmm.predict(X_scaled)
    return X_scaled, labels, gmm, proto_names, feat['B_COUNTRY_ALPHA'].values


def plot_pca_scatter(X_scaled, labels, proto_names):
    """全量 PCA 二维散点图。"""
    from sklearn.decomposition import PCA
    print('[Plot] PCA 降维(全量 97220 点)...')
    pca = PCA(n_components=2, random_state=42)
    Z = pca.fit_transform(X_scaled)
    evr = pca.explained_variance_ratio_
    print(f'  PCA 前两维解释方差: {evr[0]:.2%} + {evr[1]:.2%} = {evr.sum():.2%}')

    fig, ax = plt.subplots(figsize=(14, 11))
    for k in range(14):
        mask = labels == k
        ax.scatter(Z[mask, 0], Z[mask, 1], s=3, alpha=0.25, color=COLORS[k],
                   label=f'P{k} {proto_names[k]}', rasterized=True)
    ax.set_xlabel(f'PC1 ({evr[0]:.1%} 方差)', fontsize=12)
    ax.set_ylabel(f'PC2 ({evr[1]:.1%} 方差)', fontsize=12)
    ax.set_title('14 个文化原型聚类结构(PCA, 68 维 → 2 维)',
                 fontproperties=CJK_FONT, fontsize=16, fontweight='bold', pad=15)
    ax.legend(prop=CJK_FONT, fontsize=9, markerscale=4, ncol=2,
              loc='upper right', framealpha=0.9)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(RES, 'fig8_pca_scatter.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  已保存: {out}')
    return pca


def plot_pca_centers(X_scaled, labels, gmm, proto_names, pca):
    """PCA 空间 14 个聚类中心 + 置信椭圆。"""
    print('[Plot] 聚类中心 + 置信椭圆...')
    means = gmm.means_          # 标准化空间中心
    centers = pca.transform(means)

    fig, ax = plt.subplots(figsize=(14, 11))

    # 背景: 抽样 5000 点浅色底
    rng = np.random.default_rng(42)
    idx = rng.choice(len(X_scaled), 5000, replace=False)
    Z_bg = pca.transform(X_scaled[idx])
    ax.scatter(Z_bg[:, 0], Z_bg[:, 1], s=2, c='#d0d0d0', alpha=0.35, rasterized=True)

    # 每个类的置信椭圆(在 PCA 空间)
    for k in range(14):
        mask = labels == k
        Zk = pca.transform(X_scaled[mask])
        mean = Zk.mean(axis=0)
        cov = np.cov(Zk, rowvar=False)
        # 特征值分解画椭圆
        vals, vecs = np.linalg.eigh(cov)
        order = vals.argsort()[::-1]
        vals, vecs = vals[order], vecs[:, order]
        angle = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
        width, height = 2 * np.sqrt(5.991 * vals)  # 95% 置信
        ell = Ellipse(mean, width, height, angle=angle, facecolor=COLORS[k],
                      alpha=0.12, edgecolor=COLORS[k], linewidth=1.6)
        ax.add_patch(ell)

    # 聚类中心点
    for k in range(14):
        ax.scatter(centers[k, 0], centers[k, 1], s=320, c=[COLORS[k]],
                   edgecolors='white', linewidth=2, zorder=5)
        ax.annotate(f'{k}\n{proto_names[k]}', (centers[k, 0], centers[k, 1]),
                    xytext=(6, 6), textcoords='offset points',
                    fontproperties=CJK_FONT, fontsize=8, fontweight='bold', zorder=6)

    ax.set_xlabel('PC1', fontsize=12)
    ax.set_ylabel('PC2', fontsize=12)
    ax.set_title('14 个文化原型聚类中心与 95% 置信椭圆(PCA 空间)',
                 fontproperties=CJK_FONT, fontsize=16, fontweight='bold', pad=15)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(RES, 'fig8_pca_centers.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  已保存: {out}')


def plot_tsne_scatter(X_scaled, labels, proto_names):
    """t-SNE 抽样散点(展示局部邻近结构)。"""
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    print('[Plot] t-SNE 降维(抽样 10000 点)...')
    rng = np.random.default_rng(42)
    idx = rng.choice(len(X_scaled), 10000, replace=False)
    X_sub = X_scaled[idx]
    lab_sub = labels[idx]

    # 先 PCA 到 50 维加速
    pca50 = PCA(n_components=50, random_state=42)
    X50 = pca50.fit_transform(X_sub)

    tsne = TSNE(n_components=2, perplexity=30, random_state=42,
                init='pca', learning_rate='auto')
    Z = tsne.fit_transform(X50)

    fig, ax = plt.subplots(figsize=(14, 11))
    for k in range(14):
        mask = lab_sub == k
        ax.scatter(Z[mask, 0], Z[mask, 1], s=6, alpha=0.5, color=COLORS[k],
                   label=f'P{k} {proto_names[k]}', rasterized=True)
    ax.set_xlabel('t-SNE 维度 1', fontsize=12)
    ax.set_ylabel('t-SNE 维度 2', fontsize=12)
    ax.set_title('14 个文化原型聚类结构(t-SNE, 抽样 10000 点)',
                 fontproperties=CJK_FONT, fontsize=16, fontweight='bold', pad=15)
    ax.legend(prop=CJK_FONT, fontsize=9, markerscale=4, ncol=2,
              loc='upper right', framealpha=0.9)
    ax.grid(alpha=0.25)
    plt.tight_layout()
    out = os.path.join(RES, 'fig8_tsne_scatter.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f'  已保存: {out}')


def main():
    X_scaled, labels, gmm, proto_names, countries = load()
    pca = plot_pca_scatter(X_scaled, labels, proto_names)
    plot_pca_centers(X_scaled, labels, gmm, proto_names, pca)
    plot_tsne_scatter(X_scaled, labels, proto_names)
    print('\n[Done] 聚类结构可视化完成')


if __name__ == '__main__':
    main()
