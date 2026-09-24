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

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


def apply_theme():
    """Inject global CSS. Call once, right after st.set_page_config()."""
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
        div[data-testid="stSidebarNav"] a:hover {{
            background-color: {COLORS['elevated']};
            color: {COLORS['text_primary']} !important;
        }}
        div[data-testid="stSidebarNav"] a[aria-current="page"] {{
            background-color: {COLORS['elevated']};
            color: {COLORS['accent']} !important;
            font-weight: 600;
            border-left: 2px solid {COLORS['accent']};
        }}

        .sidebar-brand {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 18px 16px 14px 16px;
            border-bottom: 1px solid {COLORS['border']};
            margin-bottom: 6px;
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


def sidebar_brand():
    """Render the SecMate brand block at the top of the sidebar."""
    st.sidebar.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="mark">SM</div>
            <div>
                <div class="name">SecMate</div>
                <div class="tag">AI Security Assessment</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
    st.sidebar.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.switch_page("app.py")
