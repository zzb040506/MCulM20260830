# -*- coding: utf-8 -*-
"""一次性脚本：从 WVS-7 原始 CSV 抽取 Page 5 所需的列，存为紧凑 parquet。
- 输入：WVS-7数据集/WVS_Cross-National_Wave_7_inverted_csv_v6_0.csv (约 200MB)
- 输出：data/item_raw.parquet  (估计 10-30MB，可入仓库)
- 列：country, sex, age, edu, income, + 290 个题项 wvs_col 原始值
- 行：97,220 名受访者

Page 5 (题项级分布) 原直接读 CSV；改为读 parquet 后：
  - 免去云端部署时携带 200MB CSV
  - 加载速度数十倍提升
  - 行为与原 CSV 读取保持一致（demo 列保留为字符串以匹配原比较逻辑）
"""
import os, sys, csv
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 项目根
WVS_CSV = os.path.join(BASE, "WVS-7数据集", "WVS_Cross-National_Wave_7_inverted_csv_v6_0.csv")

DEMO_COLS = {
    "country": "B_COUNTRY_ALPHA",
    "sex":   "Q260",
    "age":   "Q262",
    "edu":   "Q275R",
    "income":"Q288R",
}

def main():
    print(f"① 读取 item_meta 取得 290 题的 wvs_col ...")
    im = pd.read_parquet(os.path.join(DATA, "item_meta.parquet"))
    item_cols = im["wvs_col"].unique().tolist()
    print(f"   {len(item_cols)} 个 wvs_col")

    print(f"② 抽取 WVS CSV 需要的列 ({len(DEMO_COLS)+len(item_cols)} 列)...")
    need = list(DEMO_COLS.values()) + item_cols
    df = pd.read_csv(WVS_CSV, usecols=lambda c: c in need, low_memory=False)
    print(f"   {df.shape[0]} 行 × {df.shape[1]} 列")

    print(f"③ 题项列数值化，负值→NaN ...")
    for c in item_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
        df.loc[df[c] < 0, c] = np.nan

    print(f"④ 人口学列保留原始字符串（与 Page 5 CSV 行为一致）...")
    # Page 5 把 rec["Q260"] 当字符串用，比较 "1"/"2"；
    # 数值化列保留为字符串形式（CSV 默认即字符串）
    for k, wvs_col in DEMO_COLS.items():
        df = df.rename(columns={wvs_col: k})
    # 把数值化的人口学列转为字符串（保持与 CSV 原行为一致）
    for k in ["sex", "age", "edu", "income"]:
        df[k] = df[k].astype("Int64").astype("string").fillna("")
        # Int64 处理 NaN，再转 string 时 NaN -> <NA>，所以先 fillna
    # country 保留字符串
    df["country"] = df["country"].astype("string").fillna("")

    print(f"⑤ 保存 parquet ...")
    out = os.path.join(DATA, "item_raw.parquet")
    df.to_parquet(out, index=False, compression="zstd")
    size_mb = os.path.getsize(out) / 1024 / 1024
    print(f"   ✅ {out}  ({size_mb:.2f} MB, {df.shape[0]} 行 × {df.shape[1]} 列)")

if __name__ == "__main__":
    main()
