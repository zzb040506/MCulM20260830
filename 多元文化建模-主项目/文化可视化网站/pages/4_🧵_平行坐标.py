# -*- coding: utf-8 -*-
"""页面4：平行坐标图"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import pandas as pd, numpy as np
import utils
from utils import (render_sidebar, country_summary_filtered, DIMS, D_ORDER, J_ORDER,
                   name_zh, ZONES, ZONE_COLOR, ZONE_EN)

st.set_page_config(page_title="平行坐标", page_icon="🧵", layout="wide")
st.title("🧵 平行坐标图 Parallel Coordinates")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]; kind = ctx["dim_kind"]
cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

order = D_ORDER if kind=="D" else J_ORDER
dim_cols = [f"dim_{c}" for c in order]
labels = {dc: utils.fmt_dim(c, kind) for dc, c in zip(dim_cols, order)}

# 文化圈映射为数值色，用各文化圈颜色做 colorscale
zones_present = list(cs["zone"].unique())
cmap = {z: i for i, z in enumerate(zones_present)}
cs2 = cs.assign(zone_id=cs["zone"].map(cmap)).copy()
colorscale = [[i/(max(1,len(zones_present)-1)), ZONE_COLOR[z]] for i, z in enumerate(zones_present)]

fig = px.parallel_coordinates(cs2, dimensions=dim_cols, color="zone_id",
                               color_continuous_scale=colorscale,
                               labels=labels, height=620)
# parallel_coordinates 不支持离散图例，手动加文化圈说明
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)
legend_md = "　".join([f":{''}[{z}]({ZONE_EN[z]})" for z in zones_present])
st.markdown("**文化圈说明**：" + " ｜ ".join([f"{z} / {ZONE_EN[z]}" for z in zones_present]))
st.caption(f"维度集：{DIMS[kind][0]}。每线=一国，沿各维度轴展开；线条聚拢=文化模式相似，发散=差异大。线条颜色按文化圈（颜色条对应上图 zone_id 编号）。")
