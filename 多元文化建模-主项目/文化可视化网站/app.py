# -*- coding: utf-8 -*-
"""多元文化建模可视化 — 主入口 / 总览页"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import pandas as pd
from utils import (load_country_summary, load_respondent_dims, load_item_meta,
                   load_theory, render_sidebar, country_summary_filtered, ZONES)

st.set_page_config(page_title="多元文化建模可视化", page_icon="🌐", layout="wide")

st.title("🌐 多元文化建模 · 跨国文化图式可视化")
st.caption("Cross-National Cultural Schema Visualization | WVS-7 66国 · 97,220受访者 · 290题编码体系")

with st.expander("📖 项目说明 About", expanded=False):
    st.markdown("""
本网站用 **WVS 第7波完整数据集**（66国、97220名受访者）对自建的 **290题文化编码方案** 做跨国可视化。
- **文化地图散点**：以 WVS 自带 Welzel 两指数（传统—世俗理性 `SACSECVAL` × 生存—自我表达 `RESEMAVAL`）为轴，复现 Inglehart–Welzel 文化地图。
- **schema 维度对比**：把 290 题按我们自己编码的 **D 场域(8类)** 与 **J 判断(6类)** 聚合（每题先 min-max 归一化再取维度均值），比较各国"文化形状"。
- **题项级**：看单题（如"男性更适合当领导"）如何跨国分布，检验其支撑的中层理论。
- 侧边栏可切换文化圈、维度集，并按性别/年龄/教育/收入切片。
""")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]

cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

# 顶部关键指标
c1,c2,c3,c4 = st.columns(4)
c1.metric("国家数 Countries", len(cs))
c2.metric("受访者 Respondents", f"{int(cs['n_resp'].sum()):,}")
c3.metric("文化圈 Zones", cs['zone'].nunique())
c4.metric("编码题项 Coded items", 290)
st.divider()

# 总览图1：文化地图（Welzel 散点）作为首页亮点
st.subheader("🌍 文化地图 Inglehart–Welzel Cultural Map")
fig = px.scatter(cs, x="welzel_secular", y="welzel_emanc", color="zone",
                 text="country", size="n_resp", size_max=28,
                 hover_name="name_zh",
                 hover_data={"country":True,"n_resp":":,","welzel_secular":":.3f","welzel_emanc":":.3f"},
                 labels={"welzel_secular":"传统→世俗理性 Sacred→Secular",
                         "welzel_emanc":"生存→自我表达 Survival→Emancipative","zone":"文化圈"},
                 color_discrete_map={z:__import__('utils').ZONE_COLOR[z] for z in cs['zone'].unique()},
                 height=560)
fig.update_xaxes(range=[0.1,0.55]); fig.update_yaxes(range=[0.15,0.75])
fig.update_traces(textposition='top center', textfont_size=9)
fig.add_hline(y=0.45, line_dash="dash", line_color="#aaa")
fig.add_vline(x=0.33, line_dash="dash", line_color="#aaa")
fig.update_layout(template="plotly_white", font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)
st.caption("气泡=国家，大小=受访者数，颜色=文化圈。左下=传统/生存；右上=世俗/自我表达。详见「文化地图」页。")

# 总览图2：各文化圈维度均值条形
st.subheader("📊 各文化圈维度均值 Dimension means by cultural zone")
kind = ctx["dim_kind"]
_u = __import__('utils')
dim_cols = [f"dim_{c}" for c in (_u.D_ORDER if kind=="D" else _u.J_ORDER if kind=="J" else _u.O_ORDER)]
zmean = cs.groupby("zone")[dim_cols].mean().reset_index()
zmean = zmean.melt(id_vars="zone", var_name="dim", value_name="score")
zmean["dim"] = zmean["dim"].str.replace("dim_","")
fig2 = px.bar(zmean, x="dim", y="score", color="zone", barmode="group",
              labels={"score":"维度均值(0-1, 已归一化)","dim":"维度","zone":"文化圈"},
              height=420)
fig2.update_layout(template="plotly_white", xaxis_tickangle=-30)
st.plotly_chart(fig2, use_container_width=True)
st.caption(f"维度集：{_u.DIMS[kind][0]}。可于侧边栏切换 D/J/O。")

st.divider()
st.markdown("**下一步**：从左侧导航选择页面，深入查看 文化地图 / 雷达对比 / 热力图 / 平行坐标 / 题项级 / 国家详情 / 编码体系。")
