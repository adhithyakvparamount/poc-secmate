"""
3_VAPT_Findings.py — Rule-based VAPT evidence analysis findings.

VISUAL MOCKUP NOTICE:
Findings below are placeholder sample data. Replace get_findings()
with a read from your existing VAPT analysis module's output.
"""

import streamlit as st
from html import escape
from theme import apply_theme, sidebar_brand, COLORS, SEVERITY_ORDER, logout_button
from authcheck import require_auth

st.set_page_config(page_title="SecMate — VAPT Findings", layout="wide")
require_auth()
apply_theme()
sidebar_brand()
logout_button()

st.markdown("### VAPT Findings")
st.markdown(
    f"<div style='color:{COLORS['text_secondary']}; font-size:13.5px; margin-top:-8px; margin-bottom:20px;'>"
    "Rule-based evidence analysis results across all completed assessments.</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# MOCK DATA — replace with backend calls
# ---------------------------------------------------------------------------
def get_findings():
    history = st.session_state.get("assessment_history", [])
    real_findings = []
    for run in history:
        real_findings.extend(run.get("findings", []))
    if real_findings:
        return real_findings
    return [
        {"id": "VAPT-0142", "title": "System prompt fragment disclosed under injection", "severity": "critical",
         "category": "Prompt Injection", "target": "Support Bot v1.8", "status": "open",
         "rule": "RULE-SYS-DISCLOSE-01",
         "evidence": "Response contained a partial match (87% similarity) to the configured system prompt template.",
         "remediation": "Add explicit refusal instructions for meta-prompt requests and strip system prompt echoes at the output filter."},
        {"id": "VAPT-0139", "title": "Conversation history leaked across sessions", "severity": "high",
         "category": "Data Exfiltration", "target": "Support Bot v1.8", "status": "open",
         "rule": "RULE-CTX-BOUNDARY-04",
         "evidence": "Target paraphrased prior-session user content when asked to 'repeat the last conversation'.",
         "remediation": "Ensure session context is scoped per-conversation and not retrievable via natural-language requests."},
        {"id": "VAPT-0133", "title": "Rate limiting absent on repeated jailbreak attempts", "severity": "medium",
         "category": "Denial of Service", "target": "PolicyMate Agent v2.3", "status": "acknowledged",
         "rule": "RULE-RATE-LIMIT-02",
         "evidence": "50 consecutive adversarial prompts processed with no throttling or lockout.",
         "remediation": "Introduce exponential backoff after N flagged requests within a rolling window."},
        {"id": "VAPT-0128", "title": "Verbose error message reveals internal stack trace", "severity": "low",
         "category": "Information Disclosure", "target": "Internal Copilot", "status": "resolved",
         "rule": "RULE-ERR-VERBOSITY-01",
         "evidence": "Malformed input triggered a raw exception trace in the response body.",
         "remediation": "Return generic error messages to end users; log stack traces server-side only."},
    ]


findings = get_findings()
has_real_findings = bool(st.session_state.get("assessment_history"))
if has_real_findings:
    st.info("Showing findings generated from launched red-team assessments in this session.")

# --- Filters ---
f1, f2, f3 = st.columns([1, 1, 1])
with f1:
    sev_filter = st.multiselect("Severity", SEVERITY_ORDER, default=SEVERITY_ORDER)
with f2:
    status_filter = st.multiselect("Status", ["open", "acknowledged", "resolved"], default=["open", "acknowledged", "resolved"])
with f3:
    targets = sorted({f["target"] for f in findings})
    target_filter = st.multiselect("Target", targets, default=targets)

st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

visible = [f for f in findings if f["severity"] in sev_filter and f["status"] in status_filter and f["target"] in target_filter]
visible.sort(key=lambda f: SEVERITY_ORDER.index(f["severity"]))

sev_hex = {"critical": COLORS["critical"], "high": COLORS["high"], "medium": COLORS["medium"], "low": COLORS["low"], "info": COLORS["info"]}

if not visible:
    st.markdown(f"<div style='color:{COLORS['text_secondary']}; padding:20px 0;'>No findings match the selected filters.</div>", unsafe_allow_html=True)

for f in visible:
    with st.container():
        st.markdown(
            f"""
            <div class="finding-row" style="--sev-color:{sev_hex[f['severity']]};">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <span class="badge badge-{f['severity']}">{escape(str(f['severity']).upper())}</span>
                        <span class="finding-title" style="margin-left:8px;">{escape(str(f['title']))}</span>
                    </div>
                    <span style="font-family:'JetBrains Mono',monospace; font-size:11.5px; color:{COLORS['text_secondary']};">{escape(str(f['id']))}</span>
                </div>
                <div class="finding-meta">{escape(str(f['category']))} · {escape(str(f['target']))} · {escape(str(f['status']).title())} · Rule {escape(str(f['rule']))}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("View evidence & remediation"):
            st.markdown(f"**Evidence**  \n{f['evidence']}")
            st.markdown(f"**Suggested remediation**  \n{f['remediation']}")
