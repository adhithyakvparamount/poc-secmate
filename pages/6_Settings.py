"""Account and session-backed workspace settings."""

import streamlit as st
from theme import add_notification, apply_theme, sidebar_brand, get_active_colors, notification_center, THEME_PRESETS, logout_button
from authcheck import require_auth
from workspace import DENSITIES, ENVIRONMENTS, LANGUAGES, USER_TYPES, USE_CASES, option_label, persist_workspace_preferences, save_workspace_profile, t

st.set_page_config(page_title="SecMate — Settings", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(f"### {t('settings')}")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    f"{t('settings_subtitle')}</div>",
    unsafe_allow_html=True,
)

with st.form("workspace_preferences_form", border=True):
    st.markdown(f'<div class="section-title">{t("appearance")}</div>', unsafe_allow_html=True)
    theme_names = list(THEME_PRESETS.keys())
    c1, c2 = st.columns(2)
    with c1:
        selected_theme = st.selectbox(
            t("theme"),
            theme_names,
            index=theme_names.index(st.session_state.get("dashboard_theme", "SecMate Dark")),
        )
        selected_language = st.selectbox(
            t("language"),
            LANGUAGES,
            index=LANGUAGES.index(st.session_state.get("language_pref", "English")),
        )
    with c2:
        selected_environment = st.selectbox(
            t("environment"),
            ENVIRONMENTS,
            index=ENVIRONMENTS.index(st.session_state.get("workspace_environment", "Staging")),
            format_func=option_label,
        )
        selected_density = st.selectbox(
            t("dashboard_density"),
            DENSITIES,
            index=DENSITIES.index(st.session_state.get("dashboard_density", "Comfortable")),
            format_func=option_label,
        )
    selected_reduced_motion = st.toggle(t("reduced_motion"), value=st.session_state.get("reduced_motion", False))
    apply_preferences = st.form_submit_button(t("save_settings"))

if apply_preferences:
    st.session_state.dashboard_theme = selected_theme
    st.session_state.language_pref = selected_language
    st.session_state.workspace_environment = selected_environment
    st.session_state.dashboard_density = selected_density
    st.session_state.reduced_motion = selected_reduced_motion
    st.session_state.sync_sidebar_preferences = True
    persist_workspace_preferences()
    add_notification(t("settings_saved"), f"{option_label(selected_environment)} · {option_label(selected_density)}", level="success")
    st.rerun()

st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

with st.form("onboarding_profile_form", border=True):
    st.markdown(f'<div class="section-title">{t("about_use_case")}</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.selectbox(t("user_type_question"), USER_TYPES, key="onboarding_user_type", format_func=option_label)
    with p2:
        st.selectbox(t("use_case_question"), USE_CASES, key="onboarding_use_case", format_func=option_label)
    st.text_area(t("goal_question"), key="onboarding_goal", placeholder=t("goal_placeholder"))
    save_onboarding = st.form_submit_button(t("save_settings"))

if save_onboarding:
    save_workspace_profile()
    add_notification(t("settings_saved"), option_label(st.session_state.onboarding_use_case), level="success")
    st.rerun()

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
if st.button("Save profile and assessment defaults"):
    st.success("Profile and assessment defaults are retained for this session.")
