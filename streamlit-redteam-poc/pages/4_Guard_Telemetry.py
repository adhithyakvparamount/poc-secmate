import pandas as pd
import streamlit as st

from data import GUARDS
from ui import configure_page


configure_page(
    "Guard telemetry",
    "Runtime guard verdicts, borderline classifications and control-layer limits.",
)

st.warning(
    "Borderline prompt-injection verdicts are up 3.1x on the SupportBot ingestion path. "
    "Treat uncertain verdicts as a detection signal, not only as a block/allow decision."
)

df = pd.DataFrame(GUARDS)
st.dataframe(
    df[["name", "side", "products", "checked", "breach"]],
    use_container_width=True,
    hide_index=True,
)

st.subheader("Breach rate")
chart = df.set_index("name")[["breach"]]
st.bar_chart(chart)

st.markdown(
    """
    <div class="callout red">
      <b>Important limitation:</b> gateway guards see prompts and completions. They do not reliably see the internal tool sequence. Action-layer findings still need tool policy, destination allowlists, parameter validation, and approval gates.
    </div>
    """,
    unsafe_allow_html=True,
)
