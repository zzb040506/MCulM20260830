# -*- coding: utf-8 -*-
"""页面7：编码体系说明 —— 展示290题如何归约到文化图式"""
import sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd, numpy as np
import utils
from utils import (load_item_meta, load_theory, load_country_summary, render_sidebar,
                   D_ORDER, J_ORDER, O_ORDER, D_ZH, J_ZH, O_ZH)

st.set_page_config(page_title="编码体系", page_icon="📐", layout="wide")
st.title("📐 编码体系：290题如何归约到文化图式")

st.markdown("""
本页展示自建编码体系如何把 **WVS 290题** 逐步归约到 **文化图式**，是上述跨国可视化的方法论基础。
""")

# --- 流程链 ---
st.subheader("工作链 Pipeline")
st.markdown("""
`290题原子命题` → 按 `J/O/D/C/V` 编码 → 按 `JODCV模式` 分组 → `中层理论(34条)` → 检验证据/反证 → `文化图式 S-SC`
""")
steps = ["方法论\n核心框架", "编码规范\n语义编号表", "数据执行\n290题编码", "理论提升\n34中层理论", "结构判断\n文化图式"]
st.columns(5)  # placeholder; 用文字流程
cols = st.columns(5)
for i,(col,s) in enumerate(zip(cols,steps)):
    col.markdown(f"```\n{i+1}\n```")
    col.markdown(f"**{s}**")

st.divider()

# --- 维度构成统计 ---
im = load_item_meta()
cs = load_country_summary()

st.subheader("各维度题项构成 Item composition per dimension")
from collections import Counter
cJ = Counter(im["J_code"])
cD = Counter(im["D_primary"])
cO = Counter(im["O_primary"])
c1, c2, c3 = st.columns(3)
with c1:
    df = pd.DataFrame([(k,v) for k,v in cJ.items() if k not in ("—",None)],
                      columns=["code","n"]).sort_values("n",ascending=True)
    df["label"] = df["code"].map(lambda k: J_ZH.get(k,k))
    fig = px.bar(df, x="n", y="label", orientation="h", text="n",
                 labels={"n":"题项数","label":""}, height=420)
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("判断类型 J Judgment")
with c2:
    df = pd.DataFrame([(k,v) for k,v in cD.items() if k not in ("—",None,"OPEN-PROVISIONAL")],
                      columns=["code","n"]).sort_values("n",ascending=True)
    df["label"] = df["code"].map(lambda k: D_ZH.get(k,k))
    fig = px.bar(df, x="n", y="label", orientation="h", text="n",
                 labels={"n":"题项数","label":""}, height=420)
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("场域 D Domain")
with c3:
    df = pd.DataFrame([(k,v) for k,v in cO.items() if k not in ("—",None,"OPEN-PROVISIONAL")],
                      columns=["code","n"]).sort_values("n",ascending=True)
    df["label"] = df["code"].map(lambda k: O_ZH.get(k,k))
    fig = px.bar(df, x="n", y="label", orientation="h", text="n",
                 labels={"n":"题项数","label":""}, height=420)
    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("对象 O Object (14个有题项的代码)")

st.divider()

# --- 中层理论浏览 ---
st.subheader("中层理论注册表 Mid-level theory registry")
th = load_theory()
sec = st.selectbox("按板块筛选 Filter by section", ["全部"]+sorted(th["section"].unique().tolist()))
show = th if sec=="全部" else th[th["section"]==sec]
for _, r in show.iterrows():
    with st.expander(f"{r['theory_id']}　{r['theory_name']}　（{r['section']}）"):
        cA,cB = st.columns([2,1])
        with cA:
            st.markdown(f"**核心机制**：{r['core_mechanism_expected_relation']}")
            st.markdown(f"**预期入口**：`{r['JODCV_entry_S_form']}`")
        with cB:
            st.markdown(f"**来源级别**：{r['source_level']}")
            st.caption(str(r["literature_basis"])[:120] + " …")
        st.markdown(f"**证据/反证**：{r['observable_evidence_falsification']}")

st.divider()
st.caption("注：本编码体系单题只作指标；结构判断须基于多题联合分布。详见主项目 `国家文化知识建模_*` 系列表。")

# --- S 结构代码参考 ---
st.divider()
st.subheader("跨命题文化结构 S Structures (理论级)")
st.markdown("""
S 代码不是题项级，而是 **跨命题/理论级**：用于描述 34 条中层理论所涉及的「文化结构类型」。
每个理论的 `JODCV_entry_S_form` 字段中标注其涉及的 S 代码（及 J/O/D/C 代码共现关系）。
详见「S-JOD 共现网络」页。
""")
S_ZH = {
    "S-CB": "类别与边界 Classification & Boundaries — 类别之间的成员资格、亲疏、地位、排斥与跨界关系",
    "S-SC": "图式 Schemas — 多个概念或命题构成、可由线索激活的关系网络",
    "S-FR": "框架 Frames — 围绕问题、原因、道德评价和解决方案形成的选择性组织",
    "S-BC": "二元代码 Binary Codes — 成组对立概念、价向及其对象映射",
    "S-NA": "叙事 Narratives — 角色、时间、因果与情节组织",
    "S-DR": "话语与复现 Discourses & Repertoires — 围绕议题形成的竞争立场、理由和表达资源",
    "S-GE": "体裁 Genres — 反复交往情境中的形式惯例、预期受众和适当言语行动",
}
S_ORDER = ["S-CB","S-SC","S-FR","S-BC","S-NA","S-DR","S-GE"]
sdf = pd.DataFrame([(k, v.split(" — ")[0], v.split(" — ")[1] if " — " in v else "") for k,v in S_ZH.items()],
                   columns=["代码 code","英文名 en","定义 definition"])
st.dataframe(sdf, use_container_width=True, hide_index=True)

# --- O 对象代码参考 ---
st.subheader("对象 O 代码参考 Object codes reference")
st.markdown("以下为 O 的 14 个有题项覆盖的代码（语义表共 20 个，余下 6 个未在本批 290 题作为 primary 出现）：")
odf = pd.DataFrame([(o, O_ZH.get(o,o).split(" ")[0], O_ZH.get(o,o)) for o in O_ORDER],
                   columns=["代码 code","关键词 key","中英对照 label"])
st.dataframe(odf, use_container_width=True, hide_index=True)
