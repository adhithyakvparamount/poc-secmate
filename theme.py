"""
theme.py — SecMate visual design system.

This module is FRONTEND ONLY. It defines colors, typography, CSS,
and small HTML-rendering helpers used across every page. It does not
call any backend / model / scanning logic.

Usage in any page:
    import streamlit as st
    from theme import apply_theme, get_active_colors, metric_card, severity_badge, status_pill

    st.set_page_config(page_title="SecMate", layout="wide")
    apply_theme()
"""

from datetime import datetime
from html import escape

import streamlit as st

# ---------------------------------------------------------------------------
# Color tokens
# ---------------------------------------------------------------------------
COLORS = {
    "canvas": "#0A0E14",
    "surface": "#111827",
    "elevated": "#1C2333",
    "border": "#2D3548",
    "accent": "#8B7CF6",
    "accent_dim": "#6D5FDB",
    "accent_text": "#FFFFFF",
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
    "SecMate Dark": {"canvas": "#090D15", "surface": "#121927", "elevated": "#202A3D", "border": "#5A6A87", "accent": "#A597FF", "accent_dim": "#6657D6", "accent_text": "#FFFFFF", "text_primary": "#F1F5FB", "text_secondary": "#AAB5C8"},
    "Claude Dark": {"canvas": "#171715", "surface": "#23221E", "elevated": "#33312B", "border": "#706B60", "accent": "#F09A79", "accent_dim": "#A9472D", "accent_text": "#FFFFFF", "text_primary": "#FFF9F0", "text_secondary": "#C5BDB0"},
    "ChatGPT Dark": {"canvas": "#151515", "surface": "#212121", "elevated": "#303030", "border": "#6B6B6B", "accent": "#4DDBAE", "accent_dim": "#087A60", "accent_text": "#FFFFFF", "text_primary": "#F5F5F5", "text_secondary": "#BDBDBD"},
    "Blue Cyber": {"canvas": "#06101D", "surface": "#0D1B2D", "elevated": "#172D49", "border": "#4779A8", "accent": "#70B7FF", "accent_dim": "#2563C7", "accent_text": "#FFFFFF", "text_primary": "#F2F8FF", "text_secondary": "#ADC2DA"},
    "White": {"canvas": "#F4F6F9", "surface": "#FFFFFF", "elevated": "#E9EEF5", "border": "#7A889D", "accent": "#2563EB", "accent_dim": "#1D4ED8", "accent_text": "#FFFFFF", "text_primary": "#111827", "text_secondary": "#526176"},
}

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


def get_active_colors():
    """Return the palette selected for the current Streamlit session."""
    theme_name = st.session_state.get("dashboard_theme", "SecMate Dark")
    return {**COLORS, **THEME_PRESETS.get(theme_name, THEME_PRESETS["SecMate Dark"])}


def apply_theme():
    """Inject global CSS. Call once, right after st.set_page_config()."""
    theme_name = st.session_state.get("dashboard_theme", "SecMate Dark")
    active = get_active_colors()
    color_scheme = "light" if theme_name == "White" else "dark"
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            color-scheme: {color_scheme};
        }}

        .stApp {{
            background-color: {active['canvas']};
            color: {active['text_primary']};
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {active['surface']};
            border-right: 1px solid {active['border']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {active['text_primary']};
        }}
        div[data-testid="stSidebarNav"] a {{
            border-radius: 6px;
            padding: 8px 12px !important;
            margin: 2px 8px;
            font-size: 14px;
            color: {active['text_secondary']} !important;
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
            background-color: {active['elevated']};
            color: {active['text_primary']} !important;
        }}
        div[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background: linear-gradient(90deg, {active['accent']}26, {active['elevated']});
            color: {active['accent']} !important;
            font-weight: 600;
            border-left: 2px solid {active['accent']};
        }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 16px 10px 14px 10px;
            border-bottom: 1px solid {active['border']};
            border-top: 1px solid {active['border']};
            margin: 42px 16px 8px 16px;
        }}
        .sidebar-brand .mark {{
            width: 28px; height: 28px;
            border-radius: 6px;
            background: linear-gradient(135deg, {active['accent']}, {active['accent_dim']});
            display: flex; align-items: center; justify-content: center;
            font-weight: 700; color: {active['accent_text']}; font-size: 14px;
        }}
        .sidebar-brand .name {{
            font-weight: 600; font-size: 15px; color: {active['text_primary']};
            letter-spacing: 0.2px;
        }}
        .sidebar-brand .tag {{
            font-size: 11px; color: {active['text_secondary']};
        }}

        .sidebar-account {{
            margin: 8px 16px 12px 16px;
            padding: 10px;
            border: 1px solid {active['border']};
            border-radius: 10px;
            background: {active['elevated']};
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
            background: linear-gradient(135deg, {active['accent']}, {active['low']});
            color: {active['accent_text']};
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 12px;
        }}
        .sidebar-user-name {{
            color: {active['text_primary']};
            font-size: 13px;
            font-weight: 600;
            line-height: 1.2;
        }}
        .sidebar-user-role {{
            color: {active['text_secondary']};
            font-size: 11px;
            margin-top: 2px;
        }}
        .sidebar-link {{
            display: flex;
            align-items: center;
            gap: 9px;
            padding: 8px 9px;
            color: {active['text_secondary']};
            border-radius: 7px;
            font-size: 13px;
            text-decoration: none;
        }}
        .sidebar-link:hover {{
            background: {active['elevated']};
            color: {active['text_primary']};
        }}
        .sidebar-icon {{
            width: 15px;
            height: 15px;
            display: inline-flex;
            color: {active['text_secondary']};
        }}
        section[data-testid="stSidebar"] .stButton > button {{
            margin: 4px 16px 0 16px;
            width: calc(100% - 32px);
            background: transparent;
            color: {active['text_secondary']};
            border: 1px solid {active['border']};
            border-radius: 8px;
            font-weight: 500;
            padding: 8px 12px;
            text-align: left;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(240,68,82,0.08);
            color: {active['critical']};
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
            background-color: {active['surface']};
            border: 1px solid {active['border']} !important;
            border-radius: 10px;
        }}

        /* ---- Metric cards ---- */
        .metric-card {{
            background-color: {active['surface']};
            border: 1px solid {active['border']};
            border-radius: 10px;
            padding: 16px 18px;
        }}
        .metric-card .label {{
            font-size: 12.5px; color: {active['text_secondary']};
            margin-bottom: 6px;
        }}
        .metric-card .value {{
            font-size: 26px; font-weight: 600; color: {active['text_primary']};
            font-family: 'JetBrains Mono', monospace;
        }}
        .metric-card .delta-up {{ color: {active['accent']}; font-size: 12.5px; }}
        .metric-card .delta-down {{ color: {active['critical']}; font-size: 12.5px; }}

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
        .badge-critical {{ background: rgba(240,68,82,0.18); color: {active['critical']}; }}
        .badge-high     {{ background: rgba(255,138,61,0.18); color: {active['high']}; }}
        .badge-medium   {{ background: rgba(245,197,66,0.18); color: {active['medium']}; }}
        .badge-low      {{ background: rgba(74,158,255,0.18); color: {active['low']}; }}
        .badge-info     {{ background: rgba(92,107,135,0.22); color: {active['info']}; }}

        /* ---- Status pills (run status, not severity) ---- */
        .pill {{
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 11.5px;
            font-weight: 500;
        }}
        .pill-complete {{ background: {active['accent']}26; color: {active['accent']}; }}
        .pill-running  {{ background: rgba(74,158,255,0.18); color: {active['low']}; }}
        .pill-failed   {{ background: rgba(240,68,82,0.18); color: {active['critical']}; }}
        .pill-pending  {{ background: {active['elevated']}; color: {active['text_secondary']}; }}

        /* ---- Findings row (severity edge bar) ---- */
        .finding-row {{
            background: {active['surface']};
            border: 1px solid {active['border']};
            border-left: 3px solid var(--sev-color);
            border-radius: 6px;
            padding: 12px 14px;
            margin-bottom: 8px;
        }}
        .finding-title {{ font-weight: 600; font-size: 14px; color: {active['text_primary']}; }}
        .finding-meta {{ font-size: 12px; color: {active['text_secondary']}; margin-top: 2px; }}

        /* ---- Transcript cards (Red / Blue team) ---- */
        .transcript-card {{
            border: 1px solid {active['border']};
            border-radius: 8px;
            padding: 12px 14px;
            margin-bottom: 10px;
        }}
        .transcript-prompt {{ background: {active['accent']}12; border-left: 3px solid {active['accent']}; }}
        .transcript-response {{ background: rgba(74,158,255,0.10); border-left: 3px solid {active['low']}; }}
        .transcript-label {{
            font-size: 11px; text-transform: none; color: {active['text_secondary']};
            margin-bottom: 6px; font-weight: 500;
        }}
        .transcript-body {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 13px; color: {active['text_primary']};
            white-space: pre-wrap; line-height: 1.5;
        }}

        /* ---- Buttons ---- */
        .stButton > button {{
            background-color: {active['accent_dim']};
            color: {active['accent_text']};
            border: 1px solid {active['accent_dim']};
            border-radius: 6px;
            font-weight: 600;
            padding: 6px 18px;
        }}
        .stButton > button:hover {{
            background-color: {active['accent']};
            color: {active['accent_text']};
            border-color: {active['accent']};
        }}

        /* ---- Section headers ---- */
        .section-title {{
            font-size: 15px; font-weight: 600; color: {active['text_primary']};
            margin-bottom: 10px;
        }}

        /* ---- Theme-aware text and controls ---- */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
        .stApp label, .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stWidgetLabel"] {{
            color: {active['text_primary']};
        }}
        .stApp [data-testid="stCaptionContainer"],
        .stApp small {{
            color: {active['text_secondary']} !important;
        }}
        .stApp hr {{ border-color: {active['border']}; }}

        .stApp input,
        .stApp textarea,
        .stApp [data-baseweb="select"] > div,
        .stApp [data-baseweb="base-input"] {{
            background-color: {active['elevated']} !important;
            color: {active['text_primary']} !important;
            border-color: {active['border']} !important;
        }}
        .stApp input::placeholder,
        .stApp textarea::placeholder {{
            color: {active['text_secondary']} !important;
            opacity: 0.8;
        }}
        .stApp input:focus,
        .stApp textarea:focus,
        .stApp [data-baseweb="select"] > div:focus-within {{
            border-color: {active['accent']} !important;
            box-shadow: 0 0 0 1px {active['accent']} !important;
        }}

        [data-baseweb="popover"],
        [data-baseweb="menu"],
        [role="listbox"] {{
            background-color: {active['surface']} !important;
            color: {active['text_primary']} !important;
            border-color: {active['border']} !important;
        }}
        [role="option"] {{
            color: {active['text_primary']} !important;
        }}
        [role="option"]:hover,
        [role="option"][aria-selected="true"] {{
            background-color: {active['elevated']} !important;
        }}
        [data-baseweb="tag"] {{
            background-color: {active['accent_dim']} !important;
            color: {active['accent_text']} !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            border-bottom: 1px solid {active['border']};
        }}
        .stTabs [data-baseweb="tab"] {{
            color: {active['text_secondary']};
        }}
        .stTabs [aria-selected="true"] {{
            color: {active['accent']} !important;
            border-bottom-color: {active['accent']} !important;
        }}

        [data-testid="stExpander"],
        [data-testid="stFileUploaderDropzone"],
        [data-testid="stPopoverBody"] {{
            background-color: {active['surface']} !important;
            color: {active['text_primary']} !important;
            border-color: {active['border']} !important;
        }}
        [data-testid="stAlert"] {{
            background-color: {active['elevated']} !important;
            color: {active['text_primary']} !important;
            border-color: {active['border']} !important;
        }}

        [data-baseweb="checkbox"] [aria-checked="true"],
        [data-baseweb="radio"] [aria-checked="true"],
        [data-testid="stToggle"] [data-checked="true"] {{
            background-color: {active['accent_dim']} !important;
            border-color: {active['accent_dim']} !important;
        }}
        [data-baseweb="slider"] [role="slider"] {{
            background-color: {active['accent_dim']} !important;
            border-color: {active['accent_text']} !important;
        }}

        [data-testid="stDataFrame"],
        [data-testid="stTable"] {{
            color: {active['text_primary']};
            border-color: {active['border']};
        }}

        /* ---- Notification center ---- */
        [data-testid="stPopover"] > button {{
            background: {active['surface']} !important;
            color: {active['text_primary']} !important;
            border: 1px solid {active['border']} !important;
            border-radius: 10px !important;
        }}
        [data-testid="stPopover"] > button:hover {{
            background: {active['elevated']} !important;
            border-color: {active['accent']} !important;
        }}
        .notification-item {{
            background: {active['elevated']};
            border: 1px solid {active['border']};
            border-left: 3px solid var(--notification-color);
            border-radius: 8px;
            padding: 10px 12px;
            margin-bottom: 8px;
        }}
        .notification-title {{
            color: {active['text_primary']};
            font-size: 13px;
            font-weight: 700;
        }}
        .notification-message {{
            color: {active['text_secondary']};
            font-size: 12px;
            line-height: 1.45;
            margin-top: 3px;
        }}
        .notification-time {{
            color: {active['text_secondary']};
            font-family: 'JetBrains Mono', monospace;
            font-size: 10.5px;
            margin-top: 6px;
        }}

        /* ---- Misc cleanup ---- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{background: transparent;}}
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


def add_notification(title: str, message: str, level: str = "info", notification_id: str | None = None):
    """Add one unread session notification, avoiding duplicate IDs."""
    notifications = st.session_state.setdefault("notifications", [])
    item_id = notification_id or f"notification-{datetime.now().timestamp()}"
    if any(item.get("id") == item_id for item in notifications):
        return
    notifications.insert(
        0,
        {
            "id": item_id,
            "title": title,
            "message": message,
            "level": level,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "unread": True,
        },
    )
    del notifications[20:]


def notification_center():
    """Render the session notification popover at the top-right of a page."""
    if not st.session_state.get("notification_center_initialized"):
        add_notification(
            "Notification center ready",
            "Assessment completions and new findings will appear here.",
            notification_id="notification-center-ready",
        )
        st.session_state.notification_center_initialized = True

    notifications = st.session_state.get("notifications", [])
    unread_count = sum(bool(item.get("unread")) for item in notifications)
    _, notification_col = st.columns([0.82, 0.18])
    with notification_col:
        label = f"Notifications ({unread_count})" if unread_count else "Notifications"
        with st.popover(
            label,
            icon=":material/notifications:",
            width="stretch",
            key="notification_center_popover",
        ):
            st.markdown("#### Notifications")
            if not notifications:
                st.caption("No notifications yet.")
            else:
                level_colors = {
                    "critical": COLORS["critical"],
                    "warning": COLORS["high"],
                    "success": get_active_colors()["accent"],
                    "info": COLORS["low"],
                }
                for item in notifications:
                    unread_marker = "New - " if item.get("unread") else ""
                    color = level_colors.get(str(item.get("level")), COLORS["info"])
                    st.markdown(
                        f"""
                        <div class="notification-item" style="--notification-color:{color};">
                            <div class="notification-title">{unread_marker}{escape(str(item.get('title', 'Notification')))}</div>
                            <div class="notification-message">{escape(str(item.get('message', '')))}</div>
                            <div class="notification-time">{escape(str(item.get('created_at', '')))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                mark_col, clear_col = st.columns(2)
                with mark_col:
                    if st.button("Mark all read", use_container_width=True, key="notifications_mark_read"):
                        for item in notifications:
                            item["unread"] = False
                        st.rerun()
                with clear_col:
                    if st.button("Clear", use_container_width=True, key="notifications_clear"):
                        st.session_state.notifications = []
                        st.rerun()


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
        st.session_state.pop("notifications", None)
        st.session_state.pop("notification_center_initialized", None)
        st.switch_page("app.py")
