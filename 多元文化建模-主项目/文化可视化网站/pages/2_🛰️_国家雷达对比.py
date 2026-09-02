# -*- coding: utf-8 -*-
"""页面2：国家雷达对比 + 小多图矩阵"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd, numpy as np
import utils
from utils import (render_sidebar, country_summary_filtered, DIMS, D_ORDER, J_ORDER, O_ORDER,
                   ZONE_COLOR, name_zh, ZONES)

st.set_page_config(page_title="国家雷达对比", page_icon="🛰️", layout="wide")
st.title("🛰️ 国家文化雷达对比 Country Radar Comparison")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]; kind = ctx["dim_kind"]
cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

order = D_ORDER if kind=="D" else J_ORDER if kind=="J" else O_ORDER
labels = [f"{utils.fmt_dim(c, kind).split(' ')[0]}\n{c}" for c in order]
dim_cols = [f"dim_{c}" for c in order]

st.markdown(f"**维度集**：{DIMS[kind][0]}　|　拖动滑块选国家对比（最多6国）")

all_countries = cs.sort_values("name_zh")["country"].tolist()
default = [c for c in ["CHN","USA","JPN","DEU"] if c in all_countries][:4]
sel = st.multiselect("选择国家 Select countries", all_countries, default=default,
                     format_func=lambda c: f"{name_zh(c)} ({c})", key="radar_sel")
sel = sel[:6]

# --- 雷达对比 ---
if len(sel) >= 1:
    fig = go.Figure()
    for c in sel:
        row = cs[cs.country==c].iloc[0]
        vals = [row[col] for col in dim_cols]
        vals = vals + [vals[0]]
        lab = labels + [labels[0]]
        zone = row["zone"]
        fig.add_trace(go.Scatterpolar(r=vals, theta=lab, fill='toself',
                                      name=f"{name_zh(c)} ({c})", line=dict(color=ZONE_COLOR.get(zone)),
                                      opacity=0.6))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0,1], showticklabels=True)),
                      template="plotly_white", height=560,
                      legend=dict(orientation="h", y=-0.05))
    st.plotly_chart(fig, use_container_width=True)
    st.caption("雷达轴=维度，半径=该维度均值(0-1归一化)。形状越外=该类文化命题越被认可。")
else:
    st.info("请至少选一个国家 / Select at least one country.")

st.divider()

# --- 小多图矩阵 ---
st.subheader("全部国家小多图矩阵 Small multiples (all countries)")
n = len(cs)
ncol = st.slider("每行列数 Cols", 4, 8, 6)
nrow = int(np.ceil(n/ncol))
fig2 = make_subplots(rows=nrow, cols=ncol, specs=[[{"type":"polar"}]*ncol]*nrow,
                     subplot_titles=[f"{name_zh(c)}" for c in cs["country"]])
for i, (_, row) in enumerate(cs.iterrows()):
    r, col = divmod(i, ncol)
    vals = [row[dc] for dc in dim_cols] + [row[dim_cols[0]]]
    lab = labels + [labels[0]]
    zone = row["zone"]
    fig2.add_trace(go.Scatterpolar(r=vals, theta=lab, fill='toself',
                                   line=dict(color=ZONE_COLOR.get(zone), width=1.5),
                                   showlegend=False), row=r+1, col=col+1)
    fig2.update_polars(radialaxis=dict(range=[0,1], showticklabels=False, showgrid=True))
fig2.update_layout(height=220*nrow, template="plotly_white")
st.plotly_chart(fig2, use_container_width=True)
st.caption("鸟瞰66国文化形状差异；同色=同文化圈。注意 D-MC/D-HC 维度题项较少，结果较不稳定。")
