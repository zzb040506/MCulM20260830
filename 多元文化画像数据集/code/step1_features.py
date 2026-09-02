"""
Step 1: 数据清洗 + 七维文化特征构造
输入: WVS_Cross-National_Wave_7_inverted_csv_v6_0.csv (97,220 × 611)
输出: result/culture_features.parquet (97,220 × 91 数值特征 + 元信息)
"""
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, '..', 'WVS_Cross-National_Wave_7_inverted_csv_v6_0.csv')
OUT = os.path.join(BASE, 'result')
os.makedirs(OUT, exist_ok=True)

MISSING_CODES = [-1, -2, -3, -4, -5]


def main():
    print('[Step1] 读取 WVS 数据...')
    df = pd.read_csv(CSV, low_memory=False)
    print(f'  原始数据: {df.shape[0]} 行 × {df.shape[1]} 列')

    # === 缺失码统一处理 ===
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].where(~df[num_cols].isin(MISSING_CODES))
    print(f'  缺失码 -1/-2/-3/-4/-5 已转为 NaN')

    meta = df[['B_COUNTRY_ALPHA', 'A_YEAR', 'W_WEIGHT', 'S018']].copy()

    features = pd.DataFrame(index=df.index)

    # ============================================================
    # 维度 1: 地区 / 地理 (~8 维)
    # ============================================================
    features['urban'] = (df['H_URBRURAL'] == 1).astype(int)  # 1=城市
    townsize = pd.to_numeric(df['G_TOWNSIZE'], errors='coerce')
    features['townsize'] = townsize  # ordinal
    features['longitude'] = pd.to_numeric(df['O1_LONGITUDE'], errors='coerce')
    features['latitude'] = pd.to_numeric(df['O2_LATITUDE'], errors='coerce')
    # 国家编码(数值,后续 embedding 用)
    features['country_code'] = pd.to_numeric(df['B_COUNTRY'], errors='coerce')

    # ============================================================
    # 维度 2: 语言 (~3 维)
    # ============================================================
    # 家庭语言与访谈语言是否一致
    features['lang_home_eq_interview'] = (df['Q272'] == df['S_INTLANGUAGE']).astype(int)
    # 家庭语言缺失则视为不一致
    features.loc[df['Q272'].isna(), 'lang_home_eq_interview'] = np.nan
    # 国家官方语言与家庭语言是否一致(近似:同国家内家庭语言众数)
    home_lang_mode = df.groupby('B_COUNTRY_ALPHA')['Q272'].transform(
        lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan
    )
    features['lang_official_match'] = (df['Q272'] == home_lang_mode).astype(int)
    features.loc[df['Q272'].isna(), 'lang_official_match'] = np.nan

    # ============================================================
    # 维度 3: 价值观 (20 维,均已 0-1 标准化)
    # ============================================================
    value_cols = [
        'SACSECVAL', 'RESEMAVAL',
        'I_AUTHORITY', 'I_NATIONALISM', 'I_DEVOUT',
        'I_TRUSTARMY', 'I_TRUSTPOLICE', 'I_TRUSTCOURTS',
        'I_NORM1', 'I_NORM2', 'I_NORM3',
        'AUTONOMY', 'EQUALITY', 'CHOICE', 'VOICE',
        'DEFIANCE', 'DISBELIEF', 'RELATIVISM', 'SCEPTICISM',
        'Y001', 'Y002', 'Y003'
    ]
    for c in value_cols:
        features[c] = pd.to_numeric(df[c], errors='coerce')

    # ============================================================
    # 维度 4: 社会规范 (~12 维)
    # ============================================================
    # 4.1 信任半径(Q57P-Q63P,0-1)
    trust_map = {
        'trust_general': 'Q57P', 'trust_family': 'Q58P', 'trust_neighbor': 'Q59P',
        'trust_acquaintance': 'Q60P', 'trust_stranger': 'Q61P',
        'trust_other_religion': 'Q62P', 'trust_foreign': 'Q63P'
    }
    for name, col in trust_map.items():
        features[name] = pd.to_numeric(df[col], errors='coerce')
    features['trust_decay'] = features['trust_family'] - features['trust_foreign']

    # 4.2 机构信任均值(Q64P-Q89P)
    inst_cols = [f'Q{c}P' for c in range(64, 90) if f'Q{c}P' in df.columns]
    inst_df = df[inst_cols].apply(pd.to_numeric, errors='coerce')
    features['institutional_trust'] = inst_df.mean(axis=1)

    # 4.3 伦理弹性(Q177-Q195,1-10 量表→0-1)
    just_cols = [f'Q{c}' for c in range(177, 196) if f'Q{c}' in df.columns]
    just_df = df[just_cols].apply(pd.to_numeric, errors='coerce')
    features['ethical_flexibility'] = just_df.mean(axis=1) / 10

    # 4.4 工作伦理(Q39P-Q41P,0-1)
    work_cols = ['Q39P', 'Q40P', 'Q41P']
    work_df = df[work_cols].apply(pd.to_numeric, errors='coerce')
    features['work_ethic'] = work_df.mean(axis=1)

    # 4.5 政府权力接受度(Q196P-Q198P,0-1)
    gov_cols = ['Q196P', 'Q197P', 'Q198P']
    gov_df = df[gov_cols].apply(pd.to_numeric, errors='coerce')
    features['gov_power_acceptance'] = gov_df.mean(axis=1)

    # ============================================================
    # 维度 5: 关系结构 (~14 维)
    # ============================================================
    # 5.1 家庭结构
    features['marital_status'] = pd.to_numeric(df['Q273'], errors='coerce')
    features['n_children'] = pd.to_numeric(df['Q274'], errors='coerce')
    features['household_size'] = pd.to_numeric(df['Q270'], errors='coerce')
    features['live_with_parents'] = pd.to_numeric(df['Q271'], errors='coerce')
    features['family_importance'] = pd.to_numeric(df['Q1P'], errors='coerce')
    features['friend_importance'] = pd.to_numeric(df['Q2P'], errors='coerce')
    features['leisure_importance'] = pd.to_numeric(df['Q3P'], errors='coerce')

    # 5.2 移民背景(0-3 代)
    imm_cols = ['Q263', 'Q264', 'Q265']
    imm_df = df[imm_cols].apply(pd.to_numeric, errors='coerce')
    # Q263-Q265: 1=Yes immigrant, 2=No (按 codebook,1=本人/母/父移民)
    features['immigrant_generations'] = imm_df.apply(lambda x: (x == 1).sum(), axis=1)

    # 5.3 组织参与计数(Q94R-Q105R,1=成员)
    org_cols = [f'Q{c}R' for c in range(94, 106) if f'Q{c}R' in df.columns]
    org_df = df[org_cols].apply(pd.to_numeric, errors='coerce')
    features['org_density'] = org_df.apply(lambda x: (x > 0).sum(), axis=1)

    # 5.4 认同半径(世界认同 - 本地认同)
    features['identity_radius'] = pd.to_numeric(df['Q259P'], errors='coerce') - \
                                  pd.to_numeric(df['Q255P'], errors='coerce')

    # 5.5 自主 vs 服从(儿童品质)
    features['autonomy_vs_obedience'] = (
        pd.to_numeric(df['Q8P'], errors='coerce') +
        pd.to_numeric(df['Q11P'], errors='coerce')
    ) - (
        pd.to_numeric(df['Q7P'], errors='coerce') +
        pd.to_numeric(df['Q17P'], errors='coerce')
    )

    # 5.6 排他性指数(邻里排斥,Q18P-Q26P 均值,越低越排他→反转)
    neighbor_cols = [f'Q{c}P' for c in range(18, 27) if f'Q{c}P' in df.columns]
    neighbor_df = df[neighbor_cols].apply(pd.to_numeric, errors='coerce')
    features['exclusion_index'] = neighbor_df.mean(axis=1)

    # ============================================================
    # 维度 6: 宗教 (~10 维)
    # ============================================================
    features['god_importance'] = pd.to_numeric(df['Q164'], errors='coerce') / 10  # 1-10→0-1
    features['believe_god'] = pd.to_numeric(df['Q165P'], errors='coerce')
    features['believe_afterlife'] = pd.to_numeric(df['Q166P'], errors='coerce')
    features['believe_hell'] = pd.to_numeric(df['Q167P'], errors='coerce')
    features['believe_heaven'] = pd.to_numeric(df['Q168P'], errors='coerce')
    features['service_attendance'] = pd.to_numeric(df['Q171P'], errors='coerce')
    features['church_trust'] = pd.to_numeric(df['Q64P'], errors='coerce')
    features['relig_importance'] = pd.to_numeric(df['I_RELIGIMP'], errors='coerce')
    features['relig_belief'] = pd.to_numeric(df['I_RELIGBEL'], errors='coerce')
    features['relig_practice'] = pd.to_numeric(df['I_RELIGPRAC'], errors='coerce')

    # ============================================================
    # 维度 7: 社会经济 (~14 维)
    # ============================================================
    features['sex'] = pd.to_numeric(df['Q260'], errors='coerce')
    features['age'] = pd.to_numeric(df['Q262'], errors='coerce')
    features['edu_isced'] = pd.to_numeric(df['Q275'], errors='coerce')
    features['edu_3group'] = pd.to_numeric(df['Q275R'], errors='coerce')
    features['employment'] = pd.to_numeric(df['Q279'], errors='coerce')
    features['occupation'] = pd.to_numeric(df['Q281'], errors='coerce')
    features['social_class'] = pd.to_numeric(df['Q287P'], errors='coerce')
    features['income_level'] = pd.to_numeric(df['Q288'], errors='coerce') / 10  # 1-10→0-1
    features['ethnicity'] = pd.to_numeric(df['Q290'], errors='coerce')

    # 国家级指标
    features['log_gdp'] = np.log1p(pd.to_numeric(df['GDPpercap2'], errors='coerce'))
    features['gini'] = pd.to_numeric(df['giniWB'], errors='coerce')
    features['hdi'] = pd.to_numeric(df['hdi'], errors='coerce')
    features['internet_users'] = pd.to_numeric(df['internetusers'], errors='coerce')

    print(f'  构造特征数: {features.shape[1]}')

    # === 缺失插补:国家内中位数 → 全局中位数 ===
    print('[Step1] 缺失插补(国家内中位数 → 全局中位数)...')
    country = df['B_COUNTRY_ALPHA']
    for col in features.columns:
        if features[col].isna().any():
            feat_col = features[col].copy()
            # 国家内中位数
            nat_med = feat_col.groupby(country).transform('median')
            features[col] = feat_col.fillna(nat_med)
            # 全局中位数兜底
            features[col] = features[col].fillna(features[col].median())

    # 性别/二值变量插补后强制取整
    for c in ['sex', 'marital_status', 'employment', 'occupation', 'edu_isced',
              'edu_3group', 'ethnicity', 'live_with_parents']:
        features[c] = features[c].round().clip(lower=0)

    print(f'  插补后缺失数: {features.isna().sum().sum()}')

    # === 情境弹性分数(用于后续分析,这里一并计算)==
    # 工作 vs 家庭 / 家人信任 vs 外国人信任 / 本国政府 vs UN
    ctx = (
        abs(pd.to_numeric(df['Q41P'], errors='coerce') - pd.to_numeric(df['Q1P'], errors='coerce')) +
        abs(pd.to_numeric(df['Q58P'], errors='coerce') - pd.to_numeric(df['Q63P'], errors='coerce')) +
        abs(pd.to_numeric(df['Q71P'], errors='coerce') - pd.to_numeric(df['Q83P'], errors='coerce'))
    ) / 3
    features['context_flexibility'] = ctx.fillna(ctx.median())

    # 保存
    out_features = pd.concat([meta, features], axis=1)
    out_path = os.path.join(OUT, 'culture_features.parquet')
    out_features.to_parquet(out_path, index=False)
    print(f'[Step1] 已保存: {out_path}')
    print(f'  最终形状: {out_features.shape}')
    print(f'  特征列(非元信息): {features.shape[1]} 维')
    print(f'\n[Step1] 维度分布:')
    print(f'  地区 4 + 语言 2 + 价值观 20 + 社会规范 12 + 关系结构 14 + 宗教 10 + 社会经济 13 + 情境弹性 1 = {4+2+20+12+14+10+13+1}')


if __name__ == '__main__':
    main()
