# -*- coding: utf-8 -*-
"""共享工具：数据加载、筛选、维度配置、配色"""
import os, sys
import pandas as pd
import numpy as np
import streamlit as st

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from country_meta import COUNTRIES, ZONES, ZONE_EN, ZONE_COLOR, name_zh, name_en, zone_of

DATA = os.path.join(HERE, "data")

# 维度配置
D_ORDER = ["D-FI","D-CR","D-RS","D-PL","D-WO","D-KT","D-MC","D-HC"]
J_ORDER = ["J-CM","J-AC","J-ER","J-NO","J-RA","J-RI"]
D_ZH = {"D-FI":"家庭 Family","D-CR":"社区 Community","D-RS":"宗教 Religion",
        "D-PL":"政治法律 Polity","D-WO":"市场工作 Work","D-KT":"教育知识 Knowledge",
        "D-MC":"媒介文化 Media","D-HC":"健康身体 Health"}
J_ZH = {"J-CM":"分类 Classify","J-AC":"属性因果 Attribute","J-ER":"评价排序 Evaluate",
        "J-NO":"规范应然 Norm","J-RA":"关系分配 Relate","J-RI":"表征认同 Represent"}
DIMS = {"D": ("制度与生活场域 Domain D", D_ORDER, D_ZH),
        "J": ("判断与关系规则 Judgment J", J_ORDER, J_ZH)}

@st.cache_data
def load_country_summary():
    return pd.read_parquet(os.path.join(DATA, "country_summary.parquet"))

@st.cache_data
def load_respondent_dims():
    return pd.read_parquet(os.path.join(DATA, "respondent_dims.parquet"))

@st.cache_data
def load_item_means():
    return pd.read_parquet(os.path.join(DATA, "item_means.parquet"))

@st.cache_data
def load_item_meta():
    return pd.read_parquet(os.path.join(DATA, "item_meta.parquet"))

@st.cache_data
def load_theory():
    import openpyxl
    BASE = "/Users/f.fantasiachopin/Documents/UCAS博士文件夹/Project/多元文化建模20260830/多元文化建模-主项目"
    wb = openpyxl.load_workbook(os.path.join(BASE, "国家文化知识建模_中层理论注册表.xlsx"), data_only=True)
    ws = wb.active
    h = [c.value for c in ws[1]]
    rows = [dict(zip(h, r)) for r in ws.iter_rows(min_row=2, values_only=True)]
    return pd.DataFrame(rows)

def dim_cols(kind):
    return [f"dim_{c}" for c in (D_ORDER if kind=="D" else J_ORDER)]

def country_summary_filtered(demo):
    """根据人口学筛选返回国家×维度汇总。demo: dict(sex/age/edu/income)。"""
    has_filter = any(demo.get(k) for k in ["sex","age","edu","income"])
    base = load_country_summary().copy()
    name_map = dict(zip(base["country"], base["name_zh"]))
    nameen_map = dict(zip(base["country"], base["name_en"]))
    if not has_filter:
        return base
    rd = load_respondent_dims()
    m = pd.Series(True, index=rd.index)
    if demo.get("sex"):   m &= (rd["sex"]==demo["sex"])
    if demo.get("age"):   m &= (rd["age_group"].astype(str)==demo["age"])
    if demo.get("edu"):   m &= (rd["edu"]==demo["edu"])
    if demo.get("income"):m &= (rd["income"]==demo["income"])
    sub = rd[m]
    cols = ["welzel_secular","welzel_emanc"] + dim_cols("D") + dim_cols("J")
    agg = sub.groupby("country")[cols].mean().reset_index()
    agg["n_resp"] = sub.groupby("country").size().reindex(agg["country"]).values
    agg["name_zh"] = agg["country"].map(name_map)
    agg["name_en"] = agg["country"].map(nameen_map)
    agg["zone"] = agg["country"].map(zone_of)
    return agg

def render_sidebar():
    """渲染侧边栏筛选控件，返回 dict: zones, dim_kind, demo."""
    st.sidebar.markdown("## 🔧 筛选 Filters")
    zones = st.sidebar.multiselect("文化圈 Cultural zone", ZONES, default=ZONES,
                                   format_func=lambda z: f"{z} / {ZONE_EN[z]}")
    dim_kind = st.sidebar.radio("维度集 Dimension set", ["D","J"], format_func=lambda k: DIMS[k][0])
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👤 人口学切片 Demographics")
    demo = {}
    demo["sex"] = st.sidebar.selectbox("性别 Sex", ["", "男 Male", "女 Female"]) or None
    demo["age"] = st.sidebar.selectbox("年龄 Age", ["", "<30","30-44","45-59","60+"]) or None
    demo["edu"] = st.sidebar.selectbox("教育 Education", ["", "低 Low","中 Mid","高 High"]) or None
    demo["income"] = st.sidebar.selectbox("收入 Income", ["", "低 Low","中 Mid","高 High"]) or None
    return {"zones": zones, "dim_kind": dim_kind, "demo": demo}

def filter_countries(df, zones):
    if zones:
        return df[df["zone"].isin(zones)].copy()
    return df.copy()

def fmt_dim(code, kind):
    return DIMS[kind][2].get(code, code)

# 题项文字（中文简化）
@st.cache_data
def question_text(qid):
    im = load_item_meta()
    row = im[im["variable"]==qid]
    if len(row)==0: return ""
    return str(row.iloc[0]["atomic_proposition"])
