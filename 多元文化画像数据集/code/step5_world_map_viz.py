"""
多元文化画像 - 7维度世界地图可视化
以世界地图为基底，展示不同国家/地区的文化画像差异

7维度:
1. 地区/地理
2. 语言
3. 价值观
4. 社会规范
5. 关系结构
6. 宗教/传统
7. 社会经济
"""
import os, sys, numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import warnings
warnings.filterwarnings('ignore')

# ============ 配置 ============
BASE = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集'
RES = os.path.join(BASE, 'result')

CJK_PATH = '/System/Library/Fonts/PingFang.ttc'
CJK_FONT = FontProperties(fname=CJK_PATH) if os.path.exists(CJK_PATH) else None
if CJK_FONT:
    plt.rcParams['font.sans-serif'] = [CJK_FONT.get_name(), 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ============ 7维度特征映射 ============
DIM_MAP = {
    '地区/地理': {
        'features': ['latitude', 'longitude', 'urban', 'townsize'],
        'label': '地理分布',
        'cmap': 'YlGnBu',
    },
    '语言': {
        'features': ['lang_home_eq_interview', 'lang_official_match'],
        'label': '语言一致性',
        'cmap': 'Oranges',
    },
    '价值观': {
        'features': [
            'SACSECVAL', 'RESEMAVAL', 'AUTONOMY', 'EQUALITY',
            'I_AUTHORITY', 'I_NATIONALISM', 'I_DEVOUT',
            'CHOICE', 'VOICE', 'DISBELIEF', 'RELATIVISM',
            'SCEPTICISM', 'DEFIANCE',
            'I_TRUSTARMY', 'I_TRUSTPOLICE', 'I_TRUSTCOURTS',
            'I_NORM1', 'I_NORM2', 'I_NORM3',
            'Y001', 'Y002', 'Y003'
        ],
        'label': '价值取向',
        'cmap': 'RdYlBu',
    },
    '社会规范': {
        'features': [
            'trust_general', 'trust_family', 'trust_neighbor',
            'trust_acquaintance', 'trust_stranger', 'trust_foreign',
            'trust_other_religion', 'trust_decay',
            'institutional_trust', 'ethical_flexibility',
            'work_ethic', 'gov_power_acceptance'
        ],
        'label': '社会规范',
        'cmap': 'Greens',
    },
    '关系结构': {
        'features': [
            'family_importance', 'friend_importance', 'leisure_importance',
            'marital_status', 'n_children', 'household_size',
            'live_with_parents', 'immigrant_generations',
            'org_density', 'identity_radius',
            'autonomy_vs_obedience', 'exclusion_index'
        ],
        'label': '关系模式',
        'cmap': 'Purples',
    },
    '宗教/传统': {
        'features': [
            'god_importance', 'believe_god', 'believe_afterlife',
            'believe_heaven', 'believe_hell',
            'church_trust', 'service_attendance',
            'relig_importance', 'relig_belief', 'relig_practice'
        ],
        'label': '宗教虔诚',
        'cmap': 'Reds',
    },
    '社会经济': {
        'features': [
            'age', 'edu_isced', 'edu_3group', 'employment',
            'occupation', 'income_level', 'social_class',
            'log_gdp', 'gini', 'hdi', 'internet_users'
        ],
        'label': '社会经济',
        'cmap': 'Blues',
    },
}

# 国家中文名映射
COUNTRY_CN = {
    'CHN': '中国', 'JPN': '日本', 'KOR': '韩国', 'USA': '美国', 'CAN': '加拿大',
    'MEX': '墨西哥', 'BRA': '巴西', 'ARG': '阿根廷', 'GBR': '英国', 'FRA': '法国',
    'DEU': '德国', 'ITA': '意大利', 'ESP': '西班牙', 'PRT': '葡萄牙', 'NLD': '荷兰',
    'BEL': '比利时', 'SWE': '瑞典', 'NOR': '挪威', 'DNK': '丹麦', 'FIN': '芬兰',
    'POL': '波兰', 'CZE': '捷克', 'SVK': '斯洛伐克', 'HUN': '匈牙利', 'ROU': '罗马尼亚',
    'BGR': '保加利亚', 'HRV': '克罗地亚', 'SVN': '斯洛文尼亚', 'RUS': '俄罗斯', 'UKR': '乌克兰',
    'TUR': '土耳其', 'IRN': '伊朗', 'IRQ': '伊拉克', 'SAU': '沙特', 'EGY': '埃及',
    'PAK': '巴基斯坦', 'IND': '印度', 'IDN': '印尼', 'MYS': '马来西亚', 'THA': '泰国',
    'VNM': '越南', 'PHL': '菲律宾', 'SGP': '新加坡', 'KHM': '柬埔寨', 'MMR': '缅甸',
    'KAZ': '哈萨克斯坦', 'UZB': '乌兹别克斯坦', 'AZE': '阿塞拜疆', 'GEO': '格鲁吉亚', 'ARM': '亚美尼亚',
    'ZAF': '南非', 'NGA': '尼日利亚', 'KEN': '肯尼亚', 'ETH': '埃塞俄比亚', 'TZA': '坦桑尼亚',
    'GHA': '加纳', 'UGA': '乌干达', 'ZWE': '津巴布韦', 'BWA': '博茨瓦纳', 'ZMB': '赞比亚',
    'AUS': '澳大利亚', 'NZL': '新西兰', 'CHL': '智利', 'COL': '哥伦比亚', 'PER': '秘鲁',
    'JOR': '约旦', 'LBN': '黎巴嫩', 'ISR': '以色列', 'PSE': '巴勒斯坦', 'YEM': '也门',
    'BOL': '玻利维亚', 'ECU': '厄瓜多尔', 'VEN': '委内瑞拉', 'PRY': '巴拉圭', 'URY': '乌拉圭',
    'MNG': '蒙古', 'TWN': '台湾', 'HKG': '香港', 'MAC': '澳门',
    'ALB': '阿尔巴尼亚', 'LVA': '拉脱维亚', 'LTU': '立陶宛', 'EST': '爱沙尼亚', 'ISL': '冰岛',
}

def load_data():
    """加载特征数据"""
    import json
    print('[Load] 加载文化特征数据...')
    feat = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
    print(f'  样本数: {len(feat)}')
    
    # 加载原型信息
    with open(os.path.join(RES, 'culture_prototypes.json'), 'r', encoding='utf-8') as f:
        proto = json.load(f)
    
    # 加载国家分布
    country_dist = pd.read_csv(os.path.join(RES, 'country_culture_dist.csv'))
    
    return feat, proto, country_dist

def compute_country_dimensions(feat):
    """计算每个国家在7个维度上的统计值"""
    print('[Compute] 计算国家级7维度统计值...')
    
    results = []
    countries = feat['B_COUNTRY_ALPHA'].unique()
    
    for country in countries:
        mask = feat['B_COUNTRY_ALPHA'] == country
        subset = feat[mask]
        
        # 计算每个维度的均值
        dim_values = {}
        for dim_name, dim_config in DIM_MAP.items():
            features = dim_config['features']
            available = [f for f in features if f in subset.columns]
            if available:
                # 标准化后取均值作为该维度的"画像得分"
                vals = subset[available].copy()
                # 对每个特征做 min-max 归一化
                for col in vals.columns:
                    vmin, vmax = vals[col].min(), vals[col].max()
                    if vmax - vmin > 1e-9:
                        vals[col] = (vals[col] - vmin) / (vmax - vmin)
                    else:
                        vals[col] = 0.5
                dim_values[dim_name] = vals.mean().mean()
            else:
                dim_values[dim_name] = np.nan
        
        # 获取经纬度 (取均值)
        lat = subset['latitude'].mean() if 'latitude' in subset.columns else np.nan
        lon = subset['longitude'].mean() if 'longitude' in subset.columns else np.nan
        
        results.append({
            'country': country,
            'country_cn': COUNTRY_CN.get(country, country),
            'lat': lat,
            'lon': lon,
            'n_samples': len(subset),
            **dim_values
        })
    
    result_df = pd.DataFrame(results)
    print(f'  国家数: {len(result_df)}')
    return result_df

def plot_world_map_with_dimensions(country_stats, proto_info):
    """绘制7维度世界地图可视化"""
    print('[Plot] 生成7维度世界地图...')
    
    # 创建 2x4 子图布局 (7维度 + 1图例)
    fig, axes = plt.subplots(4, 2, figsize=(24, 20))
    axes = axes.flatten()
    
    # 更简洁的维度名称
    dim_display = {
        '地区/地理': '① 地理分布',
        '语言': '② 语言一致性',
        '价值观': '③ 价值取向',
        '社会规范': '④ 社会规范',
        '关系结构': '⑤ 关系模式',
        '宗教/传统': '⑥ 宗教虔诚',
        '社会经济': '⑦ 社会经济',
    }
    
    for idx, (dim_name, dim_config) in enumerate(DIM_MAP.items()):
        ax = axes[idx]
        
        # 过滤有数据的国家
        valid = country_stats.dropna(subset=[dim_name])
        valid = valid[valid['lat'].notna() & valid['lon'].notna()]
        
        if len(valid) < 5:
            ax.text(0.5, 0.5, f'{dim_display[dim_name]}\n(数据不足)', 
                    ha='center', va='center', fontsize=14, 
                    fontproperties=CJK_FONT, transform=ax.transAxes)
            continue
        
        # 绘制世界地图底图 (简化版: 经纬度散点)
        # 用浅灰色背景作为"世界地图"的简化表示
        ax.set_facecolor('#E8F4FD')
        
        # 绘制国家点
        vmin = valid[dim_name].quantile(0.05)
        vmax = valid[dim_name].quantile(0.95)
        
        sc = ax.scatter(
            valid['lon'], valid['lat'],
            c=valid[dim_name],
            cmap=dim_config['cmap'],
            s=valid['n_samples'] * 0.5 + 50,  # 点大小与样本数成正比
            alpha=0.8,
            edgecolors='white',
            linewidth=0.5,
            vmin=vmin,
            vmax=vmax,
            zorder=3
        )
        
        # 添加国家标签
        for _, row in valid.iterrows():
            if row['n_samples'] > 200:  # 只标注样本数大的国家
                ax.annotate(
                    row['country'],
                    (row['lon'], row['lat']),
                    fontsize=6,
                    ha='center',
                    va='bottom',
                    xytext=(0, 4),
                    textcoords='offset points',
                    alpha=0.7
                )
        
        # 设置坐标轴范围
        ax.set_xlim(-180, 180)
        ax.set_ylim(-80, 80)
        
        # 设置背景网格
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        # 添加标题
        ax.set_title(
            f'{dim_display[dim_name]}\n{dim_config["label"]}',
            fontproperties=CJK_FONT if CJK_FONT else None,
            fontsize=13,
            fontweight='bold',
            pad=10
        )
        
        # 添加颜色条
        cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('维度得分', fontproperties=CJK_FONT if CJK_FONT else None, fontsize=9)
    
    # 最后一个子图: 图例和说明
    ax_legend = axes[7]
    ax_legend.set_facecolor('#FAFAFA')
    ax_legend.axis('off')
    
    # 图例内容
    legend_text = """
多元文化画像: 7维度特征说明
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① 地理分布: 城市化程度、城镇规模
② 语言一致性: 家庭语言 vs 官方语言
③ 价值取向: 世俗/宗教、个体/集体、信任
④ 社会规范: 信任半径、伦理弹性、工作伦理
⑤ 关系模式: 家庭结构、组织参与、社会距离
⑥ 宗教虔诚: 上帝重要性、宗教实践
⑦ 社会经济: 教育、收入、GDP、HDI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
点大小 = 样本数
颜色深浅 = 维度得分

数据来源: WVS Wave 7 (97,220 × 66国)
    """
    
    ax_legend.text(
        0.1, 0.9, legend_text,
        transform=ax_legend.transAxes,
        fontsize=10,
        verticalalignment='top',
        fontfamily=CJK_FONT.get_name() if CJK_FONT else 'DejaVu Sans',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='gray')
    )
    
    # 调整布局
    plt.suptitle(
        '世界文化画像地图: 7维度国家差异',
        fontproperties=CJK_FONT if CJK_FONT else None,
        fontsize=20,
        fontweight='bold',
        y=0.98
    )
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(
        os.path.join(RES, 'fig7_world_map_7dimensions.png'),
        dpi=150,
        bbox_inches='tight',
        facecolor='white'
    )
    plt.close()
    print(f'  已保存: fig7_world_map_7dimensions.png')

def plot_single_dimension_maps(country_stats):
    """为每个维度单独生成大图,便于阅读"""
    print('[Plot] 生成各维度独立地图...')
    
    dim_display = {
        '地区/地理': '地理分布',
        '语言': '语言一致性',
        '价值观': '价值取向',
        '社会规范': '社会规范',
        '关系结构': '关系模式',
        '宗教/传统': '宗教虔诚',
        '社会经济': '社会经济',
    }
    
    for dim_name, dim_config in DIM_MAP.items():
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        
        valid = country_stats.dropna(subset=[dim_name])
        valid = valid[valid['lat'].notna() & valid['lon'].notna()]
        
        ax.set_facecolor('#E8F4FD')
        
        vmin = valid[dim_name].quantile(0.05)
        vmax = valid[dim_name].quantile(0.95)
        
        sc = ax.scatter(
            valid['lon'], valid['lat'],
            c=valid[dim_name],
            cmap=dim_config['cmap'],
            s=valid['n_samples'] * 1.0 + 100,
            alpha=0.85,
            edgecolors='white',
            linewidth=0.8,
            vmin=vmin,
            vmax=vmax,
            zorder=3
        )
        
        # 添加所有国家标签
        for _, row in valid.iterrows():
            offset_y = 0
            if row['lat'] > 30:
                offset_y = 8
            elif row['lat'] < -30:
                offset_y = -12
                
            ax.annotate(
                f"{row['country']}",
                (row['lon'], row['lat']),
                fontsize=7,
                ha='center',
                va='bottom',
                xytext=(0, offset_y + 5),
                textcoords='offset points',
                fontweight='bold',
                alpha=0.8
            )
        
        ax.set_xlim(-180, 180)
        ax.set_ylim(-80, 80)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        
        ax.set_title(
            f'世界文化画像地图: {dim_display[dim_name]}',
            fontproperties=CJK_FONT if CJK_FONT else None,
            fontsize=16,
            fontweight='bold',
            pad=15
        )
        
        ax.set_xlabel('经度', fontproperties=CJK_FONT if CJK_FONT else None, fontsize=12)
        ax.set_ylabel('纬度', fontproperties=CJK_FONT if CJK_FONT else None, fontsize=12)
        
        cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('维度得分 (标准化)', fontproperties=CJK_FONT if CJK_FONT else None, fontsize=11)
        
        plt.tight_layout()
        safe_name = dim_name.replace('/', '_').replace(' ', '_')
        plt.savefig(
            os.path.join(RES, f'fig7_{safe_name}_map.png'),
            dpi=150,
            bbox_inches='tight',
            facecolor='white'
        )
        plt.close()
        print(f'  已保存: fig7_{safe_name}_map.png')

def plot_dimension_radar_by_country(country_stats):
    """为关键国家绘制7维度雷达图"""
    print('[Plot] 生成关键国家雷达图...')
    
    # 选择关键国家
    key_countries = ['CHN', 'JPN', 'KOR', 'USA', 'GBR', 'DEU', 'FRA', 'IND', 'BRA', 'ZAF']
    
    valid_countries = [c for c in key_countries if c in country_stats['country'].values]
    
    fig, ax = plt.subplots(figsize=(14, 10), subplot_kw=dict(polar=True))
    
    dim_names = list(DIM_MAP.keys())
    dim_labels = [DIM_MAP[d]['label'] for d in dim_names]
    angles = np.linspace(0, 2 * np.pi, len(dim_names), endpoint=False).tolist()
    angles += angles[:1]
    
    # 归一化各维度到 0-1
    norm_stats = country_stats.copy()
    for dim in dim_names:
        dmin = norm_stats[dim].min()
        dmax = norm_stats[dim].max()
        if dmax - dmin > 1e-9:
            norm_stats[dim] = (norm_stats[dim] - dmin) / (dmax - dmin)
        else:
            norm_stats[dim] = 0.5
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(valid_countries)))
    
    for idx, country in enumerate(valid_countries):
        row = norm_stats[norm_stats['country'] == country].iloc[0]
        values = [row[d] for d in dim_names]
        values += values[:1]
        
        label = f"{country}({COUNTRY_CN.get(country, country)})"
        ax.plot(angles, values, 'o-', linewidth=2, markersize=6, 
                label=label, color=colors[idx], alpha=0.8)
        ax.fill(angles, values, alpha=0.1, color=colors[idx])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dim_labels, fontproperties=CJK_FONT if CJK_FONT else None, fontsize=11)
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
    ax.grid(True, alpha=0.3)
    
    ax.set_title(
        '关键国家7维度文化画像雷达图',
        fontproperties=CJK_FONT if CJK_FONT else None,
        fontsize=16,
        fontweight='bold',
        pad=20
    )
    
    ax.legend(
        loc='upper right', bbox_to_anchor=(1.3, 1.1),
        fontsize=10,
        prop={'family': CJK_FONT.get_name() if CJK_FONT else 'DejaVu Sans'}
    )
    
    plt.tight_layout()
    plt.savefig(
        os.path.join(RES, 'fig7_key_countries_radar.png'),
        dpi=150,
        bbox_inches='tight',
        facecolor='white'
    )
    plt.close()
    print('  已保存: fig7_key_countries_radar.png')

def main():
    import json
    
    # 加载数据
    feat, proto, country_dist = load_data()
    
    # 计算国家级维度统计
    country_stats = compute_country_dimensions(feat)
    
    # 保存统计结果
    country_stats.to_csv(
        os.path.join(RES, 'country_7dimensions.csv'),
        index=False,
        encoding='utf-8-sig'
    )
    print(f'  已保存: country_7dimensions.csv')
    
    # 生成可视化
    plot_world_map_with_dimensions(country_stats, proto)
    plot_single_dimension_maps(country_stats)
    plot_dimension_radar_by_country(country_stats)
    
    print('\n[Done] 7维度世界地图可视化完成!')
    print('生成的文件:')
    print('  - fig7_world_map_7dimensions.png (总览图)')
    print('  - fig7_*.png (各维度独立地图)')
    print('  - fig7_key_countries_radar.png (关键国家雷达图)')

if __name__ == '__main__':
    main()
