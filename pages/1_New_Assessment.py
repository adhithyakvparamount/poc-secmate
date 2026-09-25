"""
1_New_Assessment.py — Assessment configuration page.

The page launches the synchronous proof-of-concept assessment runner and
stores its configuration snapshot, exchanges, and findings in session state.
"""

import streamlit as st
from urllib.parse import urlparse
from theme import add_notification, apply_theme, sidebar_brand, get_active_colors, notification_center, status_pill, logout_button
from authcheck import require_auth
from assessment_runner import build_prompts, run_assessment
from workspace import option_label, t

st.set_page_config(page_title="SecMate — New Assessment", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(
    f"<div class='page-kicker'>AUTHORIZED SECURITY TESTING</div>"
    f"<div class='page-title'>{t('new_assessment')}</div>"
    f"<div class='page-subtitle'>{t('new_assessment_subtitle')} Configuration and evidence are retained with the run.</div>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-bottom:22px;">
        <div style="border:1px solid {COLORS['accent']}; background:{COLORS['accent']}14; border-radius:10px; padding:12px;"><span style="color:{COLORS['accent']}; font-family:JetBrains Mono,monospace; font-size:11px;">01</span><div style="font-weight:700; margin-top:5px;">Target</div></div>
        <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:10px; padding:12px;"><span style="color:{COLORS['text_secondary']}; font-family:JetBrains Mono,monospace; font-size:11px;">02</span><div style="font-weight:700; margin-top:5px;">Business context</div></div>
        <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:10px; padding:12px;"><span style="color:{COLORS['text_secondary']}; font-family:JetBrains Mono,monospace; font-size:11px;">03</span><div style="font-weight:700; margin-top:5px;">Coverage</div></div>
        <div style="border:1px solid {COLORS['border']}; background:{COLORS['surface']}; border-radius:10px; padding:12px;"><span style="color:{COLORS['text_secondary']}; font-family:JetBrains Mono,monospace; font-size:11px;">04</span><div style="font-weight:700; margin-top:5px;">Review & launch</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_form, col_preview = st.columns([1.4, 1])

with col_form:
    with st.container(border=True):
        st.markdown('<div class="section-title">Target Configuration</div>', unsafe_allow_html=True)
        target_name = st.text_input("Target name", placeholder="e.g. PolicyMate Agent v2.3")
        target_endpoint = st.text_input("Target endpoint / API URL", placeholder="https://api.example.com/v1/chat")
        auth_method = st.selectbox("Authentication", ["None", "API Key", "Bearer Token"])
        credential = ""
        if auth_method != "None":
            credential = st.text_input("Credential", type="password", placeholder="••••••••••••")
        st.caption("Credentials are used for this run only and are excluded from the saved configuration snapshot.")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Application Context</div>', unsafe_allow_html=True)
        owner = st.text_input("Owner / team", placeholder="e.g. AI Platform Security")
        c1, c2 = st.columns(2)
        with c1:
            criticality = st.selectbox("Business criticality", ["Tier 1 - Mission critical", "Tier 2 - Business critical", "Tier 3 - Internal productivity", "Tier 4 - Experimental"])
        with c2:
            assessment_template = st.selectbox("Assessment template", ["OWASP LLM baseline", "Prompt injection quick scan", "Data leakage review", "Custom coverage"])
        data_classes = st.multiselect("Data and capability profile", ["PII", "Payment data", "Health data", "Internal confidential", "Internet-facing", "Tool-enabled agent", "RAG / enterprise knowledge"], default=["Internal confidential"])

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="section-title">Test Suite Selection</div>', unsafe_allow_html=True)
        st.info("This build uses SecMate's deterministic adversarial prompt bank and rule-based response evaluator. Model-provider orchestration can be added without changing the run evidence format.")
        modules = ["Red Team - Adversarial Prompting", "Blue Team - Response Evaluation", "VAPT - Rule-Based Evidence Analysis"]
        iterations = st.slider("Iterations per technique", 1, 5, 2, help="Runs are capped at 5 probes per technique and 25 probes overall.")
        categories = st.multiselect(
            "Technique categories",
            ["Prompt Injection", "Jailbreak", "Data Exfiltration", "Role Confusion", "Policy Bypass", "Denial of Service"],
            default=["Prompt Injection", "Jailbreak", "Policy Bypass"],
        )
        authorized = st.checkbox("I confirm I am authorized to test this target endpoint.")

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)
    launch = st.button("Launch Authorized Assessment", use_container_width=True)
    if launch:
        parsed_endpoint = urlparse(target_endpoint)
        if not target_name or not target_endpoint:
            st.error("Target name and endpoint are required.")
        elif parsed_endpoint.scheme not in {"http", "https"} or not parsed_endpoint.netloc:
            st.error("Enter a valid HTTP or HTTPS target endpoint.")
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
                "owner": owner,
                "criticality": criticality,
                "assessment_template": assessment_template,
                "data_classes": data_classes,
                "modules": modules,
                "iterations": iterations,
                "categories": categories,
                "environment": st.session_state.get("workspace_environment", "Staging"),
            }
            with st.spinner("Running red-team assessment against target endpoint..."):
                result = run_assessment(config)
            st.session_state.latest_assessment = result
            st.session_state.assessment_history = [result] + st.session_state.get("assessment_history", [])
            critical_count = sum(finding.get("severity") == "critical" for finding in result["findings"])
            finding_count = len(result["findings"])
            if critical_count:
                notification_title = "Critical findings detected"
                notification_level = "critical"
            elif finding_count:
                notification_title = "Assessment findings ready"
                notification_level = "warning"
            else:
                notification_title = "Assessment completed"
                notification_level = "success"
            add_notification(
                notification_title,
                f"{target_name}: {len(result['exchanges'])} tests completed with {finding_count} findings.",
                level=notification_level,
                notification_id=f"assessment-{result['run_id']}",
            )
            st.toast(notification_title, icon=":material/notifications:")
            if result["status"] == "failed":
                st.error(f"Assessment could not reach **{target_name}**. Review the endpoint, authentication, and target logs before retrying.")
            elif result["status"] == "partial":
                st.warning(f"Assessment completed partially for **{target_name}** with {result['error_count']} request errors and {len(result['findings'])} findings.")
            else:
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
                <div><span style="color:{COLORS['text_secondary']};">{t('environment')}:</span>
                    <span style="font-family:'JetBrains Mono',monospace;">{option_label(st.session_state.get('workspace_environment', 'Staging'))}</span></div>
                <div><span style="color:{COLORS['text_secondary']};">Endpoint:</span>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:12px;">{target_endpoint or "—"}</span></div>
                 <div><span style="color:{COLORS['text_secondary']};">Owner:</span>
                     <span style="font-family:'JetBrains Mono',monospace;">{owner or "Unassigned"}</span></div>
                 <div><span style="color:{COLORS['text_secondary']};">Criticality:</span> {criticality}</div>
                 <div><span style="color:{COLORS['text_secondary']};">Template:</span> {assessment_template}</div>
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
        est_prompts = len(build_prompts(categories, iterations))
        st.markdown(
            f"<span style='font-family:JetBrains Mono,monospace; font-size:22px;'>{est_prompts}</span>"
            f"<span style='color:{COLORS['text_secondary']}; font-size:13px;'> adversarial probes</span>",
            unsafe_allow_html=True,
        )
        st.caption(f"Maximum estimated execution time: approximately {est_prompts * 20} seconds at the current 20-second request timeout.")

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="section-title">Safety Guardrails</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="font-size:12.8px; color:{COLORS['text_secondary']}; line-height:1.65;">
                • Only HTTP(S) endpoints are accepted.<br>
                • Runs are capped at 25 probes.<br>
                • Credentials are not stored in assessment history.<br>
                • Use a staging replica whenever production traffic or customer data may be affected.
            </div>
            """,
            unsafe_allow_html=True,
        )
