# -*- coding: utf-8 -*-
"""页面6：国家详情面板"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd, numpy as np
import utils
from utils import (render_sidebar, country_summary_filtered, DIMS, D_ORDER, J_ORDER, O_ORDER,
                   name_zh, ZONE_COLOR, ZONES, load_item_meta, load_theory)

st.set_page_config(page_title="国家详情", page_icon="🇨🇳", layout="wide")
st.title("🇨🇳 国家详情面板 Country Profile")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]; kind = ctx["dim_kind"]
cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

all_c = cs.sort_values("name_zh")["country"].tolist()
sel = st.selectbox("选择国家 Select country", all_c,
                   index=all_c.index("CHN") if "CHN" in all_c else 0,
                   format_func=lambda c: f"{name_zh(c)} ({c})")
row = cs[cs.country==sel].iloc[0]

c1,c2,c3 = st.columns(3)
c1.metric("国家 Country", f"{row['name_zh']} ({sel})")
c2.metric("文化圈 Zone", row["zone"])
c3.metric("受访者数 Respondents", f"{int(row['n_resp']):,}")

# 雷达：D + J + O 三层（O 仅当侧边栏选 O 时显示，避免过度拥挤）
order_d, order_j, order_o = D_ORDER, J_ORDER, O_ORDER
dc = [f"dim_{c}" for c in order_d]
jc = [f"dim_{c}" for c in order_j]
oc = [f"dim_{c}" for c in order_o]
lab_d = [f"{utils.fmt_dim(c,'D').split(' ')[0]}\n{c}" for c in order_d]
lab_j = [f"{utils.fmt_dim(c,'J').split(' ')[0]}\n{c}" for c in order_j]
lab_o = [f"{utils.fmt_dim(c,'O').split(' ')[0]}\n{c}" for c in order_o]

fig = go.Figure()
vd = [row[c] for c in dc] + [row[dc[0]]]
fig.add_trace(go.Scatterpolar(r=vd, theta=lab_d+[lab_d[0]], fill='toself',
                             name="场域 Domain D", line=dict(color="#2E5C8A"), opacity=0.55))
vj = [row[c] for c in jc] + [row[jc[0]]]
fig.add_trace(go.Scatterpolar(r=vj, theta=lab_j+[lab_j[0]], fill='toself',
                             name="判断 Judgment J", line=dict(color="#C0504D"), opacity=0.55))
# O 层：仅当侧边栏选择 O 时显示
if kind == "O":
    vo = [row[c] for c in oc] + [row[oc[0]]]
    fig.add_trace(go.Scatterpolar(r=vo, theta=lab_o+[lab_o[0]], fill='toself',
                                 name="对象 Object O", line=dict(color="#3A8FB7"), opacity=0.55))
fig.update_layout(polar=dict(radialaxis=dict(range=[0,1])), template="plotly_white", height=560)
st.plotly_chart(fig, use_container_width=True)
st.caption(f"蓝=8场域 D，红=6判断 J" + ("，青=14对象 O（侧边栏已选 O）" if kind=="O" else "") + "。半径=维度均值(0-1归一化)。")

# Welzel 定位
st.subheader("在文化地图上的位置 Position on cultural map")
fig2 = px.scatter(cs, x="welzel_secular", y="welzel_emanc", color="zone",
                  color_discrete_map=ZONE_COLOR, opacity=0.45, height=480,
                  labels={"welzel_secular":"传统→世俗 Sacred→Secular","welzel_emanc":"生存→自我表达 Survival→Emanc"})
fig2.add_scatter(x=[row["welzel_secular"]], y=[row["welzel_emanc"]], mode="markers+text",
                 text=[f"{row['name_zh']}"], textposition="top center",
                 marker=dict(size=18, color="black", symbol="star"), showlegend=False)
fig2.update_layout(template="plotly_white", xaxis_range=[0.1,0.55], yaxis_range=[0.15,0.75])
st.plotly_chart(fig2, use_container_width=True)

# 维度分值表
st.subheader("维度分值明细 Dimension scores")
both = pd.DataFrame({
    "维度": order_d + order_j + order_o,
    "分值(0-1)": [row[c] for c in dc] + [row[c] for c in jc] + [row[c] for c in oc],
    "类别": ["场域D"]*len(order_d) + ["判断J"]*len(order_j) + ["对象O"]*len(order_o)
})
st.dataframe(both.style.format({"分值(0-1)":"{:.3f}"}), use_container_width=True, hide_index=True)
