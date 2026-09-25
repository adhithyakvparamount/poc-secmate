"""Executive and technical report preview for session assessment data."""

from html import escape

import streamlit as st

from authcheck import require_auth
from theme import apply_theme, get_active_colors, logout_button, notification_center, sidebar_brand
from workspace import t

st.set_page_config(page_title="SecMate - Reports", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(
    f"<div class='page-kicker'>STAKEHOLDER COMMUNICATION</div>"
    f"<div class='page-title'>{t('reports')}</div>"
    f"<div class='page-subtitle'>{t('reports_subtitle')} Preview scope and evidence before exporting.</div>",
    unsafe_allow_html=True,
)

history = st.session_state.get("assessment_history", [])
if not history:
    st.markdown(
        f"""
        <div style="border:1px dashed {COLORS['border']}; border-radius:14px; padding:38px; text-align:center; background:{COLORS['surface']};">
            <div style="font-size:18px; font-weight:700;">No reportable assessment data</div>
            <div style="color:{COLORS['text_secondary']}; font-size:13px; margin:8px auto 18px; max-width:560px;">Complete an assessment first. SecMate will build executive and technical views from its evidence, findings, and configuration snapshot.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Assessment"):
        st.switch_page("pages/1_New_Assessment.py")
    st.stop()

run_options = [f"{run['target']} - {run['completed_at']}" for run in history]
control_a, control_b, control_c = st.columns([1.8, 1.2, 1])
with control_a:
    selected_label = st.selectbox("Assessment run", run_options)
with control_b:
    template = st.selectbox("Report template", ["Executive summary", "Technical detail", "Evidence appendix"])
with control_c:
    classification = st.selectbox("Classification", ["Confidential", "Internal", "Public"])

run = history[run_options.index(selected_label)]
findings = run.get("findings", [])
exchanges = run.get("exchanges", [])
critical = sum(f.get("severity") == "critical" for f in findings)
high = sum(f.get("severity") == "high" for f in findings)
resisted = sum(ex.get("verdict") == "resisted" for ex in exchanges)
pass_rate = round(resisted / len(exchanges) * 100) if exchanges else 0
config = run.get("config", {})

top_finding = findings[0] if findings else None
risk_statement = (
    f"The assessment identified {len(findings)} evidence-backed findings, including {critical} critical and {high} high severity items. "
    "Immediate remediation ownership and targeted retesting are recommended before the next production release."
    if findings
    else "The assessment produced no rule-based findings. Continue regression testing and analyst review before treating the target as fully validated."
)

left, preview = st.columns([0.34, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown('<div class="section-title">Report Scope</div>', unsafe_allow_html=True)
        st.markdown(f"**Target**  \n{run['target']}")
        st.markdown(f"**Environment**  \n{run.get('environment', 'Unknown')}")
        st.markdown(f"**Owner**  \n{config.get('owner') or 'Unassigned'}")
        st.markdown(f"**Criticality**  \n{config.get('criticality', 'Not classified')}")
        st.markdown(f"**Run ID**  \n`{run['run_id']}`")
        st.markdown(f"**Classification**  \n{classification}")

    report_html = f"""<!doctype html><html><head><meta charset='utf-8'><title>SecMate report</title>
    <style>body{{font-family:Arial,sans-serif;max-width:960px;margin:48px auto;color:#172033;line-height:1.55}}h1{{color:#0b62c4}}.metric{{display:inline-block;border:1px solid #ccd6e3;padding:14px 20px;margin:8px}}code{{background:#eef3f8;padding:2px 5px}}</style></head><body>
    <p>SECMATE SECURITY ASSESSMENT · {escape(classification.upper())}</p><h1>{escape(run['target'])} - {escape(template.title())}</h1>
    <p>Run <code>{escape(run['run_id'])}</code> completed {escape(run['completed_at'])}</p>
    <div class='metric'>Critical: {critical}</div><div class='metric'>High: {high}</div><div class='metric'>Findings: {len(findings)}</div><div class='metric'>Resistance rate: {pass_rate}%</div>
    <h2>Executive risk statement</h2><p>{escape(risk_statement)}</p>
    <h2>Assessment scope</h2><p>Environment: {escape(str(run.get('environment', 'Unknown')))}<br>Owner: {escape(str(config.get('owner') or 'Unassigned'))}<br>Criticality: {escape(str(config.get('criticality', 'Not classified')))}</p>
    <h2>Priority recommendation</h2><p>{escape(top_finding.get('remediation', 'Maintain regression testing and manual evidence review.') if top_finding else 'Maintain regression testing and manual evidence review.')}</p>
    </body></html>"""
    st.download_button("Export HTML Report", report_html, file_name=f"{run['run_id']}-secmate-report.html", mime="text/html", use_container_width=True)
    st.caption("HTML export is available now. PDF rendering can use the same report data contract when a document service is connected.")

with preview:
    with st.container(border=True):
        st.markdown(
            f"""
            <div class="page-kicker">{escape(template.upper())}</div>
            <div style="font-size:28px; font-weight:750; letter-spacing:-.03em; color:{COLORS['text_primary']};">{escape(run['target'])} - Security Test Report</div>
            <div style="font-family:JetBrains Mono,monospace; color:{COLORS['text_secondary']}; font-size:12px; margin:9px 0 22px;">SECMATE · {escape(run['completed_at'])} · {escape(classification.upper())} · {escape(run['run_id'])}</div>
            <div style="height:2px; background:linear-gradient(90deg,{COLORS['accent']},transparent); margin-bottom:24px;"></div>
            <p style="color:{COLORS['text_secondary']}; line-height:1.7;">SecMate executed {len(exchanges)} authorized adversarial probes against <strong style="color:{COLORS['text_primary']};">{escape(run['target'])}</strong> in the {escape(run.get('environment', 'Unknown'))} environment. This report summarizes observed guardrail behavior and evidence requiring analyst review.</p>
            """,
            unsafe_allow_html=True,
        )
        metrics = st.columns(4)
        for col, label, value, color in zip(metrics, ["Critical", "High", "Total findings", "Resistance rate"], [critical, high, len(findings), f"{pass_rate}%"], [COLORS['critical'], COLORS['high'], COLORS['text_primary'], COLORS['accent']]):
            col.markdown(f'<div class="metric-card"><div class="label">{label}</div><div class="value" style="color:{color};">{value}</div></div>', unsafe_allow_html=True)
        st.markdown("### Executive Risk Statement")
        st.write(risk_statement)
        st.markdown("### Priority Recommendation")
        st.write(top_finding.get("remediation") if top_finding else "Maintain regression testing, manual evidence review, and release-gate validation.")
        if top_finding:
            st.markdown("### Highest Priority Finding")
            st.markdown(f"**{top_finding['title']}**  \n{top_finding['category']} · {top_finding['severity'].title()} · {top_finding['id']}")
