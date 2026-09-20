import streamlit as st

from backend_client import BackendUnavailable, backend_available, list_findings, list_targets
from data import FINDINGS, TARGETS
from ui import chips, configure_page


configure_page(
    "Portfolio posture",
    "Company projects under reusable red-team assurance. Use the sidebar pages for the full demo.",
)

try:
    if backend_available():
        TARGET_DATA = list_targets()
        FINDING_DATA = list_findings()
        st.success("Backend connected: FastAPI/Qwen path is available.")
    else:
        TARGET_DATA = TARGETS
        FINDING_DATA = FINDINGS
except (BackendUnavailable, Exception):
    TARGET_DATA = TARGETS
    FINDING_DATA = FINDINGS
    st.warning("Backend is not running. Showing local demo data.")

open_findings = [finding for finding in FINDING_DATA if finding["status"] != "Risk accepted"]
high_findings = [finding for finding in FINDING_DATA if finding["severity"] == "High"]
weighted_rate = round(sum(target["rate"] for target in TARGET_DATA) / len(TARGET_DATA)) if TARGET_DATA else 0

cols = st.columns(4)
with cols[0]:
    st.markdown(f'<div class="metric-card"><div class="value">{weighted_rate}%</div><div class="label">Weighted pass rate</div></div>', unsafe_allow_html=True)
with cols[1]:
    st.markdown(f'<div class="metric-card red"><div class="value">{len(open_findings)}</div><div class="label">Open findings · {len(high_findings)} high severity</div></div>', unsafe_allow_html=True)
with cols[2]:
    st.markdown('<div class="metric-card"><div class="value">3/5</div><div class="label">Targets ready for Tier 2</div></div>', unsafe_allow_html=True)
with cols[3]:
    st.markdown('<div class="metric-card"><div class="value">14</div><div class="label">Pinned regression cases</div></div>', unsafe_allow_html=True)

st.subheader("Projects")

for target in TARGET_DATA:
    last_assessed = target.get("last") or target.get("updated_at") or "Not assessed yet"
    next_assessment = target.get("next") or target.get("protected_window") or "On demand"
    left, right = st.columns([3, 2])
    with left:
        st.markdown(
            f"""
            <div class="target-card">
              <h3 style="margin:0">{target['name']}</h3>
              <p style="margin:.2rem 0;color:#5a6472">{target['surface']}</p>
              <div>{chips(target.get('guides', []))}</div>
              <p style="margin:.7rem 0 0;color:#5a6472">Last assessed: <b>{last_assessed}</b> · Next: <b>{next_assessment}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.progress(target["rate"] / 100, text=f"Pass rate: {target['rate']}%")
        st.caption(f"Open findings: {target.get('high', 0)} high, {target.get('medium', 0)} medium")
        with st.expander("View weakest classes"):
            for name, value in target.get("classes", {}).items():
                st.progress(value / 100, text=f"{name}: {value}%")

st.markdown(
    """
    <div class="callout">
      <b>Demo point:</b> Portfolio gives leadership one place to see which projects are safe, which ones have open findings, and which ones need deeper red-team runs.
    </div>
    """,
    unsafe_allow_html=True,
)
