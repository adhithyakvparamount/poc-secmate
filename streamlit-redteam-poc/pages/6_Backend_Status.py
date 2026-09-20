import streamlit as st

from backend_client import BACKEND_URL, BackendUnavailable, generate_attacks, health, list_targets
from ui import configure_page


configure_page(
    "Backend status",
    "Check FastAPI backend connectivity and Qwen/Ollama attack generation from the UI.",
)

st.write(f"Backend URL: `{BACKEND_URL}`")

try:
    status = health()
    st.success("Backend is reachable.")
    st.json(status)
    targets = list_targets()
    st.write(f"Targets available from backend: **{len(targets)}**")
    st.dataframe(targets, use_container_width=True)
except BackendUnavailable as exc:
    st.error("Backend is not reachable.")
    st.code(str(exc))
    st.stop()

st.divider()
st.subheader("Qwen/Ollama test")
target_purpose = st.text_area("Target purpose", "Read-only security database assistant for schema discovery and safe SQL reporting.")
vulnerability = st.text_input("Vulnerability", "SQLMutationBypass")
count = st.slider("Prompt count", 1, 5, 3)
use_model = st.checkbox("Use Qwen/Ollama model", value=True)

if st.button("Generate attacks through backend", type="primary"):
    with st.spinner("Calling backend /attacks/generate. If Ollama/Qwen is unavailable, backend falls back to demo prompts."):
        attacks = generate_attacks(target_purpose, vulnerability, count, use_model=use_model)
    for idx, attack in enumerate(attacks, start=1):
        st.markdown(f"**Attack {idx}**")
        st.write(attack)
