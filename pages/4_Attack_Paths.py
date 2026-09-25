"""Session-derived AI attack chain visualization."""

import plotly.graph_objects as go
import streamlit as st

from authcheck import require_auth
from theme import apply_theme, get_active_colors, logout_button, notification_center, sidebar_brand

st.set_page_config(page_title="SecMate - Attack Paths", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(
    "<div class='page-kicker'>EXPOSURE CORRELATION</div>"
    "<div class='page-title'>AI Attack Paths</div>"
    "<div class='page-subtitle'>Understand how observed weaknesses could combine into business impact. Paths shown here are evidence-guided scenarios for analyst validation.</div>",
    unsafe_allow_html=True,
)

history = st.session_state.get("assessment_history", [])
runs_with_findings = [run for run in history if run.get("findings")]
if not runs_with_findings:
    st.info("Attack paths appear after an assessment produces one or more findings. A future correlation service can enrich these session-derived scenarios with identities, tools, and resource telemetry.")
    if st.button("Launch Assessment"):
        st.switch_page("pages/1_New_Assessment.py")
    st.stop()

options = [f"{run['target']} - {run['completed_at']}" for run in runs_with_findings]
selected_label = st.selectbox("Assessment run", options)
run = runs_with_findings[options.index(selected_label)]
findings = run["findings"]
config = run.get("config", {})

category = findings[0].get("category", "Guardrail weakness")
data_profile = ", ".join(config.get("data_classes", [])) or "Application data"
nodes = [
    ("External actor", "Entry point"),
    (run["target"], "AI agent"),
    (category, "Observed weakness"),
    ("Guardrail bypass", "Control impact"),
    (data_profile, "Business exposure"),
]
x = [0, 1.1, 2.2, 3.3, 4.4]
y = [0.55, 0.2, 0.7, 0.2, 0.55]

fig = go.Figure()
for index in range(len(nodes) - 1):
    fig.add_trace(go.Scatter(x=[x[index], x[index + 1]], y=[y[index], y[index + 1]], mode="lines", line=dict(color=COLORS["critical"], width=2, dash="dot"), hoverinfo="skip", showlegend=False))
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers+text",
    marker=dict(size=[32, 42, 46, 42, 48], color=[COLORS["info"], COLORS["low"], COLORS["high"], COLORS["critical"], COLORS["critical"]], line=dict(color=COLORS["text_primary"], width=1)),
    text=[node[0] for node in nodes],
    textposition="top center",
    textfont=dict(color=COLORS["text_primary"], size=12),
    customdata=[node[1] for node in nodes],
    hovertemplate="<b>%{text}</b><br>%{customdata}<extra></extra>",
    showlegend=False,
))
fig.update_layout(height=480, margin=dict(l=30, r=30, t=70, b=30), xaxis=dict(visible=False, range=[-0.4, 4.8]), yaxis=dict(visible=False, range=[-0.2, 1.2]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

graph_col, impact_col = st.columns([2.2, 1])
with graph_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">Evidence-Guided Attack Chain</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("This scenario connects the highest-priority observed finding to plausible impact. It does not claim exploitation beyond captured evidence.")

with impact_col:
    with st.container(border=True):
        st.markdown('<div class="section-title">Impact</div>', unsafe_allow_html=True)
        st.markdown(f"**Terminal outcome**  \nGuardrail or data-boundary failure")
        st.markdown(f"**Business criticality**  \n{config.get('criticality', 'Not classified')}")
        st.markdown(f"**Data at risk**  \n{data_profile}")
        st.markdown(f"**Path confidence**  \nEvidence-guided scenario")
        st.markdown(f"**Findings in scope**  \n{len(findings)}")
    with st.container(border=True):
        st.markdown('<div class="section-title">Break the Chain</div>', unsafe_allow_html=True)
        for finding in findings[:3]:
            st.markdown(f"**{finding['title']}**  \n`{finding['id']}` · {finding['severity'].title()}")
            st.caption(finding["remediation"])
        if st.button("Verify Fix - Re-run Assessment", use_container_width=True):
            st.switch_page("pages/1_New_Assessment.py")
