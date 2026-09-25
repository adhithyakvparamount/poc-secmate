"""
5_Integrations.py — External security tool integrations.

VISUAL MOCKUP NOTICE:
Integration controls are placeholders. Connect these buttons to real
credential storage and third-party APIs before production use.
"""

import streamlit as st
from theme import apply_theme, sidebar_brand, get_active_colors, notification_center, logout_button
from authcheck import require_auth
from workspace import t

st.set_page_config(page_title="SecMate — Integrations", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(
    f"<div class='page-kicker'>SECURITY ECOSYSTEM</div>"
    f"<div class='page-title'>{t('integrations')}</div>"
    f"<div class='page-subtitle'>{t('integrations_subtitle')}</div>",
    unsafe_allow_html=True,
)

integrations = [
    {"name": "Jira", "description": "Create remediation tickets from validated findings.", "status": "Not connected"},
    {"name": "Slack", "description": "Send critical-finding alerts to security channels.", "status": "Not connected"},
    {"name": "Microsoft Sentinel", "description": "Forward audit events and assessment telemetry.", "status": "Coming soon"},
    {"name": "GitHub", "description": "Attach reports and evidence to security review issues.", "status": "Not connected"},
]

cols = st.columns(2)
for index, integration in enumerate(integrations):
    with cols[index % 2]:
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; gap:16px; align-items:flex-start;">
                    <div>
                        <div style="font-size:16px; font-weight:700; color:{COLORS['text_primary']};">{integration['name']}</div>
                        <div style="font-size:12.8px; color:{COLORS['text_secondary']}; margin-top:6px; line-height:1.5;">{integration['description']}</div>
                    </div>
                    <div style="border:1px solid {COLORS['border']}; border-radius:999px; padding:4px 9px; color:{COLORS['text_secondary']}; font-size:11px; white-space:nowrap;">{integration['status']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            st.button("Configure", key=f"integration_{integration['name']}", disabled=True, help="Connection credentials and provider APIs are not configured in this build.")
