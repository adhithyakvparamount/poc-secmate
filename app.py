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
import time

from theme import apply_theme, sidebar_brand, COLORS, metric_card, status_pill, logout_button
from login_screen import render_login_screen

st.set_page_config(page_title="SecMate", layout="wide", initial_sidebar_state="expanded")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login_screen()
    st.stop()


def get_onboarding_steps():
    return [
        {"label": "Connect your target", "description": "Add the AI agent endpoint and the auth method SecMate should use."},
        {"label": "Pick security coverage", "description": "Choose Red Team, Blue Team, and VAPT checks for your first run."},
        {"label": "Review live findings", "description": "Track severity, exploit evidence, and guardrail behavior in one view."},
        {"label": "Export the report", "description": "Generate a stakeholder-ready report after validation is complete."},
    ]


def render_onboarding_loading():
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{ display: none; }}
        .stApp {{ background: radial-gradient(circle at center, {COLORS['surface']} 0%, {COLORS['canvas']} 62%); }}
        .block-container {{ max-width: 760px; padding-top: 22vh; }}
        .scale-loader {{
            width: 78px;
            height: 78px;
            margin: 0 auto 24px auto;
            border-radius: 22px;
            background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['low']});
            animation: scalePulse 1.05s ease-in-out infinite;
            box-shadow: 0 0 42px rgba(139,124,246,0.28);
        }}
        @keyframes scalePulse {{
            0%, 100% {{ transform: scale(0.86); opacity: 0.72; }}
            50% {{ transform: scale(1.12); opacity: 1; }}
        }}
        .loading-title {{ text-align:center; color:{COLORS['text_primary']}; font-size:24px; font-weight:700; }}
        .loading-sub {{ text-align:center; color:{COLORS['text_secondary']}; font-size:13px; margin-top:8px; }}
        </style>
        <div class="scale-loader"></div>
        <div class="loading-title">Preparing your SecMate workspace</div>
        <div class="loading-sub">Loading onboarding, profile, and assessment defaults.</div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(1.15)
    st.session_state.onboarding_loading = False
    st.rerun()


def render_onboarding_page():
    st.markdown(
        f"""
        <style>
        section[data-testid="stSidebar"] {{ display: none; }}
        .stApp {{ background: radial-gradient(900px 520px at 28% 10%, rgba(139,124,246,0.11), transparent 62%), {COLORS['canvas']}; }}
        .block-container {{ max-width: 1120px; padding-top: 3.5rem; }}
        .onboarding-hero {{
            border: 1px solid {COLORS['border']};
            border-radius: 22px;
            padding: 34px;
            background: linear-gradient(135deg, rgba(28,35,51,0.92), rgba(17,24,39,0.78));
        }}
        .onboarding-kicker {{ color:{COLORS['accent']}; font-family:'JetBrains Mono',monospace; font-size:12px; margin-bottom:10px; }}
        .onboarding-title {{ color:{COLORS['text_primary']}; font-size:38px; font-weight:800; line-height:1.12; max-width:700px; }}
        .onboarding-copy {{ color:{COLORS['text_secondary']}; font-size:15px; line-height:1.7; max-width:680px; margin-top:14px; }}
        .onboarding-step {{
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 16px;
            background: rgba(255,255,255,0.018);
            min-height: 132px;
        }}
        .onboarding-number {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: rgba(139,124,246,0.13);
            color: {COLORS['accent']};
            display: flex;
            align-items: center;
            justify-content: center;
            font-family:'JetBrains Mono',monospace;
            font-size:12px;
            font-weight:700;
            margin-bottom: 12px;
        }}
        </style>
        <div class="onboarding-hero">
            <div class="onboarding-kicker">SECURITY WORKSPACE SETUP</div>
            <div class="onboarding-title">Set up your first AI security assessment.</div>
            <div class="onboarding-copy">Before opening the dashboard, SecMate walks you through the core workflow: connect a target, select security coverage, review findings, and export an assessment report.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)
    cols = st.columns(4)
    for index, (col, step) in enumerate(zip(cols, get_onboarding_steps()), start=1):
        col.markdown(
            f"""
            <div class="onboarding-step">
                <div class="onboarding-number">0{index}</div>
                <div style="color:{COLORS['text_primary']}; font-weight:700; font-size:14px; margin-bottom:8px;">{step['label']}</div>
                <div style="color:{COLORS['text_secondary']}; font-size:12.8px; line-height:1.5;">{step['description']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Tell us about your use case</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(
                "Which best describes you?",
                ["Student", "Engineer", "Working Professional", "Security Analyst", "Founder / Product Owner", "Other"],
                key="onboarding_user_type",
            )
        with c2:
            st.selectbox(
                "What will you use SecMate for?",
                [
                    "Learning AI security",
                    "Testing an internal AI agent",
                    "Client security assessments",
                    "Compliance and audit reports",
                    "Research and experimentation",
                    "Production monitoring",
                ],
                key="onboarding_use_case",
            )
        st.text_area(
            "Anything specific you want SecMate to help with?",
            placeholder="Example: test prompt injection risks before deploying a customer support bot.",
            key="onboarding_goal",
        )

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([0.22, 1])
    with c1:
        if st.button("Enter Dashboard", use_container_width=True):
            st.session_state.onboarding_seen = True
            st.rerun()
    with c2:
        st.markdown(
            f"<div style='color:{COLORS['text_secondary']}; font-size:12.5px; padding-top:9px;'>You can change theme, profile, and assessment defaults from the account settings later.</div>",
            unsafe_allow_html=True,
        )


apply_theme()

if not st.session_state.get("onboarding_seen", False):
    if st.session_state.get("onboarding_loading", False):
        render_onboarding_loading()
    else:
        render_onboarding_page()
    st.stop()

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


def render_dashboard_header():
    user_type = st.session_state.get("onboarding_user_type", "Security Analyst")
    use_case = st.session_state.get("onboarding_use_case", "Testing an internal AI agent")
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; gap:18px; align-items:center; margin-bottom:20px;">
            <div>
                <div style="color:{COLORS['text_secondary']}; font-family:'JetBrains Mono',monospace; font-size:12px; margin-bottom:5px;">{user_type} workspace</div>
                <div style="color:{COLORS['text_primary']}; font-size:26px; font-weight:750; letter-spacing:-0.02em;">Dashboard</div>
                <div style="color:{COLORS['text_secondary']}; font-size:13px; margin-top:4px;">Optimized for: {use_case}</div>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:10px; padding:9px 12px; min-width:260px; color:{COLORS['text_secondary']}; font-size:13px;">
                    Search targets, reports, findings...
                </div>
                <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:10px; padding:9px 11px; color:{COLORS['text_primary']}; position:relative;">
                    <span style="position:absolute; top:6px; right:7px; width:7px; height:7px; border-radius:50%; background:{COLORS['critical']};"></span>
                    Alerts
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_col, status_col = st.columns([0.17, 1])
    with action_col:
        if st.button("New Assessment", use_container_width=True):
            st.switch_page("pages/1_New_Assessment.py")
    with status_col:
        st.markdown(
            f"<div style='color:{COLORS['text_secondary']}; font-size:12.5px; padding-top:8px;'>Workspace health: <span style='color:{COLORS['accent']};'>ready</span> · 1 assessment running · 2 critical alerts need review</div>",
            unsafe_allow_html=True,
        )


def render_quick_start_panel():
    st.markdown('<div class="section-title">Quick Start</div>', unsafe_allow_html=True)
    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.markdown(
                f"""
                <div style="font-size:18px; font-weight:700; color:{COLORS['text_primary']}; margin-bottom:6px;">Improve your first assessment run</div>
                <div style="color:{COLORS['text_secondary']}; font-size:13px; line-height:1.6; max-width:620px;">
                    Use this checklist to move from setup to a useful security report. Your existing dashboard below still shows live metrics, severity distribution, and recent runs.
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            checklist = [
                ("Connect production-like target", "Use staging or a safe replica before testing live users."),
                ("Enable critical alerts", "Get notified when jailbreak or data exposure risks appear."),
                ("Generate executive report", "Summarize risk, evidence, and remediation for stakeholders."),
            ]
            for title, description in checklist:
                st.markdown(
                    f"""
                    <div style="display:flex; gap:10px; margin-bottom:10px; align-items:flex-start;">
                        <div style="width:18px; height:18px; border-radius:50%; background:rgba(139,124,246,0.14); color:{COLORS['accent']}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">✓</div>
                        <div>
                            <div style="color:{COLORS['text_primary']}; font-size:13.5px; font-weight:600;">{title}</div>
                            <div style="color:{COLORS['text_secondary']}; font-size:12.5px; margin-top:2px;">{description}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with right:
            st.markdown(
                f"""
                <div style="border:1px solid {COLORS['border']}; border-radius:12px; padding:16px; background:rgba(255,255,255,0.018);">
                    <div style="color:{COLORS['text_secondary']}; font-size:12px; margin-bottom:8px;">Recommended next action</div>
                    <div style="color:{COLORS['text_primary']}; font-size:17px; font-weight:700; margin-bottom:8px;">Review critical findings</div>
                    <div style="color:{COLORS['text_secondary']}; font-size:12.8px; line-height:1.55; margin-bottom:14px;">There are 6 open critical findings. Prioritize evidence review before exporting a report.</div>
                    <div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:12px; color:{COLORS['text_secondary']};">
                        <span>Risk score</span><span style="color:{COLORS['critical']};">High</span>
                    </div>
                    <div style="height:8px; border-radius:999px; background:{COLORS['elevated']}; margin-top:8px; overflow:hidden;">
                        <div style="width:72%; height:100%; background:linear-gradient(90deg,{COLORS['high']},{COLORS['critical']});"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
render_dashboard_header()
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Overview of assessment activity across your monitored targets.</div>",
    unsafe_allow_html=True,
)

render_quick_start_panel()

st.markdown("<div style='height:22px;'></div>", unsafe_allow_html=True)

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
