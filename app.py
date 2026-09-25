"""
app.py — SecMate entry point: login gate + Dashboard (home page).

This file is the single entry point for the whole app:
    streamlit run app.py

If st.session_state.authenticated is not True, it renders the login
screen (login_screen.py) and stops — the dashboard below never runs.
Once signed in, it shows the Dashboard, and every file under pages/
calls authcheck.require_auth() to enforce the same gate.

Dashboard metrics, severity distribution, and recent runs are derived from
the current session's assessment history. Persistent multi-user aggregation
still requires a backend data store.
"""

import streamlit as st
import plotly.graph_objects as go
import time

from theme import apply_theme, sidebar_brand, get_active_colors, metric_card, notification_center, status_pill, logout_button
from login_screen import render_login_screen
from workspace import DENSITIES, ENVIRONMENTS, LANGUAGES, USER_TYPES, USE_CASES, initialize_workspace_state, option_label, save_workspace_profile, t

st.set_page_config(page_title="SecMate", layout="wide", initial_sidebar_state="expanded")
initialize_workspace_state()
COLORS = get_active_colors()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    render_login_screen()
    st.stop()


def get_onboarding_steps():
    return [
        {"label": t("step_connect"), "description": t("step_connect_desc")},
        {"label": t("step_coverage"), "description": t("step_coverage_desc")},
        {"label": t("step_findings"), "description": t("step_findings_desc")},
        {"label": t("step_report"), "description": t("step_report_desc")},
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
            box-shadow: 0 0 42px {COLORS['accent']}47;
        }}
        @keyframes scalePulse {{
            0%, 100% {{ transform: scale(0.86); opacity: 0.72; }}
            50% {{ transform: scale(1.12); opacity: 1; }}
        }}
        .loading-title {{ text-align:center; color:{COLORS['text_primary']}; font-size:24px; font-weight:700; }}
        .loading-sub {{ text-align:center; color:{COLORS['text_secondary']}; font-size:13px; margin-top:8px; }}
        </style>
        <div class="scale-loader"></div>
        <div class="loading-title">{t('loading_title')}</div>
        <div class="loading-sub">{t('loading_subtitle')}</div>
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
        .stApp {{ background: radial-gradient(900px 520px at 28% 10%, {COLORS['accent']}1C, transparent 62%), {COLORS['canvas']}; }}
        .block-container {{ max-width: 1040px; padding-top: 2.5rem; }}
        .onboarding-hero {{
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 26px 28px;
            background: linear-gradient(135deg, {COLORS['surface']}, {COLORS['elevated']});
        }}
        .onboarding-kicker {{ color:{COLORS['accent']}; font-family:'JetBrains Mono',monospace; font-size:12px; margin-bottom:10px; }}
        .onboarding-title {{ color:{COLORS['text_primary']}; font-size:32px; font-weight:800; line-height:1.12; max-width:700px; }}
        .onboarding-copy {{ color:{COLORS['text_secondary']}; font-size:14px; line-height:1.6; max-width:680px; margin-top:12px; }}
        .onboarding-step {{
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 14px;
            background: {COLORS['elevated']};
            min-height: 116px;
        }}
        .onboarding-number {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            background: {COLORS['accent']}21;
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
            <div class="onboarding-kicker">{t('onboarding_kicker')}</div>
            <div class="onboarding-title">{t('onboarding_title')}</div>
            <div class="onboarding-copy">{t('onboarding_copy')}</div>
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
        st.markdown(f'<div class="section-title">{t("about_use_case")}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.selectbox(
                t("user_type_question"),
                USER_TYPES,
                key="onboarding_user_type",
            )
        with c2:
            st.selectbox(
                t("use_case_question"),
                USE_CASES,
                key="onboarding_use_case",
            )
        st.text_area(
            t("goal_question"),
            placeholder=t("goal_placeholder"),
            key="onboarding_goal",
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f'<div class="section-title">{t("workspace_preferences")}</div>', unsafe_allow_html=True)
        p1, p2, p3 = st.columns(3)
        with p1:
            st.selectbox(t("language"), LANGUAGES, key="language_pref")
        with p2:
            st.selectbox(t("environment"), ENVIRONMENTS, key="workspace_environment")
        with p3:
            st.selectbox(t("dashboard_density"), DENSITIES, key="dashboard_density")

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([0.22, 1])
    with c1:
        if st.button(t("enter_dashboard"), use_container_width=True):
            save_workspace_profile()
            st.session_state.onboarding_seen = True
            st.rerun()
    with c2:
        st.markdown(
            f"<div style='color:{COLORS['text_secondary']}; font-size:12.5px; padding-top:9px;'>{t('preferences_hint')}</div>",
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
logout_button()
notification_center()

def get_assessment_history():
    return st.session_state.get("assessment_history", [])


def get_all_findings():
    return [finding for run in get_assessment_history() for finding in run.get("findings", [])]


def get_summary_metrics():
    history = get_assessment_history()
    findings = get_all_findings()
    exchanges = [exchange for run in history for exchange in run.get("exchanges", [])]
    resisted = sum(exchange.get("verdict") == "resisted" for exchange in exchanges)
    pass_rate = round((resisted / len(exchanges)) * 100) if exchanges else 0
    critical = sum(finding.get("severity") == "critical" and finding.get("status", "open") == "open" for finding in findings)
    return {
        "assessments": {"value": str(len(history)), "delta": "completed in this session" if history else "launch your first run", "up": True},
        "findings_total": {"value": str(len(findings)), "delta": "validated evidence items" if findings else "no findings recorded", "up": not findings},
        "critical_open": {"value": str(critical), "delta": "requires immediate review" if critical else "no critical exposure", "up": not critical},
        "pass_rate": {"value": f"{pass_rate}%", "delta": f"{resisted} of {len(exchanges)} tests resisted" if exchanges else "awaiting assessment data", "up": pass_rate >= 80},
    }


def get_risk_distribution():
    distribution = {severity: 0 for severity in ["critical", "high", "medium", "low", "info"]}
    for finding in get_all_findings():
        severity = finding.get("severity", "info")
        distribution[severity] = distribution.get(severity, 0) + 1
    return distribution


def get_recent_runs():
    runs = []
    for run in get_assessment_history()[:6]:
        findings = run.get("findings", [])
        runs.append({
            "Target": run.get("target", "Unknown target"),
            "Type": "Adversarial Assessment",
            "Status": run.get("status", "pending"),
            "Critical": sum(f.get("severity") == "critical" for f in findings),
            "High": sum(f.get("severity") == "high" for f in findings),
            "Timestamp": run.get("completed_at", "—"),
        })
    return runs


def render_dashboard_header():
    user_type = option_label(st.session_state.get("onboarding_user_type", "Security Analyst"))
    use_case = option_label(st.session_state.get("onboarding_use_case", "Testing an internal AI agent"))
    environment = option_label(st.session_state.get("workspace_environment", "Staging"))
    unread_count = sum(bool(item.get("unread")) for item in st.session_state.get("notifications", []))
    history = get_assessment_history()
    last_updated = history[0].get("completed_at", "No assessment data") if history else "No assessment data"
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; gap:18px; align-items:center; margin-bottom:20px;">
            <div>
                <div class="page-kicker">SECURITY OPERATIONS · {environment}</div>
                <div class="page-title">Risk Posture</div>
                <div style="color:{COLORS['text_secondary']}; font-size:13px; margin-top:4px;">{t('optimized_for')}: {use_case}</div>
            </div>
            <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:999px; padding:8px 13px; color:{COLORS['text_secondary']}; font-family:'JetBrains Mono',monospace; font-size:11px;">
                LAST UPDATED · {last_updated}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    action_col, status_col = st.columns([0.17, 1])
    with action_col:
        if st.button(t("new_assessment"), use_container_width=True):
            st.switch_page("pages/1_New_Assessment.py")
    with status_col:
        st.markdown(
            f"<div style='color:{COLORS['text_secondary']}; font-size:12.5px; padding-top:8px;'>{t('workspace_health')}: <span style='color:{COLORS['accent']};'>{t('ready')}</span> · {t('unread_notifications', count=unread_count)}</div>",
            unsafe_allow_html=True,
        )


def render_quick_start_panel():
    history = get_assessment_history()
    findings = get_all_findings()
    critical_count = sum(f.get("severity") == "critical" for f in findings)
    st.markdown('<div class="section-title">Operational Readiness</div>', unsafe_allow_html=True)
    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.markdown(
                f"""
                <div style="font-size:18px; font-weight:700; color:{COLORS['text_primary']}; margin-bottom:6px;">{'Security program is active' if history else 'Prepare your first production-grade assessment'}</div>
                <div style="color:{COLORS['text_secondary']}; font-size:13px; line-height:1.6; max-width:620px;">
                    {'Review current evidence, prioritize exposure, and validate fixes before the next release.' if history else 'Complete these controls to create a defensible assessment baseline for your AI agent.'}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
            checklist = [
                ("Target connected" if history else "Connect production-like target", "Use staging or a safe replica before testing live users.", bool(history)),
                ("Evidence captured" if findings else "Validate guardrail evidence", "Retain prompts, responses, verdicts, and remediation guidance.", bool(findings)),
                ("Executive reporting", "Summarize business exposure and remediation progress for stakeholders.", False),
            ]
            for title, description, complete in checklist:
                st.markdown(
                    f"""
                    <div style="display:flex; gap:10px; margin-bottom:10px; align-items:flex-start;">
                        <div style="width:18px; height:18px; border-radius:50%; background:{COLORS['accent']}24; color:{COLORS['accent']}; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;">{'✓' if complete else '○'}</div>
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
                <div style="border:1px solid {COLORS['border']}; border-radius:12px; padding:16px; background:{COLORS['elevated']};">
                     <div style="color:{COLORS['text_secondary']}; font-size:12px; margin-bottom:8px;">Recommended next action</div>
                     <div style="color:{COLORS['text_primary']}; font-size:17px; font-weight:700; margin-bottom:8px;">{'Review critical exposure' if critical_count else ('Review assessment evidence' if history else 'Launch a baseline assessment')}</div>
                     <div style="color:{COLORS['text_secondary']}; font-size:12.8px; line-height:1.55; margin-bottom:14px;">{f'{critical_count} critical findings require immediate evidence review and remediation ownership.' if critical_count else ('Your latest run is ready for analyst review and stakeholder reporting.' if history else 'Connect an authorized target and establish your initial security posture.')}</div>
                    <div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:12px; color:{COLORS['text_secondary']};">
                         <span>Risk status</span><span style="color:{COLORS['critical'] if critical_count else COLORS['accent']};">{'Critical' if critical_count else ('Monitored' if history else 'Not assessed')}</span>
                    </div>
                    <div style="height:8px; border-radius:999px; background:{COLORS['elevated']}; margin-top:8px; overflow:hidden;">
                         <div style="width:{'88' if critical_count else ('42' if history else '8')}%; height:100%; background:linear-gradient(90deg,{COLORS['accent']},{COLORS['critical'] if critical_count else COLORS['low']});"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Page content
# ---------------------------------------------------------------------------
render_dashboard_header()

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
        if total == 0:
            st.markdown(f"<div style='padding:30px 4px; color:{COLORS['text_secondary']};'>No finding distribution yet. Launch an assessment to establish a baseline.</div>", unsafe_allow_html=True)
        else:
            fig = go.Figure()
            sev_colors = {
                "critical": COLORS["critical"], "high": COLORS["high"],
                "medium": COLORS["medium"], "low": COLORS["low"], "info": COLORS["info"],
            }
            for sev, count in risk.items():
                if not count:
                    continue
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
    if not runs:
        st.markdown(f"<div style='padding:24px 2px; color:{COLORS['text_secondary']};'>No assessments yet. Your authorized runs will appear here with evidence and severity counts.</div>", unsafe_allow_html=True)
        st.stop()
    header_cols = st.columns([2.2, 1.6, 1, 0.8, 0.8, 1.4])
    for col, label in zip(header_cols, ["Target", "Type", "Status", "Crit.", "High", "Timestamp"]):
        col.markdown(f"<span style='color:{COLORS['text_secondary']}; font-size:12px;'>{label}</span>", unsafe_allow_html=True)
    st.markdown(f"<hr style='margin:6px 0; border-color:{COLORS['border']};'>", unsafe_allow_html=True)
    for row in runs:
        cols = st.columns([2.2, 1.6, 1, 0.8, 0.8, 1.4])
        cols[0].markdown(f"<span style='font-size:13.5px;'>{row['Target']}</span>", unsafe_allow_html=True)
        cols[1].markdown(f"<span style='font-size:13.5px; color:{COLORS['text_secondary']};'>{row['Type']}</span>", unsafe_allow_html=True)
        cols[2].markdown(status_pill(row["Status"]), unsafe_allow_html=True)
        cols[3].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:13px;'>{row['Critical']}</span>", unsafe_allow_html=True)
        cols[4].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:13px;'>{row['High']}</span>", unsafe_allow_html=True)
        cols[5].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:12px; color:{COLORS['text_secondary']};'>{row['Timestamp']}</span>", unsafe_allow_html=True)
