import json, pandas as pd
with open('多元文化画像数据集/result/culture_prototypes.json', encoding='utf-8') as f:
    p = json.load(f)
profiles = pd.DataFrame(p['profiles'])
dims = ['SACSECVAL','RESEMAVAL','AUTONOMY','EQUALITY','I_AUTHORITY','I_NATIONALISM','I_DEVOUT','god_importance',
        'trust_foreign','ethical_flexibility','exclusion_index','log_gdp','age','income_level','social_class',
        'org_density','context_flexibility']
for i in range(14):
    print(f'=== P{i} ===')
    for d in dims:
        if d in profiles.columns:
            val = float(profiles.loc[i, d])
            n = int(max(0, min(10, val*10))) if 0<=val<=1 else int(max(0, min(10, val)))
            bar = '█' * n
            print(f'  {d:25s}: {val:6.3f} {bar}')
    print()
