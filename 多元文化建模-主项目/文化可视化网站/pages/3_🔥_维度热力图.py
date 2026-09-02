# -*- coding: utf-8 -*-
"""页面3：国家×维度热力图"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import pandas as pd, numpy as np
import utils
from utils import (render_sidebar, country_summary_filtered, DIMS, D_ORDER, J_ORDER, O_ORDER,
                   name_zh, ZONES, ZONE_COLOR)

st.set_page_config(page_title="维度热力图", page_icon="🔥", layout="wide")
st.title("🔥 国家 × 维度 热力图 Country × Dimension Heatmap")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]; kind = ctx["dim_kind"]
cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

order = D_ORDER if kind=="D" else J_ORDER if kind=="J" else O_ORDER
dim_cols = [f"dim_{c}" for c in order]
labels = [utils.fmt_dim(c, kind) for c in order]

sortby = st.radio("国家排序 Sort countries by",
                  ["文化圈 by zone","维度均值 by mean score","名称 by name"], horizontal=True)
if sortby=="文化圈":
    cs = cs.sort_values(["zone","name_zh"])
elif sortby=="维度均值":
    cs = cs.sort_values(dim_cols, key=lambda df: df.mean(axis=1), ascending=False)
else:
    cs = cs.sort_values("name_zh")

mat = cs.set_index("name_zh")[dim_cols]
mat.columns = labels

fig = px.imshow(mat.values, x=labels, y=list(mat.index),
                color_continuous_scale="RdYlBu_r", aspect="auto",
                labels=dict(x="维度 Dimension", y="国家 Country", color="分值(0-1)"),
                height=max(500, len(cs)*16))
fig.update_xaxes(side="top", tickangle=-25)
# 标注数值
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat.iloc[i,j]
        fig.add_annotation(x=j, y=i, text=f"{v:.2f}", showarrow=False,
                           font=dict(size=7.5, color="white" if v>0.6 or v<0.35 else "#333"))
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)
st.caption(f"维度集：{DIMS[kind][0]}。行=国家，列=维度，色=分值(红高蓝低)。可见哪些国家在哪类文化命题上偏强/弱。")

# 文化圈均值热力
st.divider()
st.subheader("文化圈 × 维度 均值热力图")
zmean = cs.groupby("zone")[dim_cols].mean()
zmean.columns = labels
fig2 = px.imshow(zmean.values, x=labels, y=list(zmean.index),
                 color_continuous_scale="RdYlBu_r", aspect="auto",
                 labels=dict(x="维度", y="文化圈", color="均值"),
                 height=320)
for i in range(zmean.shape[0]):
    for j in range(zmean.shape[1]):
        v = zmean.iloc[i,j]
        fig2.add_annotation(x=j, y=i, text=f"{v:.2f}", showarrow=False,
                            font=dict(size=10, color="white" if v>0.55 or v<0.35 else "#333"))
fig2.update_layout(template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)
