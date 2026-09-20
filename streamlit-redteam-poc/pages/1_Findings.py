import streamlit as st

from backend_client import BackendUnavailable, backend_available, list_findings
from data import FINDINGS
from ui import configure_page, tool_chain


configure_page(
    "Findings triage",
    "Evidence-backed findings sorted by exploited blast radius, not only by score.",
)

try:
    if backend_available():
        FINDING_DATA = list_findings()
        st.success("Backend connected: findings loaded from FastAPI.")
    else:
        FINDING_DATA = FINDINGS
except (BackendUnavailable, Exception):
    FINDING_DATA = FINDINGS
    st.warning("Backend is not running. Showing local demo findings.")

severity_filter = st.radio("Filter", ["All", "Open", "High", "Action layer"], horizontal=True)

findings = FINDING_DATA
if severity_filter == "Open":
    findings = [finding for finding in FINDING_DATA if finding["status"] == "Open"]
elif severity_filter == "High":
    findings = [finding for finding in FINDING_DATA if finding["severity"] == "High"]
elif severity_filter == "Action layer":
    findings = [finding for finding in FINDING_DATA if "Action" in finding["layer"]]

selected_id = st.selectbox("Open evidence for finding", [finding["id"] for finding in findings])
selected = next(finding for finding in findings if finding["id"] == selected_id)

for finding in findings:
    severity_class = finding["severity"].lower()
    st.markdown(
        f"""
        <div class="finding-card {severity_class}">
          <b>{finding['id']} · {finding['vulnerability']}</b>
          <p style="margin:.25rem 0;color:#5a6472">{finding['target']} · {finding['layer']} layer · {finding['status']} · failed {finding['runs']}x</p>
        <div>{tool_chain(finding.get('chain', []), finding.get('hot', []))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()
st.subheader(f"Evidence drawer: {selected['id']}")
cols = st.columns(4)
cols[0].metric("Severity", selected["severity"])
cols[1].metric("Status", selected["status"])
cols[2].metric("Layer", selected["layer"])
cols[3].metric("Runs failed", selected["runs"])

st.markdown("**Exploited chain**", help="The exact tool sequence the red-team case exploited.")
st.markdown(tool_chain(selected.get("chain", []), selected.get("hot", [])), unsafe_allow_html=True)

st.markdown("### Transcript")
with st.container(border=True):
    st.markdown("**Attacker input**")
    st.write(selected["attack"])
    st.markdown("**Agent response**")
    st.write(selected["agent"])

st.markdown("### Evaluator verdict")
st.error(selected["verdict"])

st.markdown("### Remediation")
st.info(selected["fix"])

col1, col2, col3 = st.columns(3)
col1.button("Assign owner", use_container_width=True)
col2.button("Pin regression", use_container_width=True)
col3.button("Open Jira ticket", use_container_width=True)
