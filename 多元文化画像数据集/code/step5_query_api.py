"""
Step 5 (v2): 文化指纹查询 API - 14 原型
输出: result/sample_fingerprints.json
"""
import os
import sys
import json
import pickle
import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from country_names import COUNTRY_CN

RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'result')


class CultureFingerprintAPI:
    """文化指纹查询 API(14 原型)。"""

    def __init__(self):
        with open(os.path.join(RES, 'model.pkl'), 'rb') as f:
            bundle = pickle.load(f)
        self.scaler = bundle['scaler']
        self.gmm = bundle['gmm']
        self.feat_cols = bundle['feat_cols']
        self.prototypes = bundle['prototypes']
        self.n_proto = self.gmm.n_components
        self.proto_names = [p['name'] for p in self.prototypes]

        self.feat_df = pd.read_parquet(os.path.join(RES, 'culture_features.parquet'))
        self.country = self.feat_df['B_COUNTRY_ALPHA']
        self.country_median = {}
        for c in self.country.unique():
            mask = self.country == c
            self.country_median[c] = self.feat_df.loc[mask, self.feat_cols].median()

    def _build_feature_vector(self, user_input):
        country = user_input.get('country', 'CHN')
        base = self.country_median.get(country, self.feat_df[self.feat_cols].median()).copy()
        overrides = {
            'sex': user_input.get('sex'),
            'age': user_input.get('age'),
            'edu_isced': user_input.get('edu_isced'),
            'social_class': user_input.get('social_class'),
            'income_level': (user_input.get('income_level') / 10
                              if user_input.get('income_level') is not None else None),
            'urban': user_input.get('urban'),
        }
        for k, v in overrides.items():
            if v is not None and k in base.index:
                base[k] = v
        return base[self.feat_cols].values.astype(float).reshape(1, -1)

    def query(self, user_input):
        x = self._build_feature_vector(user_input)
        x_scaled = self.scaler.transform(x)
        probs = self.gmm.predict_proba(x_scaled)[0]
        main_p = int(np.argmax(probs))

        # 14 原型分布(只保留 >=5%)
        proto_dist = {}
        for i in range(self.n_proto):
            if probs[i] >= 0.05:
                proto_dist[f'P{i}_{self.proto_names[i]}'] = round(float(probs[i]), 4)

        # 价值向量
        value_dims = ['SACSECVAL', 'RESEMAVAL', 'AUTONOMY', 'EQUALITY', 'I_AUTHORITY',
                      'I_NATIONALISM', 'I_DEVOUT', 'trust_foreign', 'ethical_flexibility',
                      'exclusion_index', 'context_flexibility']
        trust_dims = {'trust_foreign', 'trust_general', 'trust_family'}
        value_vector = {}
        for d in value_dims:
            if d in self.feat_cols:
                idx = self.feat_cols.index(d)
                raw = float(x[0, idx])
                if d in trust_dims:
                    value_vector[d] = round(max(0, min(1, (4 - raw) / 3)), 4)
                else:
                    value_vector[d] = round(raw, 4)

        # 最近邻国家(基于 14 原型分布的 JS 距离)
        country_dist = pd.read_csv(os.path.join(RES, 'country_culture_dist.csv'))
        p_cols = [f'P{i}' for i in range(self.n_proto)]
        user_dist = probs

        def js_div(p, q):
            p = np.asarray(p, dtype=float) + 1e-10
            q = np.asarray(q, dtype=float) + 1e-10
            p, q = p / p.sum(), q / q.sum()
            m = 0.5 * (p + q)
            return 0.5 * np.sum(p * np.log2(p / m)) + 0.5 * np.sum(q * np.log2(q / m))

        dists = []
        for _, row in country_dist.iterrows():
            cd = row[p_cols].values.astype(float)
            dists.append((row['country'], row.get('country_cn', row['country']), js_div(user_dist, cd)))
        dists.sort(key=lambda x: x[2])
        nearest = [f'{c}({cn})' for c, cn, _ in dists[:5]]

        return {
            'input': user_input,
            'prototype_distribution': proto_dist,
            'main_prototype': {'id': main_p, 'name': self.proto_names[main_p]},
            'main_prototype_prob': round(float(probs[main_p]), 4),
            'value_vector': value_vector,
            'nearest_neighbors': nearest,
            'adaptation_advice': self._adaptation_advice(value_vector),
        }

    def _adaptation_advice(self, vv):
        advice = []
        auth = vv.get('I_AUTHORITY', 0.5)
        if auth > 0.6:
            advice.append('权力距离(高): 礼貌、间接、尊重层级')
        elif auth < 0.4:
            advice.append('权力距离(低): 直接、平等、可挑战性')
        trust_f = vv.get('trust_foreign', 0.5)
        if trust_f > 0.6:
            advice.append('开放度(高): 可用跨文化例子')
        elif trust_f < 0.4:
            advice.append('开放度(低): 用本地化例子')
        eth = vv.get('ethical_flexibility', 0.5)
        if eth > 0.6:
            advice.append('伦理弹性(高): 灵活、情境化')
        elif eth < 0.4:
            advice.append('伦理弹性(低): 严格规则、明确边界')
        return advice


def main():
    print('[Step5] 加载文化指纹 API(14 原型)...', flush=True)
    api = CultureFingerprintAPI()
    print(f'  模型已加载: {api.n_proto} 个原型', flush=True)

    samples = [
        {'country': 'CHN', 'sex': 1, 'age': 28, 'edu_isced': 5, 'income_level': 7, 'urban': 1},
        {'country': 'JPN', 'sex': 2, 'age': 45, 'edu_isced': 4, 'income_level': 6},
        {'country': 'EGY', 'sex': 1, 'age': 35, 'edu_isced': 3, 'income_level': 4},
        {'country': 'DEU', 'sex': 2, 'age': 32, 'edu_isced': 5, 'income_level': 7},
    ]

    results = []
    print('\n=== 文化指纹查询示例 ===', flush=True)
    for s in samples:
        fp = api.query(s)
        results.append(fp)
        print(f"\n--- {s['country']}({COUNTRY_CN.get(s['country'])}) {s.get('sex','?')} {s.get('age','?')}岁 ---", flush=True)
        print(f"  主原型: P{fp['main_prototype']['id']} {fp['main_prototype']['name']} ({fp['main_prototype_prob']:.1%})", flush=True)
        print(f"  14原型分布: " + ' '.join(f'{k}={v:.0%}' for k, v in fp['prototype_distribution'].items()), flush=True)
        print(f"  价值向量: SACSECVAL={fp['value_vector'].get('SACSECVAL',0):.2f} AUTONOMY={fp['value_vector'].get('AUTONOMY',0):.2f}", flush=True)
        print(f"  最近邻: {fp['nearest_neighbors']}", flush=True)

    out = os.path.join(RES, 'sample_fingerprints.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'\n[Step5] 示例指纹已保存: {out}', flush=True)


if __name__ == '__main__':
    main()
