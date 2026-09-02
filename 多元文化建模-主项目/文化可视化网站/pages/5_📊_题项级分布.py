# -*- coding: utf-8 -*-
"""页面5：题项级分布 —— 单题跨国分布(箱线/小提琴)，检验中层理论"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import pandas as pd, numpy as np
import utils
from utils import (load_respondent_dims, load_item_meta, load_item_means,
                   render_sidebar, name_zh, ZONES, ZONE_COLOR, question_text,
                   load_theory)

st.set_page_config(page_title="题项级分布", page_icon="📊", layout="wide")
st.title("📊 题项级跨国分布 Item-level Distribution")

ctx = render_sidebar()
zones = ctx["zones"]; demo = ctx["demo"]
# 题项级需要从受访者表实时算分布（带人口学筛选）
rd = load_respondent_dims()
im = load_item_meta()

# 题项选择
content_q = im[~im["J_code"].isin(["—",None])][["variable","atomic_proposition","J_code","D_primary"]].copy()
content_q["label"] = content_q["variable"] + " | " + content_q["atomic_proposition"].astype(str).str.slice(0,30)
qsel = st.selectbox("选择题项 Select item",
                    content_q["variable"].tolist(),
                    format_func=lambda q: f"{q} | {question_text(q)[:40]}")
qrow = content_q[content_q["variable"]==qsel].iloc[0]
st.markdown(f"**题项**：`{qsel}`　|　**命题**：{question_text(qsel)}　|　**编码**：{qrow['J_code']} / {qrow['D_primary']}")

# 读取该题原始分布：从打包的 item_raw.parquet 取列（云端无需 200MB WVS CSV）
@st.cache_data
def _load_item_raw_table():
    return pd.read_parquet(os.path.join(HERE, "data", "item_raw.parquet"))

@st.cache_data
def load_item_raw(qid, _im):
    raw_all = _load_item_raw_table()
    row = _im[_im["variable"]==qid].iloc[0]
    wcol = row["wvs_col"]
    sub = raw_all[["country","sex","age","edu","income", wcol]].copy()
    sub = sub.rename(columns={wcol: "val"})
    sub["val"] = pd.to_numeric(sub["val"], errors="coerce")
    sub.loc[sub["val"]<0, "val"] = np.nan
    return sub

raw = load_item_raw(qsel, im)
# 应用人口学筛选（demo值→WVS原始码）
sex_map = {"男 Male":"1","女 Female":"2"}
edu_map = {"低 Low":"1","中 Mid":"2","高 High":"3"}
inc_map = {"低 Low":"1","中 Mid":"2","高 High":"3"}
age_bin = {"<30":(0,30),"30-44":(30,45),"45-59":(45,60),"60+":(60,999)}
m = pd.Series(True, index=raw.index)
if demo.get("sex"):
    m &= (raw["sex"]==sex_map.get(demo["sex"]))
if demo.get("edu"):
    m &= (raw["edu"]==edu_map.get(demo["edu"]))
if demo.get("income"):
    inc_map = {"低 Low":"1","中 Mid":"2","高 High":"3"}
    m &= (raw["income"]==inc_map.get(demo["income"]))
if demo.get("age"):
    lo,hi = age_bin[demo["age"]]
    a = pd.to_numeric(raw["age"], errors="coerce")
    m &= (a>=lo) & (a<hi)
raw = raw[m].copy()
raw["zone"] = raw["country"].map(utils.zone_of)
if zones: raw = raw[raw["zone"].isin(zones)]

# 国别均值排序
order = raw.groupby("country")["val"].mean().sort_values().index.tolist()
raw["name_zh"] = raw["country"].map(name_zh)

plot_type = st.radio("图形", ["箱线图 Box","小提琴图 Violin","均值条 Bar"], horizontal=True, key="it_plot")
height = max(500, len(order)*14)
if plot_type=="箱线图 Box":
    fig = px.box(raw, x="val", y="name_zh", color="zone", category_orders={"name_zh":[name_zh(c) for c in order]},
                color_discrete_map=ZONE_COLOR, orientation="h",
                labels={"val":"原始回答 Raw response","name_zh":"国家"}, height=height)
elif plot_type=="小提琴图 Violin":
    fig = px.violin(raw, x="val", y="name_zh", color="zone", category_orders={"name_zh":[name_zh(c) for c in order]},
                   color_discrete_map=ZONE_COLOR, orientation="h", box=True,
                   labels={"val":"原始回答 Raw response","name_zh":"国家"}, height=height)
else:
    m = raw.groupby(["country","name_zh","zone"])["val"].mean().reset_index()
    m = m.set_index("name_zh").reindex([name_zh(c) for c in order]).reset_index()
    fig = px.bar(m, x="val", y="name_zh", color="zone", color_discrete_map=ZONE_COLOR, orientation="h",
                 labels={"val":"均值 Mean","name_zh":"国家"}, height=height)
fig.update_layout(template="plotly_white", yaxis_title="", xaxis_title="原始回答 Raw response", showlegend=True)
st.plotly_chart(fig, use_container_width=True)
st.caption(f"图按各国均值升序排列。原始量表值见题项原始编码(多为1-4或1-10)；负值为缺失已剔除。")

# 关联中层理论
st.divider()
st.subheader("🔗 该题可能支撑的中层理论")
th = load_theory()
J = qrow["J_code"]; D = qrow["D_primary"]
# 找JODCV里含该J和D的理论
def match(t):
    s = str(t.get("JODCV_entry_S_form",""))
    return (J in s) and (D in s)
cand = th[th.apply(match, axis=1)]
if len(cand):
    for _, r in cand.iterrows():
        st.markdown(f"- **{r['theory_id']} {r['theory_name']}**　（{r['section']}）")
        st.caption(str(r["core_mechanism_expected_relation"])[:160] + " …")
else:
    st.info("当前题项的 J/D 组合未直接命中已注册理论（可能因方向/对象未匹配）。可尝试其他题项。")
