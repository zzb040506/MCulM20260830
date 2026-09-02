# -*- coding: utf-8 -*-
"""页面8：S ↔ JOD 共现网络 —— 解析 34 条中层理论的 JODCV_entry_S_form，
构建 S 代码与 J/O/D 代码的共现二部图。"""
import sys, os, re
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import streamlit as st
import plotly.graph_objects as go
import pandas as pd, numpy as np
from utils import load_theory, D_ORDER, J_ORDER, O_ORDER, D_ZH, J_ZH, O_ZH

st.set_page_config(page_title="S-JOD 共现网络", page_icon="🧬", layout="wide")
st.title("🧬 S ↔ JOD 共现网络 S-JOD Co-occurrence Network")
st.caption("解析 34 条中层理论的 JODCV_entry_S_form 字段，构建跨命题结构 S 与判断 J/对象 O/场域 D 的共现关系。")

th = load_theory()
S_ORDER = ["S-CB","S-SC","S-FR","S-BC","S-NA","S-DR","S-GE"]
S_ZH = {
    "S-CB":"类别与边界 Class.&Bound.","S-SC":"图式 Schemas","S-FR":"框架 Frames",
    "S-BC":"二元代码 Binary Codes","S-NA":"叙事 Narratives",
    "S-DR":"话语 Discourses","S-GE":"体裁 Genres",
}

# --- 解析 JODCV_entry_S_form ---
# 字段格式形如："J-CM、J-ER、J-NO、J-RA；O-AR、O-GP、O-OI、O-PL、O-RP、O-MSW；D-PL、D-MC；C-VA、C-CT；S-BC，可与S-FR、S-NA并存"
# 用正则提取所有 X-XXX 代码
def parse_jodcv(s):
    s = str(s)
    # 匹配 J-XX, O-XX, D-XX, C-XX, S-XX, S-XX-YY 等
    codes = re.findall(r'\b([JODCS]-[A-Z]+(?:-[A-Z]+)?)\b', s)
    j = [c for c in codes if c.startswith("J-")]
    o = [c for c in codes if c.startswith("O-")]
    d = [c for c in codes if c.startswith("D-")]
    s_ = [c for c in codes if c.startswith("S-")]
    # 去重保序
    def uniq(lst):
        seen, out = set(), []
        for c in lst:
            if c not in seen: seen.add(c); out.append(c)
        return out
    return {"J": uniq(j), "O": uniq(o), "D": uniq(d), "S": uniq(s_)}

th_parsed = th.assign(
    _parsed=th["JODCV_entry_S_form"].apply(parse_jodcv),
    theory=lambda df: df["theory_id"].astype(str) + " " + df["theory_name"].astype(str),
)

# --- 统计 S × JOD 共现 ---
# edges: dict[(s, jod_code)] = count, theory_list
edges = {}
for _, r in th_parsed.iterrows():
    p = r["_parsed"]
    s_list = p["S"]
    jod = p["J"] + p["O"] + p["D"]
    for s in s_list:
        for code in jod:
            key = (s, code)
            if key not in edges: edges[key] = {"count": 0, "theories": []}
            edges[key]["count"] += 1
            edges[key]["theories"].append(r["theory"])

# 过滤：S 必须在 S_ORDER，JOD 必须在已用代码
def is_valid_s(s): return s in S_ORDER
def is_valid_jod(c):
    return c in J_ORDER or c in O_ORDER or c in D_ORDER

edges = {k: v for k, v in edges.items() if is_valid_s(k[0]) and is_valid_jod(k[1])}

# --- 节点准备 ---
# 左侧 S 节点（7个），右侧 JOD 节点（动态）
s_nodes = S_ORDER[:]
# 右侧节点：按 J → O → D 顺序，只保留出现过的
jod_nodes = []
for c in J_ORDER + O_ORDER + D_ORDER:
    if any(k[1] == c for k in edges):
        jod_nodes.append(c)

# 类别颜色
def jod_color(c):
    if c.startswith("J-"): return "#C0504D"
    if c.startswith("O-"): return "#3A8FB7"
    if c.startswith("D-"): return "#2E5C8A"
    return "#888"

# 布局：S 在左(x=0)，JOD 在右(x=1)，按顺序均匀分布
n_s, n_jod = len(s_nodes), len(jod_nodes)
s_y = np.linspace(1, 0, n_s) if n_s > 1 else [0.5]
jod_y = np.linspace(1, 0, n_jod) if n_jod > 1 else [0.5]
s_pos = {n: (0, y) for n, y in zip(s_nodes, s_y)}
jod_pos = {n: (1, y) for n, y in zip(jod_nodes, jod_y)}

# 节点标签
def s_label(c): return f"{c}<br>{S_ZH.get(c,c)}"
def jod_label(c):
    if c.startswith("J-"): zh = J_ZH.get(c, c)
    elif c.startswith("O-"): zh = O_ZH.get(c, c)
    elif c.startswith("D-"): zh = D_ZH.get(c, c)
    else: zh = c
    short = zh.split(" ")[0] if zh else c
    return f"{c}<br>{short}"

# --- 画图：节点 + 边 ---
fig = go.Figure()

# 边（按 S 节点分组着色，便于辨识）
for s in s_nodes:
    edge_x, edge_y = [], []
    widths = []
    hover_texts = []
    for (ss, code), v in edges.items():
        if ss != s: continue
        x0, y0 = s_pos[s]
        x1, y1 = jod_pos[code]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        widths.append(v["count"])
        hover_texts.append(f"{s} ↔ {code}<br>共现 {v['count']} 次<br>理论: {', '.join(v['theories'][:2])}{'…' if len(v['theories'])>2 else ''}")
    # 用宽度差异画粗细（plotly 不支持单 trace 内变宽度，这里折中用 trace 数 = 1 每条边）
    # 为了 hover 信息丰富，逐边画
    for (ss, code), v in [((s, c), vv) for (ss, c), vv in edges.items() if ss == s]:
        x0, y0 = s_pos[s]
        x1, y1 = jod_pos[code]
        w = 1 + v["count"] * 1.5
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(width=w, color="rgba(153,153,153,0.45)"),
            hovertext=f"{s} ↔ {code}　共现 {v['count']} 次　涉及: {', '.join(v['theories'][:3])}{'…' if len(v['theories'])>3 else ''}",
            hoverinfo="text", showlegend=False,
        ))

# S 节点（左侧）
fig.add_trace(go.Scatter(
    x=[s_pos[s][0] for s in s_nodes],
    y=[s_pos[s][1] for s in s_nodes],
    mode="markers+text",
    marker=dict(size=28, color="#7F6BAF", line=dict(width=1, color="white")),
    text=[s_label(s) for s in s_nodes],
    textposition="middle left",
    textfont=dict(size=11, color="#333"),
    hovertext=[f"{s} | {S_ZH.get(s,s)}" for s in s_nodes],
    hoverinfo="text", name="S 结构", showlegend=False,
))
# JOD 节点（右侧）
fig.add_trace(go.Scatter(
    x=[jod_pos[c][0] for c in jod_nodes],
    y=[jod_pos[c][1] for c in jod_nodes],
    mode="markers+text",
    marker=dict(size=22, color=[jod_color(c) for c in jod_nodes], line=dict(width=1, color="white")),
    text=[jod_label(c) for c in jod_nodes],
    textposition="middle right",
    textfont=dict(size=10, color="#333"),
    hovertext=[f"{c} | {('J' if c.startswith('J-') else 'O' if c.startswith('O-') else 'D')}" for c in jod_nodes],
    hoverinfo="text", name="JOD 代码", showlegend=False,
))

fig.update_layout(
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.35, 1.35]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.1, 1.1]),
    template="plotly_white", height=700, margin=dict(l=20, r=20, t=20, b=20),
)
st.plotly_chart(fig, use_container_width=True)
st.caption("左=7个 S 跨命题结构；右=J(红)/O(青)/D(蓝) 代码。边粗=共现次数（理论数）。悬停看涉及理论。")

# --- 图例说明 ---
st.markdown("**图例**：　🔴 J 判断类型 (6)　🔵 O 对象类型 (14)　🔷 D 场域 (8)　🟣 S 跨命题结构 (7)")

# --- 共现统计表 ---
st.divider()
st.subheader("共现矩阵 S × JOD Co-occurrence matrix")
# 构造矩阵行=S，列=JOD
mat = pd.DataFrame(0, index=s_nodes, columns=jod_nodes, dtype=int)
for (s, code), v in edges.items():
    mat.loc[s, code] = v["count"]
# 简化列名（取首词）
mat.columns = [c for c in mat.columns]
fig2 = go.Figure(data=go.Heatmap(
    z=mat.values,
    x=list(mat.columns),
    y=[f"{s} {S_ZH.get(s,s).split(' ')[0]}" for s in mat.index],
    colorscale="Blues",
    text=mat.values,
    texttemplate="%{text}",
    hovertemplate="S=%{y}<br>JOD=%{x}<br>共现=%{z}<extra></extra>",
    colorbar=dict(title="共现次数"),
))
fig2.update_layout(template="plotly_white", height=max(400, len(s_nodes)*55),
                   xaxis=dict(tickangle=-35), margin=dict(l=20, r=20, t=20, b=80))
st.plotly_chart(fig2, use_container_width=True)
st.caption("矩阵值=该 S 代码与该 JOD 代码共同出现在多少条理论中。深色=共现更频繁。")

# --- 详情表 ---
st.divider()
st.subheader("理论 × S 代码明细 Theory × S codes")
rows = []
for _, r in th_parsed.iterrows():
    p = r["_parsed"]
    if not p["S"]: continue
    rows.append({
        "theory_id": r["theory_id"],
        "theory_name": r["theory_name"],
        "section": r["section"],
        "S_codes": "、".join(p["S"]),
        "J_codes": "、".join(p["J"]),
        "O_codes": "、".join(p["O"]),
        "D_codes": "、".join(p["D"]),
    })
df_detail = pd.DataFrame(rows)
st.dataframe(df_detail, use_container_width=True, hide_index=True)
st.caption(f"共 {len(df_detail)} 条理论在 JODCV_entry_S_form 中标注了 S 代码。")
