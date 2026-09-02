"""
Step 7: 七维度 WVS 原始维度统计表
依据《多元文化画像构建方案V2.md》第二节“七维度变量映射表”枚举的 WVS 原始变量,
对 CSV 原始数据(不做 0-1 归一 / log 变换 / 特征工程)计算描述统计,保留 WVS 原始取值。

输出:
  - result/七维度WVS原始维度统计表.csv
  - md/七维度WVS原始维度统计表.md
"""
import json
import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, '..', 'WVS_Cross-National_Wave_7_inverted_csv_v6_0.csv')
CODEBOOK_JSON = os.path.join(BASE, 'codebook_variables.json')
OUT_CSV = os.path.join(BASE, 'result', '七维度WVS原始维度统计表.csv')
OUT_MD = os.path.join(BASE, 'md', '七维度WVS原始维度统计表.md')

# WVS 标准缺失码(负数即缺失)
MISSING_NEGATIVE = True

# 纯“分类/编码”变量(数值型但无均值意义),仅报告 N、类别数、众数
CATEGORICAL = {
    'B_COUNTRY_ALPHA', 'B_COUNTRY', 'N_REGION_ISO', 'N_REGION_WVS', 'N_REGION_NUTS2',
    'H_SETTLEMENT', 'G_TOWNSIZE', 'G_TOWNSIZE2',
    'S_INTLANGUAGE', 'LNGE_ISO', 'Q272',
    'Q266', 'Q267', 'Q268',
    'Q275A', 'Q281', 'Q282', 'Q283', 'Q284',
    'Q289', 'Q290',
}

# 国家级指标(个体内为常数)
COUNTRY_LEVEL = {'GDPpercap1', 'GDPpercap2', 'giniWB', 'hdi', 'internetusers'}


def load_codebook():
    with open(CODEBOOK_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    mapping = {}
    for section, items in data.items():
        for it in items:
            mapping[it['var']] = it.get('label', '')
    return mapping


# (子维度中文, 变量名) 列表,严格对应 V2.md 第二节七维度表格
DIMENSIONS = [
    ("维度1 地区/地理", [
        ("国家(ISO-3)", "B_COUNTRY_ALPHA"),
        ("国家(数字)", "B_COUNTRY"),
        ("国内区域 ISO", "N_REGION_ISO"),
        ("国内区域 WVS", "N_REGION_WVS"),
        ("NUTS-2 区域", "N_REGION_NUTS2"),
        ("城乡", "H_URBRURAL"),
        ("城镇规模", "G_TOWNSIZE"),
        ("城镇规模(5组)", "G_TOWNSIZE2"),
        ("定居点类型", "H_SETTLEMENT"),
        ("经度", "O1_LONGITUDE"),
        ("纬度", "O2_LATITUDE"),
    ]),
    ("维度2 语言", [
        ("访谈语言", "S_INTLANGUAGE"),
        ("访谈语言 ISO", "LNGE_ISO"),
        ("家庭语言", "Q272"),
    ]),
    ("维度3 价值观", [
        ("世俗-传统(主轴)", "SACSECVAL"),
        ("生存-自我表达(主轴)", "RESEMAVAL"),
        ("权威服从", "I_AUTHORITY"),
        ("民族主义", "I_NATIONALISM"),
        ("虔诚度", "I_DEVOUT"),
        ("自主性(合成)", "AUTONOMY"),
        ("平等观(合成)", "EQUALITY"),
        ("选择自由(合成)", "CHOICE"),
        ("发声倾向(合成)", "VOICE"),
        ("认识论怀疑", "DEFIANCE"),
        ("不信教", "DISBELIEF"),
        ("相对主义", "RELATIVISM"),
        ("怀疑主义", "SCEPTICISM"),
        ("信任军队", "I_TRUSTARMY"),
        ("信任警察", "I_TRUSTPOLICE"),
        ("信任法院", "I_TRUSTCOURTS"),
        ("规范1", "I_NORM1"),
        ("规范2", "I_NORM2"),
        ("规范3", "I_NORM3"),
        ("后物质主义12项", "Y001"),
        ("后物质主义4项", "Y002"),
        ("自主指数", "Y003"),
    ]),
    ("维度4 社会规范", [
        ("信任半径-通用信任", "Q57P"),
        ("信任半径-信任家人", "Q58P"),
        ("信任半径-信任邻里", "Q59P"),
        ("信任半径-信任熟人", "Q60P"),
        ("信任半径-信任陌生人", "Q61P"),
        ("信任半径-信任异教徒", "Q62P"),
        ("信任半径-信任外国人", "Q63P"),
        ("机构信任-宗教组织", "Q64P"),
        ("机构信任-军队", "Q65P"),
        ("机构信任-报刊", "Q66P"),
        ("机构信任-电视", "Q67P"),
        ("机构信任-工会", "Q68P"),
        ("机构信任-警察", "Q69P"),
        ("机构信任-法院", "Q70P"),
        ("机构信任-政府", "Q71P"),
        ("机构信任-政党", "Q72P"),
        ("机构信任-议会", "Q73P"),
        ("机构信任-公务员", "Q74P"),
        ("机构信任-大学", "Q75P"),
        ("机构信任-选举", "Q76P"),
        ("机构信任-大企业", "Q77P"),
        ("机构信任-银行", "Q78P"),
        ("机构信任-环保运动", "Q79P"),
        ("机构信任-妇女运动", "Q80P"),
        ("机构信任-慈善组织", "Q81P"),
        ("机构信任-区域组织", "Q82P"),
        ("机构信任-联合国", "Q83P"),
        ("机构信任-IMF", "Q84P"),
        ("机构信任-ICC", "Q85P"),
        ("机构信任-NATO", "Q86P"),
        ("机构信任-世界银行", "Q87P"),
        ("机构信任-WHO", "Q88P"),
        ("机构信任-WTO", "Q89P"),
        ("伦理弹性-骗福利", "Q177"),
        ("伦理弹性-逃票", "Q178"),
        ("伦理弹性-偷窃", "Q179"),
        ("伦理弹性-逃税", "Q180"),
        ("伦理弹性-受贿", "Q181"),
        ("伦理弹性-同性恋", "Q182"),
        ("伦理弹性-卖淫", "Q183"),
        ("伦理弹性-堕胎", "Q184"),
        ("伦理弹性-离婚", "Q185"),
        ("伦理弹性-婚前性", "Q186"),
        ("伦理弹性-自杀", "Q187"),
        ("伦理弹性-安乐死", "Q188"),
        ("伦理弹性-家暴", "Q189"),
        ("伦理弹性-体罚孩子", "Q190"),
        ("伦理弹性-暴力", "Q191"),
        ("伦理弹性-恐怖主义", "Q192"),
        ("伦理弹性-随便性行为", "Q193"),
        ("伦理弹性-政治暴力", "Q194"),
        ("伦理弹性-死刑", "Q195"),
        ("工作伦理-不工作者变懒", "Q39P"),
        ("工作伦理-工作是社会义务", "Q40P"),
        ("工作伦理-工作优先于闲暇", "Q41P"),
        ("工作伦理-收入平等vs激励", "Q106"),
        ("工作伦理-私有vs国有", "Q107"),
        ("工作伦理-政府vs个人责任", "Q108"),
        ("工作伦理-竞争观", "Q109"),
        ("工作伦理-成功归因", "Q110"),
        ("工作伦理-环境vs增长", "Q111"),
        ("政府权力-公共监控", "Q196P"),
        ("政府权力-监控通讯", "Q197P"),
        ("政府权力-收集信息", "Q198P"),
    ]),
    ("维度5 关系结构", [
        ("家庭结构-婚姻状况", "Q273"),
        ("家庭结构-子女数", "Q274"),
        ("家庭结构-家庭规模", "Q270"),
        ("家庭结构-与父母同住", "Q271"),
        ("家庭结构-家庭重要性", "Q1P"),
        ("家庭结构-朋友重要性", "Q2P"),
        ("家庭结构-闲暇重要性", "Q3P"),
        ("移民背景-本人移民", "Q263"),
        ("移民背景-母亲移民", "Q264"),
        ("移民背景-父亲移民", "Q265"),
        ("移民背景-本人出生国", "Q266"),
        ("移民背景-母亲出生国", "Q267"),
        ("移民背景-父亲出生国", "Q268"),
        ("移民背景-公民身份", "Q269"),
        ("组织参与-宗教组织", "Q94R"),
        ("组织参与-体育组织", "Q95R"),
        ("组织参与-文化教育组织", "Q96R"),
        ("组织参与-工会", "Q97R"),
        ("组织参与-政党", "Q98R"),
        ("组织参与-环保组织", "Q99R"),
        ("组织参与-专业组织", "Q100R"),
        ("组织参与-慈善组织", "Q101R"),
        ("组织参与-消费者组织", "Q102R"),
        ("组织参与-自助组织", "Q103R"),
        ("组织参与-妇女组织", "Q104R"),
        ("组织参与-其他组织", "Q105R"),
        ("地域认同-人权感知", "Q253P"),
        ("地域认同-国家自豪", "Q254P"),
        ("地域认同-认同村镇", "Q255P"),
        ("地域认同-认同地区", "Q256P"),
        ("地域认同-认同国家", "Q257P"),
        ("地域认同-认同大洲", "Q258P"),
        ("地域认同-认同世界", "Q259P"),
        ("儿童品质-礼貌", "Q7P"),
        ("儿童品质-独立", "Q8P"),
        ("儿童品质-勤奋", "Q9P"),
        ("儿童品质-责任感", "Q10P"),
        ("儿童品质-想象力", "Q11P"),
        ("儿童品质-宽容", "Q12P"),
        ("儿童品质-节俭", "Q13P"),
        ("儿童品质-毅力", "Q14P"),
        ("儿童品质-宗教信仰", "Q15P"),
        ("儿童品质-无私", "Q16P"),
        ("儿童品质-服从", "Q17P"),
        ("邻里排斥-吸毒者", "Q18P"),
        ("邻里排斥-异族", "Q19P"),
        ("邻里排斥-艾滋病人", "Q20P"),
        ("邻里排斥-移民", "Q21P"),
        ("邻里排斥-同性恋", "Q22P"),
        ("邻里排斥-异教徒", "Q23P"),
        ("邻里排斥-酗酒者", "Q24P"),
        ("邻里排斥-未婚同居者", "Q25P"),
        ("邻里排斥-异语者", "Q26P"),
    ]),
    ("维度6 宗教/传统", [
        ("上帝重要性", "Q164"),
        ("信上帝", "Q165P"),
        ("信来世", "Q166P"),
        ("信地狱", "Q167P"),
        ("信天堂", "Q168P"),
        ("科学宗教冲突时宗教对", "Q169P"),
        ("宗教派别", "Q289"),
        ("宗教服务频率", "Q171P"),
        ("宗教组织信任", "Q64P"),
        ("宗教重要性(指数)", "I_RELIGIMP"),
        ("宗教信仰(指数)", "I_RELIGBEL"),
        ("宗教实践(指数)", "I_RELIGPRAC"),
        ("让父母骄傲", "Q27P"),
    ]),
    ("维度7 社会经济背景", [
        ("性别", "Q260"),
        ("出生年", "Q261"),
        ("年龄", "Q262"),
        ("年龄(6段)", "X003R"),
        ("年龄(3段)", "X003R2"),
        ("教育(ISCED)", "Q275"),
        ("教育(国别版)", "Q275A"),
        ("教育(3组)", "Q275R"),
        ("配偶教育", "Q276"),
        ("配偶教育(3组)", "Q276R"),
        ("父亲教育", "Q278"),
        ("父亲教育(3组)", "Q278R"),
        ("就业状态", "Q279"),
        ("配偶就业", "Q280"),
        ("职业大类", "Q281"),
        ("配偶职业", "Q282"),
        ("父亲职业", "Q283"),
        ("就业部门", "Q284"),
        ("主要收入来源", "Q285"),
        ("家庭储蓄", "Q286"),
        ("社会阶层", "Q287P"),
        ("收入等级", "Q288"),
        ("收入(重编码)", "Q288R"),
        ("种族归属", "Q290"),
        ("国家GDP(现价PPP)", "GDPpercap1"),
        ("国家GDP(不变价PPP)", "GDPpercap2"),
        ("国家Gini", "giniWB"),
        ("国家HDI", "hdi"),
        ("互联网普及率", "internetusers"),
    ]),
]


def compute_stats(df, col):
    """返回 (n_valid, n_missing, n_unique, mean, std, min, max, top3, is_categorical)"""
    raw = df[col]
    is_cat = col in CATEGORICAL or (raw.dtype == object)
    if is_cat:
        if raw.dtype == object:
            s = raw.astype('string').str.strip()
            valid = s.dropna()
            valid = valid[valid != '']
        else:
            # 数值型分类/编码变量:负数(-1~-5)视为缺失
            num = pd.to_numeric(raw, errors='coerce')
            valid = num[num >= 0].dropna()
        n_valid = int(valid.size)
        n_missing = int(raw.size - n_valid)
        n_unique = int(valid.nunique())
        top3 = valid.value_counts().head(3)
        top3_str = "; ".join(f"{k}={v}" for k, v in top3.items())
        return n_valid, n_missing, n_unique, np.nan, np.nan, np.nan, np.nan, top3_str, True
    else:
        num = pd.to_numeric(raw, errors='coerce')
        # 负数视为 WVS 缺失码
        mask = num.isna() | (num < 0)
        valid = num[~mask]
        n_valid = int(valid.size)
        n_missing = int(mask.sum())
        n_unique = int(valid.nunique())
        if n_valid == 0:
            return n_valid, n_missing, n_unique, np.nan, np.nan, np.nan, np.nan, "", False
        return (n_valid, n_missing, n_unique,
                float(valid.mean()), float(valid.std(ddof=1)),
                float(valid.min()), float(valid.max()), "", False)


def fmt(x, nd=3):
    if pd.isna(x):
        return "—"
    return f"{x:.{nd}f}"


def main():
    print("[Step7] 读取数据...")
    df = pd.read_csv(CSV, low_memory=False)
    labels = load_codebook()

    rows = []
    missing_cols = []
    for dim, vars_ in DIMENSIONS:
        for sub, var in vars_:
            if var not in df.columns:
                missing_cols.append(var)
                rows.append({
                    '维度': dim, '子维度': sub, '变量': var,
                    'Label': labels.get(var, ''), '类型': '缺失',
                    '有效N': np.nan, '缺失数': np.nan, '缺失率(%)': np.nan,
                    '类别数': np.nan, '均值': np.nan, '标准差': np.nan,
                    '最小值': np.nan, '最大值': np.nan, '众数Top3': '',
                })
                continue
            n_valid, n_missing, n_unique, mean, std, mn, mx, top3, is_cat = compute_stats(df, var)
            if is_cat:
                typ = "分类"
            elif var in COUNTRY_LEVEL:
                typ = "国家级(连续)"
            elif var in {'Q260', 'H_URBRURAL', 'Q271', 'Q263', 'Q264', 'Q265', 'Q269',
                         'Q285', 'Q165P', 'Q166P', 'Q167P', 'Q168P'}:
                typ = "二值"
            else:
                typ = "连续/有序"
            rows.append({
                '维度': dim, '子维度': sub, '变量': var,
                'Label': labels.get(var, ''), '类型': typ,
                '有效N': n_valid, '缺失数': n_missing,
                '缺失率(%)': round(n_missing / df.shape[0] * 100, 3),
                '类别数': n_unique if is_cat else np.nan,
                '均值': mean, '标准差': std, '最小值': mn, '最大值': mx,
                '众数Top3': top3,
            })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_CSV, index=False, encoding='utf-8-sig')
    print(f"[Step7] 已保存 CSV: {OUT_CSV}")
    if missing_cols:
        print(f"[Step7] 警告: CSV 中不存在的变量 {len(missing_cols)} 个: {missing_cols}")

    # 生成 Markdown
    lines = []
    lines.append("# 七维度 WVS 原始维度统计表\n")
    lines.append("> 依据《多元文化画像构建方案V2.md》第二节“七维度变量映射表”枚举的 WVS 原始变量,"
                 "对 CSV 原始数据(不归一化 / 不 log 变换 / 不做特征工程)计算描述统计,保留 WVS 原始取值。\n")
    lines.append("> 缺失处理:负数(-1/-2/-3/-4/-5)与空值均视为缺失;均值/标准差仅对有效值计算。\n")
    lines.append(f"> 样本总量: **{df.shape[0]:,}** 人。\n")

    cur_dim = None
    for _, r in out.iterrows():
        if r['维度'] != cur_dim:
            cur_dim = r['维度']
            lines.append("")
            lines.append(f"## {cur_dim}\n")
            lines.append("")
            lines.append("| 子维度 | 变量 | Label(codebook 原文) | 类型 | 有效N | 均值 | 标准差 | 最小值 | 最大值 | 缺失率(%) |")
            lines.append("|---|---|---|---|---|---|---|---|---|---|")
        n_cell = f"{int(r['有效N']):,}" if pd.notna(r['有效N']) else "—"
        if r['类型'] in ('分类', '缺失'):
            mean_cell = fmt(r['均值'])
            std_cell = fmt(r['标准差'])
            mn_cell = fmt(r['最小值'])
            mx_cell = fmt(r['最大值'])
            if r['类型'] == '分类':
                note = f"类别数={int(r['类别数'])}" if pd.notna(r['类别数']) else ""
                if r['众数Top3']:
                    note += f"; 众数({r['众数Top3']})"
                mean_cell = note if note else "—"
                std_cell, mn_cell, mx_cell = "—", "—", "—"
            lines.append(
                f"| {r['子维度']} | `{r['变量']}` | {r['Label']} | {r['类型']} | "
                f"{n_cell} | {mean_cell} | {std_cell} | {mn_cell} | {mx_cell} | {fmt(r['缺失率(%)'], 2)} |"
            )
        else:
            lines.append(
                f"| {r['子维度']} | `{r['变量']}` | {r['Label']} | {r['类型']} | "
                f"{n_cell} | {fmt(r['均值'])} | {fmt(r['标准差'])} | "
                f"{fmt(r['最小值'])} | {fmt(r['最大值'])} | {fmt(r['缺失率(%)'], 2)} |"
            )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*统计表生成于 2026-08-24,基于 WVS Wave 7 v6.0 原始 CSV 数据。*")

    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"[Step7] 已保存 Markdown: {OUT_MD}")
    print(f"[Step7] 共 {len(out)} 个变量,分布于 {out['维度'].nunique()} 个维度。")


if __name__ == '__main__':
    main()
