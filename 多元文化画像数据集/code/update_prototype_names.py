"""
更新文化原型命名为人文社科理论命名方案。
映射关系:
  P0: 个体表达型 (Individual Expressive)
  P1: 传统-世俗混合型 (Traditional-Secular Mixed)
  P2: 生存焦虑型 (Survival Anxiety)
  P3: 集体团结型 (Collective Solidarity)
  P4: 传统宗教型 (Traditional Religious)
  P5: 世俗理性型 (Secular-Rational)
  P6: 宽容宗教型 (Tolerant Religious)
  P7: 自由理性型 (Liberal-Rational)
  P8: 保守宗教型 (Conservative Religious)
  P9: 积极参与型 (Active Participatory)
  P10: 等级个人主义型 (Hierarchical Individualistic)
  P11: 温和保守型 (Moderate Conservative)
  P12: 封闭虔诚型 (Closed-Devotional)
  P13: 世俗自主型 (Secular-Autonomous)
"""
import os, json, pandas as pd

BASE = '/Users/f.fantasiachopin/Documents/code/Research/Test20260822/多元文化画像数据集'
RES = os.path.join(BASE, 'result')

# 新的理论命名映射
NEW_NAMES = {
    0: '个体表达型',
    1: '传统-世俗混合型',
    2: '生存焦虑型',
    3: '集体团结型',
    4: '传统宗教型',
    5: '世俗理性型',
    6: '宽容宗教型',
    7: '自由理性型',
    8: '保守宗教型',
    9: '积极参与型',
    10: '等级个人主义型',
    11: '温和保守型',
    12: '封闭虔诚型',
    13: '世俗自主型',
}

# 理论依据说明
THEORY_BASIS = {
    0: {
        'cn': '个体表达型',
        'en': 'Individual Expressive',
        'theorists': 'Hofstede (IDV高) + Hall (低语境) + Inglehart (自我表达)',
        'characteristics': '低神圣、低民族主义、高信任、高平等、高语境外弹',
        'countries': 'DEU, GBR, NLD',
    },
    1: {
        'cn': '传统-世俗混合型',
        'en': 'Traditional-Secular Mixed',
        'theorists': 'Hall (高语境) + Triandis (垂直集体主义) + Inglehart (混合价值)',
        'characteristics': '中等神圣、高语境外弹、中等自主、低民族主义',
        'countries': 'JPN',
    },
    2: {
        'cn': '生存焦虑型',
        'en': 'Survival Anxiety',
        'theorists': 'Inglehart (生存价值) + Hall (高语境)',
        'characteristics': '低信任、低理性、低经济、低自主、高语境',
        'countries': 'BRA, ZWE',
    },
    3: {
        'cn': '集体团结型',
        'en': 'Collective Solidarity',
        'theorists': 'Triandis (垂直集体主义) + Inglehart (生存价值)',
        'characteristics': '高组织参与、高经济、低信任、高民族主义、中等神圣',
        'countries': 'TUR, RUS',
    },
    4: {
        'cn': '传统宗教型',
        'en': 'Traditional Religious',
        'theorists': 'Hall (高语境) + Inglehart (传统价值) + Hofstede (高UAI)',
        'characteristics': '高神圣、高民族主义、低信任、高组织、高语境',
        'countries': 'KAZ, IRN',
    },
    5: {
        'cn': '世俗理性型',
        'en': 'Secular-Rational',
        'theorists': 'Inglehart (世俗-理性) + Hall (低语境)',
        'characteristics': '低神圣、高自主、高经济、高语境弹性、中等排他',
        'countries': 'CHN, MNG',
    },
    6: {
        'cn': '宽容宗教型',
        'en': 'Tolerant Religious',
        'theorists': 'Inglehart (传统价值) + Triandis (水平集体主义)',
        'characteristics': '高神圣、高信任、低民族主义、低权威、高经济',
        'countries': 'USA, CAN',
    },
    7: {
        'cn': '自由理性型',
        'en': 'Liberal-Rational',
        'theorists': 'Hofstede (IDV最高) + Hall (低语境) + Inglehart (自我表达)',
        'characteristics': '低神圣、高理性、高信任、高平等、高自主、高经济',
        'countries': 'FRA, SWE',
    },
    8: {
        'cn': '保守宗教型',
        'en': 'Conservative Religious',
        'theorists': 'Hall (高语境) + Inglehart (传统价值)',
        'characteristics': '高神圣、中等信任、中等民族主义、高语境、中等经济',
        'countries': 'USA, CAN',
    },
    9: {
        'cn': '积极参与型',
        'en': 'Active Participatory',
        'theorists': 'Hofstede (IDV中等) + Inglehart (传统-世俗混合)',
        'characteristics': '中等神圣、中等信任、中等民族主义、高组织参与、高经济',
        'countries': 'IDN, PHL',
    },
    10: {
        'cn': '等级个人主义型',
        'en': 'Hierarchical Individualistic',
        'theorists': 'Triandis (垂直个人主义) + Hofstede (IDV高)',
        'characteristics': '高权威服从、高自主、低信任、高民族主义、中等神圣',
        'countries': 'KOR, JPN',
    },
    11: {
        'cn': '温和保守型',
        'en': 'Moderate Conservative',
        'theorists': 'Inglehart (生存价值) + Hall (高语境)',
        'characteristics': '中等信任、中等民族主义、中等神圣、中等理性、中等经济',
        'countries': 'BRA, ZWE',
    },
    12: {
        'cn': '封闭虔诚型',
        'en': 'Closed-Devotional',
        'theorists': 'Inglehart (传统价值) + Hall (高语境) + Hofstede (高UAI)',
        'characteristics': '高神圣、低信任、高民族主义、高组织、高语境、中等经济',
        'countries': 'EGY, PAK',
    },
    13: {
        'cn': '世俗自主型',
        'en': 'Secular-Autonomous',
        'theorists': 'Inglehart (世俗-理性) + Triandis (水平个人主义) + Hall (低语境)',
        'characteristics': '低神圣、高理性、高自主、中等信任、低民族主义、高经济',
        'countries': 'FIN, NOR',
    },
}

# === 1. 更新 culture_prototypes.json ===
print('[Update] 更新文化原型命名...')
with open(os.path.join(RES, 'culture_prototypes.json'), 'r', encoding='utf-8') as f:
    proto_data = json.load(f)

# 更新原型名称
for i, p in enumerate(proto_data['prototypes']):
    old_name = p['name']
    new_name = NEW_NAMES.get(i, old_name)
    p['name'] = new_name
    p['theoretical_basis'] = THEORY_BASIS.get(i, {})
    print(f'  P{i}: {old_name} → {new_name}')

with open(os.path.join(RES, 'culture_prototypes.json'), 'w', encoding='utf-8') as f:
    json.dump(proto_data, f, ensure_ascii=False, indent=2)
print(f'  已保存: culture_prototypes.json')

# === 2. 更新 model.pkl 中的原型名称 ===
import pickle
with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
    model_bundle = pickle.load(f)

model_bundle['prototypes'] = proto_data['prototypes']
with open(os.path.join(RES, 'model.pkl'), 'wb') as f:
    pickle.dump(model_bundle, f)
print('  已更新: model.pkl')

# === 3. 更新 prototype_assignment.parquet ===
print('[Update] 更新个体分配数据...')
assign = pd.read_parquet(os.path.join(RES, 'prototype_assignment.parquet'))

# 更新 main_prototype_name
assign['main_prototype_name'] = assign['main_prototype'].map(NEW_NAMES)

# 更新 P 列名
old_cols = [f'P{i}' for i in range(14)]
new_cols_name = [NEW_NAMES[i] for i in range(14)]
col_mapping = {f'P{i}': f'P{i}' for i in range(14)}  # 保留 P0-P13 列名，便于处理
assign.to_parquet(os.path.join(RES, 'prototype_assignment.parquet'), index=False)
print('  已保存: prototype_assignment.parquet')

# === 4. 更新 country_culture_dist.csv ===
print('[Update] 更新国家级分布数据...')
country_dist = pd.read_csv(os.path.join(RES, 'country_culture_dist.csv'))

# 更新 main_prototype_name
country_dist['main_prototype_name'] = country_dist['main_prototype_id'].map(NEW_NAMES)

country_dist.to_csv(os.path.join(RES, 'country_culture_dist.csv'), index=False, encoding='utf-8-sig')
print('  已保存: country_culture_dist.csv')

# === 5. 打印更新结果 ===
print('\n[Update] 新命名方案总览:')
print('=' * 60)
for i in range(14):
    info = THEORY_BASIS[i]
    print(f"\nP{i}: {info['cn']} ({info['en']})")
    print(f"  理论依据: {info['theorists']}")
    print(f"  核心特征: {info['characteristics']}")
    print(f"  主要国家: {info['countries']}")

print('\n' + '=' * 60)
print('\n[Update] 完成!')
