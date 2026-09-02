"""给 14 个文化原型起唯一名字:基类型 + 序号。"""
import os
import sys
import json
import re
import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)

RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')


def rename_prototypes():
    with open(os.path.join(RES, 'culture_prototypes.json'), encoding='utf-8') as f:
        proto = json.load(f)
    profiles = pd.DataFrame(proto['profiles'])
    n = proto['n_prototypes']

    # 从 scores 字段推断原始 base type
    base_types = []
    for p in proto['prototypes']:
        scores = p.get('scores', {})
        base_types.append(max(scores, key=scores.get) if scores else p['name'])

    # 同 base_type 内加序号
    from collections import defaultdict
    counters = defaultdict(int)
    new_names = []
    for i in range(n):
        bt = base_types[i]
        counters[bt] += 1
        # 如果该类型只有一个,不加序号
        total = base_types.count(bt)
        if total == 1:
            new_names.append(bt)
        else:
            new_names.append(f'{bt}{counters[bt]}')

    # 打印 + 显示关键特征
    key_dims = ['SACSECVAL', 'RESEMAVAL', 'AUTONOMY', 'I_AUTHORITY', 'I_NATIONALISM',
                'I_DEVOUT', 'god_importance', 'trust_foreign', 'ethical_flexibility',
                'exclusion_index', 'log_gdp', 'age']
    print('=== 14 原型命名 ===', flush=True)
    for i in range(n):
        size = proto['prototypes'][i]['size']
        pct = proto['prototypes'][i]['pct']
        feat_str = ' '.join(f'{d}={profiles.loc[i,d]:.2f}' for d in key_dims if d in profiles.columns)
        print(f'  P{i}: {new_names[i]:12s} ({size:5d}人, {pct:5.1f}%)  {feat_str}', flush=True)

    # 更新 JSON
    for i in range(n):
        proto['prototypes'][i]['name'] = new_names[i]
    with open(os.path.join(RES, 'culture_prototypes.json'), 'w', encoding='utf-8') as f:
        json.dump(proto, f, ensure_ascii=False, indent=2)
    print('  JSON 已更新', flush=True)

    # 更新 assignment parquet
    assign = pd.read_parquet(os.path.join(RES, 'prototype_assignment.parquet'))
    old_main = assign['main_prototype'].values
    assign['main_prototype_name'] = [new_names[i] for i in old_main]
    assign.to_parquet(os.path.join(RES, 'prototype_assignment.parquet'), index=False)
    print('  Assignment parquet 已更新', flush=True)

    # 更新 model.pkl
    import pickle
    with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
        bundle = pickle.load(f)
    for i in range(n):
        bundle['prototypes'][i]['name'] = new_names[i]
    with open(os.path.join(RES, 'model.pkl'), 'wb') as f:
        pickle.dump(bundle, f)
    print('  Model pkl 已更新', flush=True)


if __name__ == '__main__':
    rename_prototypes()
