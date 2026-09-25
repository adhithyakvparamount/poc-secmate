"""
theme.py — SecMate visual design system.

This module is FRONTEND ONLY. It defines colors, typography, CSS,
and small HTML-rendering helpers used across every page. It does not
call any backend / model / scanning logic.

Usage in any page:
    import streamlit as st
    from theme import apply_theme, COLORS, metric_card, severity_badge, status_pill

    st.set_page_config(page_title="SecMate", layout="wide")
    apply_theme()
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Color tokens
# ---------------------------------------------------------------------------
COLORS = {
    "canvas": "#0A0E14",
    "surface": "#111827",
    "elevated": "#1C2333",
    "border": "#2D3548",
    "accent": "#00D9A3",
    "accent_dim": "#0AA37D",
    "text_primary": "#E2E8F0",
    "text_secondary": "#8B94A7",
    # Severity scale — reserved for risk indication only, never decoration
    "critical": "#F04452",
    "high": "#FF8A3D",
    "medium": "#F5C542",
    "low": "#4A9EFF",
    "info": "#5C6B87",
}

THEME_PRESETS = {
    "SecMate Dark": {"canvas": "#0A0E14", "surface": "#111827", "elevated": "#1C2333", "border": "#2D3548", "accent": "#00D9A3", "accent_dim": "#0AA37D", "text_primary": "#E2E8F0", "text_secondary": "#8B94A7"},
    "Claude Dark": {"canvas": "#171717", "surface": "#20201D", "elevated": "#30302C", "border": "#3B3B35", "accent": "#D97757", "accent_dim": "#B85F43", "text_primary": "#F4F1EA", "text_secondary": "#AAA49A"},
    "ChatGPT Dark": {"canvas": "#212121", "surface": "#171717", "elevated": "#2F2F2F", "border": "#3A3A3A", "accent": "#10A37F", "accent_dim": "#0E8F70", "text_primary": "#ECECEC", "text_secondary": "#AFAFAF"},
    "Blue Cyber": {"canvas": "#07111F", "surface": "#0E1B2E", "elevated": "#162A45", "border": "#274463", "accent": "#4A9EFF", "accent_dim": "#2F6FED", "text_primary": "#EAF3FF", "text_secondary": "#93A8C3"},
    "White": {"canvas": "#F7F8FA", "surface": "#FFFFFF", "elevated": "#EEF2F7", "border": "#D8DEE8", "accent": "#2563EB", "accent_dim": "#1D4ED8", "text_primary": "#111827", "text_secondary": "#667085"},
}

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


def apply_theme():
    """Inject global CSS. Call once, right after st.set_page_config()."""
    theme_name = st.session_state.get("dashboard_theme", "SecMate Dark")
    active = {**COLORS, **THEME_PRESETS.get(theme_name, THEME_PRESETS["SecMate Dark"])}
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {COLORS['canvas']};
            color: {COLORS['text_primary']};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['surface']};
            border-right: 1px solid {COLORS['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['text_primary']};
        }}
        div[data-testid="stSidebarNav"] a {{
            border-radius: 6px;
            padding: 8px 12px !important;
            margin: 2px 8px;
            font-size: 14px;
            color: {COLORS['text_secondary']} !important;
        }}
        div[data-testid="stSidebarNav"] a[href$="/Settings"],
        div[data-testid="stSidebarNav"] a[href$="Settings"],
        div[data-testid="stSidebarNav"] a[href$="/Profile"],
        div[data-testid="stSidebarNav"] a[href$="Profile"] {{
            display: none !important;
        }}
        div[data-testid="stSidebarNav"] ul li:first-child a span {{
            display: none;
        }}
        div[data-testid="stSidebarNav"] ul li:first-child a::after {{
            content: "Dashboard";
        }}
        div[data-testid="stSidebarNav"] a:hover {{
            background-color: {COLORS['elevated']};
            color: {COLORS['text_primary']} !important;
        }}
        div[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: linear-gradient(90deg, rgba(0,217,163,0.12), {COLORS['elevated']});
            color: {COLORS['accent']} !important;
            font-weight: 600;
            border-left: 2px solid {COLORS['accent']};
        }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 16px 10px 14px 10px;
            border-bottom: 1px solid {COLORS['border']};
            border-top: 1px solid {COLORS['border']};
            margin: 42px 16px 8px 16px;
        }}
        .sidebar-brand .mark {{
            width: 28px; height: 28px;
            border-radius: 6px;
            background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['accent_dim']});
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; color: {COLORS['canvas']}; font-size: 14px;
        }}
        .sidebar-brand .name {{
            font-weight: 600; font-size: 15px; color: {COLORS['text_primary']};
            letter-spacing: 0.2px;
        }}
        .sidebar-brand .tag {{
            font-size: 11px; color: {COLORS['text_secondary']};
        }}

        .sidebar-account {{
            margin: 8px 16px 12px 16px;
            padding: 10px;
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            background: rgba(255,255,255,0.02);
        }}
        .sidebar-profile {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .sidebar-avatar {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: linear-gradient(135deg, {COLORS['accent']}, {COLORS['low']});
            color: {COLORS['canvas']};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 12px;
        }}
        .sidebar-user-name {{
            color: {COLORS['text_primary']};
            font-size: 13px;
            font-weight: 600;
            line-height: 1.2;
        }}
        .sidebar-user-role {{
            color: {COLORS['text_secondary']};
            font-size: 11px;
            margin-top: 2px;
        }}
        .sidebar-link {{
            display: flex;
            align-items: center;
            gap: 9px;
            padding: 8px 9px;
            color: {COLORS['text_secondary']};
            border-radius: 7px;
            font-size: 13px;
            text-decoration: none;
        }}
        .sidebar-link:hover {{
            background: {COLORS['elevated']};
            color: {COLORS['text_primary']};
        }}
        .sidebar-icon {{
            width: 15px;
            height: 15px;
            display: inline-flex;
            color: {COLORS['text_secondary']};
        }}
        section[data-testid="stSidebar"] .stButton > button {{
            margin: 4px 16px 0 16px;
            width: calc(100% - 32px);
            background: transparent;
            color: {COLORS['text_secondary']};
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            font-weight: 500;
            padding: 8px 12px;
            text-align: left;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(240,68,82,0.08);
            color: {COLORS['critical']};
            border-color: rgba(240,68,82,0.35);
        }}
        section[data-testid="stSidebar"] .stButton > button::before {{
            content: "";
            width: 15px;
            height: 15px;
            display: inline-block;
            margin-right: 9px;
            vertical-align: -2px;
            background-color: currentColor;
            -webkit-mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M15 12H3m0 0 4-4m-4 4 4 4m5-10V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-1'/%3E%3C/svg%3E") center / contain no-repeat;
            mask: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='black' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M15 12H3m0 0 4-4m-4 4 4 4m5-10V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-1'/%3E%3C/svg%3E") center / contain no-repeat;
        }}

        /* ---- Cards ---- */
        div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']} !important;
            border-radius: 10px;
        }}

        /* ---- Metric cards ---- */
        .metric-card {{
            background-color: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 10px;
            padding: 16px 18px;
        }}
        .metric-card .label {{
            font-size: 12.5px; color: {COLORS['text_secondary']};
            margin-bottom: 6px;
        }}
        .metric-card .value {{
            font-size: 26px; font-weight: 600; color: {COLORS['text_primary']};
            font-family: 'JetBrains Mono', monospace;
        }}
        .metric-card .delta-up {{ color: {COLORS['accent']}; font-size: 12.5px; }}
        .metric-card .delta-down {{ color: {COLORS['critical']}; font-size: 12.5px; }}

        /* ---- Badges (severity) ---- */
        .badge {{
            display: inline-block;
            padding: 2px 9px;
            border-radius: 4px;
            font-size: 11.5px;
            font-weight: 600;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.3px;
        }}
        .badge-critical {{ background: rgba(240,68,82,0.15); color: {COLORS['critical']}; }}
        .badge-high     {{ background: rgba(255,138,61,0.15); color: {COLORS['high']}; }}
        .badge-medium   {{ background: rgba(245,197,66,0.15); color: {COLORS['medium']}; }}
        .badge-low      {{ background: rgba(74,158,255,0.15); color: {COLORS['low']}; }}
        .badge-info     {{ background: rgba(92,107,135,0.20); color: {COLORS['info']}; }}

        /* ---- Status pills (run status, not severity) ---- */
        .pill {{
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11.5px;
            font-weight: 500;
        }}
        .pill-complete {{ background: rgba(0,217,163,0.15); color: {COLORS['accent']}; }}
        .pill-running  {{ background: rgba(74,158,255,0.15); color: {COLORS['low']}; }}
        .pill-failed   {{ background: rgba(240,68,82,0.15); color: {COLORS['critical']}; }}
        .pill-pending  {{ background: rgba(139,148,167,0.15); color: {COLORS['text_secondary']}; }}

        /* ---- Findings row (severity edge bar) ---- */
        .finding-row {{
            background: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-left: 3px solid var(--sev-color);
            border-radius: 6px;
            padding: 12px 14px;
            margin-bottom: 8px;
        }}
        .finding-title {{ font-weight: 600; font-size: 14px; color: {COLORS['text_primary']}; }}
        .finding-meta {{ font-size: 12px; color: {COLORS['text_secondary']}; margin-top: 2px; }}

        /* ---- Transcript cards (Red / Blue team) ---- */
        .transcript-card {{
            border: 1px solid {COLORS['border']};
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 10px;
        }}
        .transcript-prompt {{ background: rgba(0,217,163,0.06); border-left: 3px solid {COLORS['accent']}; }}
        .transcript-response {{ background: rgba(74,158,255,0.06); border-left: 3px solid {COLORS['low']}; }}
        .transcript-label {{
            font-size: 11px; text-transform: none; color: {COLORS['text_secondary']};
            margin-bottom: 6px; font-weight: 500;
        }}
        .transcript-body {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px; color: {COLORS['text_primary']};
            white-space: pre-wrap; line-height: 1.5;
        }}

        /* ---- Buttons ---- */
        .stButton > button {{
            background-color: {COLORS['accent']};
            color: {COLORS['canvas']};
            border: none;
            border-radius: 6px;
            font-weight: 600;
            padding: 6px 18px;
        }}
        .stButton > button:hover {{
            background-color: {COLORS['accent_dim']};
            color: {COLORS['canvas']};
        }}

        /* ---- Section headers ---- */
        .section-title {{
            font-size: 15px; font-weight: 600; color: {COLORS['text_primary']};
            margin-bottom: 10px;
        }}

        /* ---- Misc cleanup ---- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {active['canvas']} !important; }}
        section[data-testid="stSidebar"] {{ background-color: {active['surface']} !important; }}
        section[data-testid="stSidebar"] *, .stApp {{ color: {active['text_primary']}; }}
        div[data-testid="stSidebarNav"] a {{ color: {active['text_secondary']} !important; }}
        div[data-testid="stSidebarNav"] a:hover {{ background-color: {active['elevated']} !important; }}
        div[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: linear-gradient(90deg, {active['accent']}22, {active['elevated']}) !important;
            color: {active['accent']} !important;
            border-left-color: {active['accent']} !important;
        }}
        .sidebar-brand .mark, .stButton > button {{ background: {active['accent']} !important; }}
        .sidebar-avatar {{ background: linear-gradient(135deg, {active['accent']}, {COLORS['low']}) !important; }}
        .metric-card, div[data-testid="stVerticalBlockBorderWrapper"] > div {{
            background-color: {active['surface']} !important;
            border-color: {active['border']} !important;
        }}
        .metric-card .label, .sidebar-user-role, .sidebar-link, .section-title + div,
        [data-testid="stMarkdownContainer"] p {{ color: {active['text_secondary']}; }}
        .metric-card .value, .section-title, .sidebar-user-name {{ color: {active['text_primary']} !important; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_brand():
    """Render the SecMate brand and account block in the sidebar."""
    user_email = st.session_state.get("user_email", "adhithya@example.com")
    display_name = st.session_state.get("display_name", "Adhithya K V")
    plan_name = st.session_state.get("plan_name", "Free")
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="mark">SM</div>
            <div>
                <div class="name">SecMate</div>
                <div class="tag">AI Security Assessment</div>
            </div>
        </div>
        <div class="sidebar-account">
            <div class="sidebar-profile">
                <div class="sidebar-avatar">AD</div>
                <div>
                    <div class="sidebar-user-name">{display_name}</div>
                    <div class="sidebar-user-role">{plan_name} plan</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar.popover("Profile", use_container_width=True):
        st.markdown(f"**{display_name}**")
        st.caption(user_email)
        st.markdown(f"Plan: **{plan_name}**")
        plan = st.radio("Account type", ["Free", "Paid"], index=0 if plan_name == "Free" else 1, horizontal=True)
        st.session_state.plan_name = plan
        st.text_input("Name", value=display_name, key="display_name")
        st.caption("Profile changes are visual only in this mockup.")

    with st.sidebar.popover("Settings", use_container_width=True):
        st.markdown("**Settings**")
        theme_names = list(THEME_PRESETS.keys())
        current_theme = st.session_state.get("dashboard_theme", "SecMate Dark")
        st.selectbox("Dashboard theme", theme_names, index=theme_names.index(current_theme), key="dashboard_theme")
        st.selectbox("Language", ["English", "Hindi", "Arabic", "French"], key="language_pref")
        st.selectbox("Dashboard density", ["Comfortable", "Compact", "Spacious"], key="dashboard_density")
        st.toggle("Reduced motion", key="reduced_motion")
        st.divider()
        st.button("Upgrade plan", use_container_width=True)
        st.button("Get apps and extensions", use_container_width=True)
        st.button("Learn more", use_container_width=True)
        st.button("Get help", use_container_width=True)


def metric_card(label: str, value: str, delta: str = None, delta_positive: bool = True):
    """Render a single metric card. `value` is pre-formatted (e.g. '128', '94%')."""
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_positive else "delta-down"
        arrow = "▲" if delta_positive else "▼"
        delta_html = f'<div class="{cls}">{arrow} {delta}</div>'
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_badge(severity: str) -> str:
    """Return HTML for a severity badge. severity: critical/high/medium/low/info."""
    sev = severity.lower()
    return f'<span class="badge badge-{sev}">{sev.upper()}</span>'


def status_pill(status: str) -> str:
    """Return HTML for a run-status pill. status: complete/running/failed/pending."""
    s = status.lower()
    return f'<span class="pill pill-{s}">{status.title()}</span>'


def logout_button():
    """Render a 'Log out' control at the bottom of the sidebar."""
    st.sidebar.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.onboarding_seen = False
        st.session_state.onboarding_loading = False
        st.switch_page("app.py")
