"""
1_New_Assessment.py — Assessment configuration page.

VISUAL MOCKUP NOTICE:
The "Launch Assessment" button below only shows a confirmation message.
Wire it to your existing backend's assessment-run entry point (the
function that currently kicks off Red Team / Blue Team / VAPT logic).
"""

import streamlit as st
from theme import apply_theme, sidebar_brand, get_active_colors, status_pill, logout_button
from authcheck import require_auth
from assessment_runner import run_assessment

st.set_page_config(page_title="SecMate — New Assessment", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()

st.markdown("### New Assessment")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Configure a target and launch a Red Team, Blue Team, or full VAPT run.</div>",
    unsafe_allow_html=True,
)

col_form, col_preview = st.columns([1.4, 1])

with col_form:
    with st.container(border=True):
        st.markdown('<div class="section-title">Target Configuration</div>', unsafe_allow_html=True)
        target_name = st.text_input("Target name", placeholder="e.g. PolicyMate Agent v2.3")
        target_endpoint = st.text_input("Target endpoint / API URL", placeholder="https://api.example.com/v1/chat")
        auth_method = st.selectbox("Authentication", ["None", "API Key", "Bearer Token", "OAuth2"])
        credential = ""
        if auth_method != "None":
            credential = st.text_input("Credential", type="password", placeholder="••••••••••••")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Model Configuration</div>', unsafe_allow_html=True)
        model_provider = st.selectbox("Attacker model provider", ["Anthropic", "OpenAI", "Local / Custom"])
        model_name = st.text_input("Model identifier", placeholder="e.g. claude-sonnet-4-6")
        temperature = st.slider("Sampling temperature", 0.0, 1.0, 0.7, 0.05)

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Test Suite Selection</div>', unsafe_allow_html=True)
        modules = st.multiselect(
            "Assessment modules",
            ["Red Team — Adversarial Prompting", "Blue Team — Response Evaluation", "VAPT — Rule-Based Evidence Analysis"],
            default=["Red Team — Adversarial Prompting", "Blue Team — Response Evaluation", "VAPT — Rule-Based Evidence Analysis"],
        )
        iterations = st.slider("Iterations per technique", 1, 50, 10)
        categories = st.multiselect(
            "Technique categories",
            ["Prompt Injection", "Jailbreak", "Data Exfiltration", "Role Confusion", "Policy Bypass", "Denial of Service"],
            default=["Prompt Injection", "Jailbreak", "Policy Bypass"],
        )
        authorized = st.checkbox("I confirm I am authorized to test this target endpoint.")

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    launch = st.button("Launch Assessment", use_container_width=False)
    if launch:
        if not target_name or not target_endpoint:
            st.error("Target name and endpoint are required.")
        elif not authorized:
            st.error("Confirm that you are authorized to test this target before launching.")
        elif not categories:
            st.error("Select at least one technique category.")
        else:
            config = {
                "target_name": target_name,
                "target_endpoint": target_endpoint,
                "auth_method": auth_method,
                "credential": credential,
                "model_provider": model_provider,
                "model_name": model_name,
                "temperature": temperature,
                "modules": modules,
                "iterations": iterations,
                "categories": categories,
            }
            with st.spinner("Running red-team assessment against target endpoint..."):
                result = run_assessment(config)
            st.session_state.latest_assessment = result
            st.session_state.assessment_history = [result] + st.session_state.get("assessment_history", [])
            st.success(f"Assessment completed for **{target_name}** with {len(result['exchanges'])} tests and {len(result['findings'])} findings.")
            c_results, c_findings = st.columns(2)
            with c_results:
                if st.button("View Red / Blue Results", use_container_width=True):
                    st.switch_page("pages/2_Red_Blue_Team.py")
            with c_findings:
                if st.button("View Findings", use_container_width=True):
                    st.switch_page("pages/3_VAPT_Findings.py")

with col_preview:
    st.markdown('<div class="section-title">Run Summary</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="font-size:13px; line-height:2;">
                <div><span style="color:{COLORS['text_secondary']};">Target:</span>
                    <span style="font-family:'JetBrains Mono',monospace;">{target_name or "—"}</span></div>
                <div><span style="color:{COLORS['text_secondary']};">Endpoint:</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:12px;">{target_endpoint or "—"}</span></div>
                <div><span style="color:{COLORS['text_secondary']};">Model:</span>
                    <span style="font-family:'JetBrains Mono',monospace;">{model_name or "—"} ({model_provider})</span></div>
                <div><span style="color:{COLORS['text_secondary']};">Iterations:</span> {iterations} per technique</div>
                <div><span style="color:{COLORS['text_secondary']};">Modules:</span> {len(modules)} selected</div>
                <div><span style="color:{COLORS['text_secondary']};">Categories:</span> {len(categories)} selected</div>
                <div style="margin-top:8px;">Status: {status_pill("pending")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Estimated Scope</div>', unsafe_allow_html=True)
        est_prompts = iterations * max(len(categories), 1)
        st.markdown(
            f"<span style='font-family:JetBrains Mono,monospace; font-size:22px;'>{est_prompts}</span>"
            f"<span style='color:{COLORS['text_secondary']}; font-size:13px;'> adversarial prompts to generate</span>",
            unsafe_allow_html=True,
        )
