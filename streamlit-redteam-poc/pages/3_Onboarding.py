import yaml
import streamlit as st

from data import DEFAULT_INTAKE
from ui import configure_page


configure_page(
    "Project onboarding",
    "Add a new company project using architecture facts, endpoints, owners and custom risks.",
)

left, right = st.columns([3, 2])

with left:
    st.subheader("Intake form")
    name = st.text_input("Project name", "ClaimsPilot")
    team = st.text_input("Owning team", "Claims Platform")
    window = st.text_input("Protected testing window", "Thu 22:00-04:00 IST")
    purpose = st.text_area(
        "Project purpose",
        "Claims servicing agent: reads claim records, drafts responses, recommends settlements, and raises approvals",
    )

    st.markdown("### Architecture facts")
    calls_tools = st.checkbox("Calls tools", True)
    stateful = st.checkbox("Stateful sessions", False)
    rag = st.checkbox("Retrieval-backed", True)
    delegates = st.checkbox("Delegates to sub-agents", False)
    untrusted = st.checkbox("Ingests untrusted data", True)

    st.markdown("### Endpoint summary")
    st.text_input("Front door", "https://claimspilot.internal/agent")
    st.text_input("Staging", "https://claimspilot.staging.internal/agent")
    st.text_input("Trace endpoint", "https://otel.internal/v1/traces")

with right:
    st.subheader("Definition of done")
    dod = [
        ("Intake YAML parsed", True),
        ("Front door and staging endpoint present", True),
        ("Evidence endpoint present", True),
        ("Capability map recorded", True),
        ("Tool calls include parameters and outputs", True),
        ("Custom vulnerabilities declared", False),
        ("Rules of engagement and SOC owner named", False),
        ("Calibration run passed with canaries", False),
    ]
    for item, done in dod:
        (st.success if done else st.warning)(item)
    st.button("Schedule assessment", disabled=True, use_container_width=True)
    st.caption("Scheduling is blocked until all definition-of-done items pass.")

st.divider()
st.subheader("YAML intake preview")
st.info("You can upload either the generic dynamic target config or a SecMate-style persona YAML with name, description, system_prompt, guardrails and tools.")
uploaded = st.file_uploader("Upload intake YAML", type=["yaml", "yml"])
source = uploaded.getvalue().decode("utf-8") if uploaded else DEFAULT_INTAKE
st.code(source, language="yaml")

try:
    parsed = yaml.safe_load(source)
    st.success("YAML parsed successfully")
    st.json(parsed)
except yaml.YAMLError as exc:
    st.error(f"Could not parse YAML: {exc}")

facts = [calls_tools, stateful, rag, delegates, untrusted]
families = []
if calls_tools or delegates:
    families.append("AI agents")
if stateful:
    families.append("Conversational agents")
if rag:
    families.append("Agentic RAG")
if untrusted:
    families.append("Indirect-instruction coverage")

st.info(f"Derived scope for {name} owned by {team}: {', '.join(families)}. Protected window: {window}.")
st.caption(f"Purpose: {purpose}")
