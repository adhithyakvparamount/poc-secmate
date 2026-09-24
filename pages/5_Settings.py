"""
5_Settings.py — Target, model, and environment configuration defaults.

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
    "Default configuration used when creating a new assessment.</div>",
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown('<div class="section-title">Default Target Configuration</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Default endpoint", placeholder="https://api.example.com/v1/chat")
    with c2:
        st.selectbox("Default authentication method", ["None", "API Key", "Bearer Token", "OAuth2"])

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Model Configuration</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox("Attacker model provider", ["Anthropic", "OpenAI", "Local / Custom"])
    with c2:
        st.text_input("Attacker model identifier", placeholder="claude-sonnet-4-6")
    with c3:
        st.slider("Default temperature", 0.0, 1.0, 0.7, 0.05)

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Test Suite Defaults</div>', unsafe_allow_html=True)
    st.multiselect(
        "Default technique categories",
        ["Prompt Injection", "Jailbreak", "Data Exfiltration", "Role Confusion", "Policy Bypass", "Denial of Service"],
        default=["Prompt Injection", "Jailbreak"],
    )
    st.slider("Default iterations per technique", 1, 50, 10)

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown('<div class="section-title">Environment</div>', unsafe_allow_html=True)
    st.radio("Active environment", ["Staging", "Production", "Local"], horizontal=True)
    st.toggle("Enable verbose logging", value=False)

st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
if st.button("Save Settings"):
    st.success("Settings saved. (Visual confirmation only — connect to backend to persist configuration.)")
