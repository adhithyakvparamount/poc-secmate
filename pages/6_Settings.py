"""
6_Settings.py — Account and workspace settings.

VISUAL MOCKUP NOTICE:
"Save Settings" only shows a confirmation message. Wire it to your
existing backend's configuration persistence (file, database, or
session store).
"""

import streamlit as st
from theme import apply_theme, sidebar_brand, COLORS, logout_button
from authcheck import require_auth

st.set_page_config(page_title="SecMate — Settings", layout="wide")
require_auth()
apply_theme()
sidebar_brand()
logout_button()

st.markdown("### Settings")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Manage your workspace appearance, account preferences, and assessment defaults.</div>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="section-title">Appearance</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Theme", ["SecMate Dark", "ChatGPT Dark", "Teal Cyber", "High Contrast"])
    with c2:
        st.selectbox("Dashboard density", ["Comfortable", "Compact", "Spacious"])
    with c3:
        st.selectbox("Accent color", ["Purple", "Blue", "Teal", "Green"])
    st.toggle("Use reduced motion", value=False)

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Profile Preferences</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Display name", value="Adhithya")
        st.text_input("Job title", value="Security Analyst")
    with c2:
        st.text_input("Work email", value=st.session_state.get("user_email", "adhithya@example.com"))
        st.selectbox("Timezone", ["Asia/Kolkata", "UTC", "America/New_York", "Europe/London"])

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Assessment Defaults</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Default endpoint", placeholder="https://api.example.com/v1/chat")
        st.selectbox("Default authentication method", ["None", "API Key", "Bearer Token", "OAuth2"])
    with c2:
        st.selectbox("Attacker model provider", ["Anthropic", "OpenAI", "Local / Custom"])
        st.slider("Default iterations per technique", 1, 50, 10)

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Notifications and Security</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.toggle("Email assessment summaries", value=True)
        st.toggle("Alert on critical findings", value=True)
        st.toggle("Weekly executive digest", value=False)
    with c2:
        st.toggle("Require SSO for workspace access", value=False)
        st.toggle("Session timeout warnings", value=True)
        st.selectbox("Audit log retention", ["30 days", "90 days", "180 days", "1 year"])

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
if st.button("Save Settings"):
    st.success("Settings saved. (Visual confirmation only — connect to backend to persist configuration.)")
