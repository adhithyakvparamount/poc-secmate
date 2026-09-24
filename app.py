"""
app.py — SecMate entry point: login gate + Dashboard (home page).

This file is the single entry point for the whole app:
    streamlit run app.py

If st.session_state.authenticated is not True, it renders the login
screen (login_screen.py) and stops — the dashboard below never runs.
Once signed in, it shows the Dashboard, and every file under pages/
calls authcheck.require_auth() to enforce the same gate.

VISUAL MOCKUP NOTICE:
All data in this file (metrics, chart values, run history) is placeholder
sample data used to demonstrate the layout. Replace the functions in the
"MOCK DATA — replace with backend calls" section with real calls into
your existing SecMate backend (Red Team / Blue Team / VAPT modules).
Nothing in this file implements assessment logic.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from theme import apply_theme, sidebar_brand, COLORS, metric_card, status_pill, logout_button
from login_screen import render_login_screen

st.set_page_config(page_title="SecMate", layout="wide", initial_sidebar_state="expanded")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login_screen()
    st.stop()

apply_theme()
sidebar_brand()

# Optional: environment/target context selector, purely visual here
st.sidebar.markdown("<div style='padding:0 16px;'>", unsafe_allow_html=True)
st.sidebar.selectbox("Environment", ["Staging", "Production", "Local"], key="env_select")
st.sidebar.markdown("</div>", unsafe_allow_html=True)
logout_button()

# ---------------------------------------------------------------------------
# MOCK DATA — replace with backend calls
# ---------------------------------------------------------------------------
def get_summary_metrics():
    return {
        "assessments": {"value": "128", "delta": "+12 this week", "up": True},
        "findings_total": {"value": "342", "delta": "+8 today", "up": False},
        "critical_open": {"value": "6", "delta": "-2 since last run", "up": True},
        "pass_rate": {"value": "87%", "delta": "+3% vs last week", "up": True},
    }


def get_risk_distribution():
    return {"critical": 6, "high": 24, "medium": 58, "low": 112, "info": 142}


def get_recent_runs():
    return pd.DataFrame([
        {"Target": "PolicyMate Agent v2.3", "Type": "Full Assessment", "Status": "complete", "Critical": 2, "High": 5, "Timestamp": "2026-09-24 08:12"},
        {"Target": "PolicyMate Agent v2.3", "Type": "Red Team Only",   "Status": "complete", "Critical": 1, "High": 3, "Timestamp": "2026-09-23 17:40"},
        {"Target": "Support Bot v1.8",      "Type": "Full Assessment", "Status": "running",  "Critical": "—", "High": "—", "Timestamp": "2026-09-23 15:05"},
        {"Target": "Support Bot v1.8",      "Type": "VAPT Only",       "Status": "failed",   "Critical": "—", "High": "—", "Timestamp": "2026-09-22 11:22"},
        {"Target": "Internal Copilot",      "Type": "Full Assessment", "Status": "complete", "Critical": 0, "High": 2, "Timestamp": "2026-09-21 09:50"},
    ])


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
st.markdown("### Dashboard")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Overview of assessment activity across your monitored targets.</div>",
    unsafe_allow_html=True,
)

metrics = get_summary_metrics()
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Total Assessments", metrics["assessments"]["value"], metrics["assessments"]["delta"], metrics["assessments"]["up"])
with c2:
    metric_card("Findings (Total)", metrics["findings_total"]["value"], metrics["findings_total"]["delta"], metrics["findings_total"]["up"])
with c3:
    metric_card("Critical Open", metrics["critical_open"]["value"], metrics["critical_open"]["delta"], metrics["critical_open"]["up"])
with c4:
    metric_card("Pass Rate", metrics["pass_rate"]["value"], metrics["pass_rate"]["delta"], metrics["pass_rate"]["up"])

st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)
    with st.container(border=True):
        risk = get_risk_distribution()
        total = sum(risk.values())
        fig = go.Figure()
        sev_colors = {
            "critical": COLORS["critical"], "high": COLORS["high"],
            "medium": COLORS["medium"], "low": COLORS["low"], "info": COLORS["info"],
        }
        for sev, count in risk.items():
            fig.add_trace(go.Bar(
                y=["Findings"], x=[count], name=sev.title(),
                orientation="h", marker_color=sev_colors[sev],
                text=f"{count}", textposition="inside",
                hovertemplate=f"{sev.title()}: {count} ({count/total:.0%})<extra></extra>",
            ))
        fig.update_layout(
            barmode="stack", height=110,
            margin=dict(l=0, r=0, t=10, b=0),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text_secondary"], size=12),
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            legend=dict(orientation="h", y=-0.3, font=dict(color=COLORS["text_secondary"])),
            showlegend=True,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with col_right:
    st.markdown('<div class="section-title">Findings by Severity</div>', unsafe_allow_html=True)
    with st.container(border=True):
        risk = get_risk_distribution()
        for sev in ["critical", "high", "medium", "low", "info"]:
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 2px;">
                    <span class="badge badge-{sev}">{sev.upper()}</span>
                    <span style="font-family:'JetBrains Mono',monospace; color:{COLORS['text_primary']}; font-size:14px;">{risk[sev]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Recent Assessments</div>', unsafe_allow_html=True)

with st.container(border=True):
    runs = get_recent_runs()
    header_cols = st.columns([2.2, 1.6, 1, 0.8, 0.8, 1.4])
    for col, label in zip(header_cols, ["Target", "Type", "Status", "Crit.", "High", "Timestamp"]):
        col.markdown(f"<span style='color:{COLORS['text_secondary']}; font-size:12px;'>{label}</span>", unsafe_allow_html=True)
    st.markdown(f"<hr style='margin:6px 0; border-color:{COLORS['border']};'>", unsafe_allow_html=True)
    for _, row in runs.iterrows():
        cols = st.columns([2.2, 1.6, 1, 0.8, 0.8, 1.4])
        cols[0].markdown(f"<span style='font-size:13.5px;'>{row['Target']}</span>", unsafe_allow_html=True)
        cols[1].markdown(f"<span style='font-size:13.5px; color:{COLORS['text_secondary']};'>{row['Type']}</span>", unsafe_allow_html=True)
        cols[2].markdown(status_pill(row["Status"]), unsafe_allow_html=True)
        cols[3].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:13px;'>{row['Critical']}</span>", unsafe_allow_html=True)
        cols[4].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:13px;'>{row['High']}</span>", unsafe_allow_html=True)
        cols[5].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:12px; color:{COLORS['text_secondary']};'>{row['Timestamp']}</span>", unsafe_allow_html=True)
