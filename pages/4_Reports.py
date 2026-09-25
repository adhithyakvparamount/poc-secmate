"""
4_Reports.py — Generated report listing and export.

VISUAL MOCKUP NOTICE:
"Generate New Report" and "Download" are visual only. Wire them to
your existing backend's report-generation function and file output.
"""

import streamlit as st
from theme import apply_theme, sidebar_brand, get_active_colors, notification_center, logout_button
from authcheck import require_auth

st.set_page_config(page_title="SecMate — Reports", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown("### Reports")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Generate and download assessment reports for stakeholders and audit trails.</div>",
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([3, 1])
with col_b:
    st.selectbox("Report scope", ["Full Assessment", "Red Team Only", "VAPT Only", "Executive Summary"], label_visibility="collapsed")
    st.button("Generate New Report", use_container_width=True)


# ---------------------------------------------------------------------------
# MOCK DATA — replace with backend calls
# ---------------------------------------------------------------------------
def get_reports():
    return [
        {"name": "PolicyMate Agent v2.3 — Full Assessment", "date": "2026-09-24", "format": "PDF", "size": "1.2 MB"},
        {"name": "Support Bot v1.8 — VAPT Summary", "date": "2026-09-22", "format": "PDF", "size": "640 KB"},
        {"name": "PolicyMate Agent v2.3 — Executive Summary", "date": "2026-09-18", "format": "PDF", "size": "310 KB"},
        {"name": "Internal Copilot — Full Assessment", "date": "2026-09-14", "format": "PDF", "size": "980 KB"},
    ]


with st.container(border=True):
    reports = get_reports()
    header = st.columns([3, 1.2, 0.8, 0.8, 1])
    for col, label in zip(header, ["Report", "Date", "Format", "Size", ""]):
        col.markdown(f"<span style='color:{COLORS['text_secondary']}; font-size:12px;'>{label}</span>", unsafe_allow_html=True)
    st.markdown(f"<hr style='margin:6px 0; border-color:{COLORS['border']};'>", unsafe_allow_html=True)
    for r in reports:
        cols = st.columns([3, 1.2, 0.8, 0.8, 1])
        cols[0].markdown(f"<span style='font-size:13.5px;'>{r['name']}</span>", unsafe_allow_html=True)
        cols[1].markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:12.5px; color:{COLORS['text_secondary']};'>{r['date']}</span>", unsafe_allow_html=True)
        cols[2].markdown(f"<span style='font-size:12.5px;'>{r['format']}</span>", unsafe_allow_html=True)
        cols[3].markdown(f"<span style='font-size:12.5px; color:{COLORS['text_secondary']};'>{r['size']}</span>", unsafe_allow_html=True)
        cols[4].button("Download", key=f"dl_{r['name']}", use_container_width=True)
