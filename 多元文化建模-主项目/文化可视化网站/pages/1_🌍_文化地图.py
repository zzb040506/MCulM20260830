# -*- coding: utf-8 -*-
"""页面1：文化地图 —— Welzel散点 + 世界地图着色"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import pandas as pd
import utils
from utils import (load_country_summary, render_sidebar, country_summary_filtered,
                   ZONE_COLOR, ZONES, ZONE_EN)

st.set_page_config(page_title="文化地图", page_icon="🌍", layout="wide")
st.title("🌍 文化地图 Cultural Map")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]
cs = country_summary_filtered(demo)
cs = cs[cs["zone"].isin(zones)] if zones else cs

metric = st.radio("地图着色维度 Map color metric",
                  ["welzel_secular (传统→世俗)","welzel_emanc (生存→自我表达)"],
                  horizontal=True, label_visibility="collapsed")
col = "welzel_secular" if metric.startswith("welzel_secular") else "welzel_emanc"
mlabel = "传统→世俗 Sacred→Secular" if "secular" in col else "生存→自我表达 Survival→Emancipative"

# --- 左：散点文化地图 ---
st.subheader("Inglehart–Welzel 文化地图散点")
fig = px.scatter(cs, x="welzel_secular", y="welzel_emanc", color="zone",
                 text="country", size="n_resp", size_max=30,
                 hover_name="name_zh",
                 hover_data={"country":True,"n_resp":":,","welzel_secular":":.3f","welzel_emanc":":.3f"},
                 labels={"welzel_secular":"传统→世俗 Sacred→Secular",
                         "welzel_emanc":"生存→自我表达 Survival→Emanc","zone":"文化圈"},
                 color_discrete_map=ZONE_COLOR, height=620)
fig.update_xaxes(range=[0.1,0.55]); fig.update_yaxes(range=[0.15,0.75])
fig.update_traces(textposition='top center', textfont_size=9)
fig.add_hline(y=0.45, line_dash="dash", line_color="#bbb")
fig.add_vline(x=0.33, line_dash="dash", line_color="#bbb")
fig.add_annotation(x=0.52, y=0.72, text="世俗·自我表达<br>Secular·Emancipative", showarrow=False, font=dict(size=10,color="#888"))
fig.add_annotation(x=0.13, y=0.18, text="传统·生存<br>Traditional·Survival", showarrow=False, font=dict(size=10,color="#888"))
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# --- 右/下：世界地图着色 ---
st.subheader(f"世界地图着色：{mlabel}")
fig2 = px.choropleth(cs, locations="country", locationmode="ISO-3",
                     color=col, hover_name="name_zh",
                     hover_data={"country":True,"n_resp":":,","zone":True},
                     color_continuous_scale="RdYlBu_r", range_color=[cs[col].min()-0.02, cs[col].max()+0.02],
                     labels={col:mlabel}, height=540)
fig2.update_layout(template="plotly_white", geo=dict(showcoastlines=True, showland=True, landcolor="#f5f5f5"))
st.plotly_chart(fig2, use_container_width=True)

st.caption("注：Welzel 两指数为 WVS 预计算指标(SACSECVAL/RESEMAVAL，已归一到0-1)。文化圈颜色编码见侧边栏；地图空白国未纳入WVS-7。")

# 文化圈均值表
with st.expander("📋 文化圈 Welzel 均值表"):
    t = cs.groupby("zone")[["welzel_secular","welzel_emanc","n_resp"]].mean().reset_index()
    t["n_resp"] = cs.groupby("zone")["n_resp"].sum().values
    t.columns = ["文化圈","传统→世俗","生存→自我表达","受访者数"]
    st.dataframe(t.sort_values("生存→自我表达", ascending=False), use_container_width=True, hide_index=True)
