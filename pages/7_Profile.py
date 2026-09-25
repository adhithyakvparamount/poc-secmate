"""
7_Profile.py — User profile page.

VISUAL MOCKUP NOTICE:
Profile controls are frontend placeholders and do not persist yet.
"""

import streamlit as st
from theme import apply_theme, sidebar_brand, get_active_colors, logout_button
from authcheck import require_auth

st.set_page_config(page_title="SecMate — Profile", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()

email = st.session_state.get("user_email", "adhithya@example.com")

st.markdown("### Profile")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Manage your SecMate identity, workspace role, and recent account activity.</div>",
    unsafe_allow_html=True,
)

left, right = st.columns([0.9, 1.3])

with left:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="width:62px; height:62px; border-radius:50%; background:linear-gradient(135deg,{COLORS['accent']},{COLORS['low']}); color:{COLORS['accent_text']}; display:flex; align-items:center; justify-content:center; font-size:22px; font-weight:800;">AD</div>
                <div>
                    <div style="font-size:20px; font-weight:700; color:{COLORS['text_primary']};">Adhithya</div>
                    <div style="font-size:13px; color:{COLORS['text_secondary']};">Security Analyst</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:12px; color:{COLORS['text_secondary']}; margin-top:4px;">{email}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
        st.button("Upload photo", use_container_width=True)

with right:
    with st.container(border=True):
        st.markdown('<div class="section-title">Profile Details</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Full name", value="Adhithya")
            st.text_input("Department", value="Security Engineering")
        with c2:
            st.text_input("Email", value=email)
            st.selectbox("Role", ["Security Analyst", "Admin", "Auditor", "Viewer"])

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)
    rows = [
        ("Signed in", "Today 21:42", "Browser session"),
        ("Viewed dashboard", "Today 21:43", "Staging environment"),
        ("Opened settings", "Today 21:44", "Workspace preferences"),
    ]
    for action, when, detail in rows:
        st.markdown(
            f"<div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid {COLORS['border']};'><span>{action}</span><span style='color:{COLORS['text_secondary']}; font-family:JetBrains Mono,monospace; font-size:12px;'>{when} - {detail}</span></div>",
            unsafe_allow_html=True,
        )

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
if st.button("Save Profile"):
    st.success("Profile saved. (Visual confirmation only.)")
