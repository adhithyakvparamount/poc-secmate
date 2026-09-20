import streamlit as st

from data import DEFAULT_INTAKE, DEMO_STEPS
from ui import configure_page


configure_page(
    "Code + demo notes",
    "Use this page during presentation to explain how the POC works and what each project implements.",
)

left, right = st.columns(2)

with left:
    st.subheader("Demo session script")
    for index, step in enumerate(DEMO_STEPS, start=1):
        st.write(f"{index}. {step}")

    st.subheader("Files in this Streamlit version")
    st.code(
        """streamlit-redteam-poc/
  app.py
  data.py
  ui.py
  pages/
    1_Findings.py
    2_New_Assessment.py
    3_Onboarding.py
    4_Guard_Telemetry.py
    5_Code_And_Demo.py
  requirements.txt
  README.md""",
        language="text",
    )

with right:
    st.subheader("Target protocol")
    st.code(
        """POST /_redteam/turn
  { run_id, case_id, session_id?, input, turns }
-> { content, session_id, tools_called: [{ name, input_parameters, output }] }

GET /_redteam/manifest
-> { agent_version, manifest_hash, tools, max_concurrency }

GET /_redteam/health
-> { ok, accepts_turn_history, mean_latency_ms }""",
        language="http",
    )

    st.subheader("Reusable intake YAML")
    st.code(DEFAULT_INTAKE, language="yaml")

st.info(
    "Main message: any project can be onboarded through the same intake, tested through the same preflight-controlled red-team flow, and triaged through the same evidence model."
)
