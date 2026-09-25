"""
2_Red_Blue_Team.py — Red Team (adversarial prompts) and Blue Team
(target response evaluation) results page.

The page reads evidence from assessment runs stored in Streamlit session
state. Blue-team scoring remains deterministic and rule-based.
"""

import streamlit as st
from html import escape
from theme import apply_theme, sidebar_brand, get_active_colors, notification_center, severity_badge, logout_button
from authcheck import require_auth
from workspace import t

st.set_page_config(page_title="SecMate — Red / Blue Team", layout="wide")
require_auth()
COLORS = get_active_colors()
apply_theme()
sidebar_brand()
logout_button()
notification_center()

st.markdown(
    f"<div class='page-kicker'>ASSESSMENT EVIDENCE</div>"
    f"<div class='page-title'>{t('results_title')}</div>"
    f"<div class='page-subtitle'>{t('results_subtitle')}</div>",
    unsafe_allow_html=True,
)

history = st.session_state.get("assessment_history", [])
if history:
    run_options = [f"{run['target']} — {run['completed_at']}" for run in history]
    run_select = st.selectbox("Run", run_options)
    selected_run = history[run_options.index(run_select)]
else:
    run_select = None
    selected_run = None

if not selected_run:
    st.markdown(
        f"""
        <div style="border:1px dashed {COLORS['border']}; border-radius:14px; padding:38px; text-align:center; background:{COLORS['surface']};">
            <div style="font-size:18px; font-weight:700; color:{COLORS['text_primary']};">No assessment evidence yet</div>
            <div style="font-size:13px; color:{COLORS['text_secondary']}; margin:8px auto 18px; max-width:520px;">Launch an authorized assessment to inspect prompts, target responses, verdicts, latency, and analyst-ready evidence.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Assessment"):
        st.switch_page("pages/1_New_Assessment.py")
    st.stop()

exchanges = selected_run.get("exchanges", [])
summary = {
    "tests": len(exchanges),
    "resisted": sum(ex.get("verdict") == "resisted" for ex in exchanges),
    "flagged": sum(ex.get("verdict") in {"flagged", "failed"} for ex in exchanges),
    "errors": sum(ex.get("verdict") == "error" for ex in exchanges),
}
c1, c2, c3, c4 = st.columns(4)
for col, label, value in zip([c1, c2, c3, c4], ["Tests executed", "Safely resisted", "Flagged for review", "Request errors"], summary.values()):
    with col:
        st.markdown(f'<div class="metric-card"><div class="label">{label}</div><div class="value">{value}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
filter_a, filter_b, filter_c = st.columns([1.2, 1, 1])
with filter_a:
    search = st.text_input("Search evidence", placeholder="Prompt, response, or technique")
with filter_b:
    technique_filter = st.multiselect("Technique", sorted({ex.get("technique", "Unknown") for ex in exchanges}), default=sorted({ex.get("technique", "Unknown") for ex in exchanges}))
with filter_c:
    verdict_filter = st.multiselect("Verdict", ["resisted", "flagged", "failed", "error"], default=["resisted", "flagged", "failed", "error"])

visible_exchanges = [
    ex for ex in exchanges
    if ex.get("technique") in technique_filter
    and ex.get("verdict") in verdict_filter
    and search.lower() in f"{ex.get('technique', '')} {ex.get('prompt', '')} {ex.get('response', '')}".lower()
]

tab_red, tab_blue = st.tabs(["Red Team Evidence", "Blue Team Evaluation"])


def get_red_team_exchanges():
    return visible_exchanges


def get_blue_team_evaluations():
    return [
            {
                "category": ex["technique"],
                "score": ex["score"],
                "note": ex["note"],
                "severity": ex["severity"],
                "latency_ms": ex.get("latency_ms", 0),
                "http_status": ex.get("http_status"),
            }
            for ex in visible_exchanges
        ]


with tab_red:
    st.caption(f"Showing {len(visible_exchanges)} of {len(exchanges)} evidence records from {selected_run['run_id']}.")
    for ex in get_red_team_exchanges():
        with st.container(border=True):
            st.markdown(
                f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div><span style="font-size:13px; color:{COLORS['text_secondary']};">{escape(str(ex['technique']))}</span><span style="margin-left:10px; font-family:JetBrains Mono,monospace; font-size:11px; color:{COLORS['accent']};">{escape(str(ex.get('verdict', '')).upper())}</span></div>
                    <div>{severity_badge(ex['severity'])}</div>
                </div>
                <div class="transcript-card transcript-prompt">
                    <div class="transcript-label">Adversarial Prompt</div>
                    <div class="transcript-body">{escape(str(ex['prompt']))}</div>
                </div>
                <div class="transcript-card transcript-response">
                    <div class="transcript-label">Target Response</div>
                    <div class="transcript-body">{escape(str(ex['response'] or '[empty response]'))}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_blue:
    st.info("Blue-team scoring is deterministic and rule-based in this implementation. Treat flagged results as analyst-review candidates, not final vulnerability confirmation.")
    for ev in get_blue_team_evaluations():
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 0.8, 1, 2])
            c1.markdown(f"<span style='font-weight:600; font-size:14px;'>{escape(str(ev['category']))}</span>", unsafe_allow_html=True)
            c2.markdown(f"<span style='font-family:JetBrains Mono,monospace; font-size:14px;'>{escape(str(ev['score']))}</span>", unsafe_allow_html=True)
            c3.markdown(severity_badge(ev["severity"]), unsafe_allow_html=True)
            if "latency_ms" in ev:
                c4.markdown(
                    f"<span style='font-family:JetBrains Mono,monospace; font-size:12px; color:{COLORS['text_secondary']};'>HTTP {ev.get('http_status') or 'n/a'} · {ev['latency_ms']}ms</span>",
                    unsafe_allow_html=True,
                )
            st.markdown(f"<div style='color:{COLORS['text_secondary']}; font-size:13px; margin-top:6px;'>{escape(str(ev['note']))}</div>", unsafe_allow_html=True)
