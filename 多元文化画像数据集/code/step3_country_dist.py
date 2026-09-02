"""
Step 3 (v2): 国家级文化分布 - 14 原型
输出:
  - result/country_culture_dist.csv (66 国 × 14 原型概率 + 主原型 + 中文名)
  - result/country_culture_dist_top14.csv (按主原型排序的国家列表)
"""
import os
import sys
import json
import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from country_names import COUNTRY_CN

RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')


def main():
    print('[Step3] 读取软分配结果...', flush=True)
    assign = pd.read_parquet(os.path.join(RES, 'prototype_assignment.parquet'))
    with open(os.path.join(RES, 'culture_prototypes.json'), encoding='utf-8') as f:
        proto = json.load(f)

    n_proto = proto['n_prototypes']
    proto_names = [p['name'] for p in proto['prototypes']]
    p_cols = [f'P{i}' for i in range(n_proto)]
    print(f'  个体数: {len(assign)}, 原型数: {n_proto}', flush=True)

    # === 国家级文化分布(加权:S018) ===
    print('[Step3] 计算 14 原型国家级分布...', flush=True)
    w = assign['S018'].fillna(1).values
    w = np.where(w > 0, w, 1)
    country = assign['B_COUNTRY_ALPHA'].values

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
            'main_prototype_name': proto_names[main_p],
            'main_prototype_prob': round(float(dist[main_p]), 4),
            **{p_cols[i]: round(float(dist[i]), 4) for i in range(n_proto)},
        })

    country_dist = pd.DataFrame(dist_rows).sort_values('main_prototype_name')
    out_csv = os.path.join(RES, 'country_culture_dist.csv')
    country_dist.to_csv(out_csv, index=False, encoding='utf-8-sig')
    print(f'  已保存: {out_csv} ({country_dist.shape})', flush=True)

    # === 按主原型分组打印 Top5 国家 ===
    print('\n[Step3] 各原型 Top5 国家:', flush=True)
    for i in range(n_proto):
        col = p_cols[i]
        top = country_dist.nlargest(5, col)[['country', 'country_cn', col, 'n']]
        top_str = ', '.join(f"{r['country']}({r['country_cn']})={r[col]:.2f}" for _, r in top.iterrows())
        print(f'  P{i} {proto_names[i]:12s}: {top_str}', flush=True)

    # 打印代表国家
    print('\n[Step3] 代表国家 14 原型分布:', flush=True)
    for c in ['CHN', 'JPN', 'KOR', 'USA', 'DEU', 'GBR', 'EGY', 'RUS', 'BRA', 'IRN', 'THA', 'NGA']:
        row = country_dist[country_dist['country'] == c]
        if len(row) == 0:
            continue
        r = row.iloc[0]
        dist_str = ' '.join(f'P{i}={r[p_cols[i]]:.2f}' for i in range(n_proto) if r[p_cols[i]] >= 0.05)
        print(f'  {c}({r["country_cn"]}, n={int(r["n"])}): 主={r["main_prototype_name"]}({r["main_prototype_prob"]:.2f}) | {dist_str}', flush=True)

    print(f'\n[Step3] 完成。共 {len(country_dist)} 国, {n_proto} 原型。')


if __name__ == '__main__':
    main()
