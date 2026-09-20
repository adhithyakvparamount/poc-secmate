import html
from typing import Iterable

import streamlit as st


def configure_page(title: str, subtitle: str) -> None:
    st.set_page_config(page_title=title, page_icon="🛡️", layout="wide")
    apply_css()
    st.markdown(f"""
    <div class="page-heading">
      <div class="eyebrow">Red Team Assurance POC</div>
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(subtitle)}</p>
    </div>
    """, unsafe_allow_html=True)


def apply_css() -> None:
    st.markdown(
        """
        <style>
        :root { --ink:#14181f; --slate:#5a6472; --rule:#dfe2e7; --panel:#f4f5f7; --red:#8c2f39; --redwash:#f8eced; --blue:#23527c; --bluewash:#eaf0f6; --amber:#8a6100; --amberwash:#fbf2dd; --green:#2f6b4f; }
        .block-container { padding-top: 2rem; }
        .page-heading { border-bottom: 2px solid var(--ink); padding-bottom: 1rem; margin-bottom: 1.4rem; }
        .page-heading h1 { margin: 0; font-size: 2.2rem; letter-spacing: -0.03em; }
        .page-heading p { margin: .35rem 0 0; color: var(--slate); max-width: 78ch; }
        .eyebrow { color: var(--red); font: 700 .72rem monospace; letter-spacing: .08em; text-transform: uppercase; margin-bottom: .35rem; }
        .metric-card { background: white; border: 1px solid var(--rule); border-top: 3px solid var(--blue); padding: 1rem; min-height: 105px; }
        .metric-card.red { border-top-color: var(--red); }
        .metric-card .value { font-size: 1.8rem; font-weight: 700; color: var(--ink); }
        .metric-card .label { color: var(--slate); font-size: .84rem; }
        .target-card, .finding-card, .evidence-card { background: white; border: 1px solid var(--rule); padding: 1rem; margin-bottom: .8rem; }
        .target-card { border-left: 4px solid var(--blue); }
        .finding-card.high { border-left: 4px solid var(--red); }
        .finding-card.medium { border-left: 4px solid var(--amber); }
        .chip { display:inline-block; background:var(--panel); color:var(--slate); border-radius:2px; padding:2px 7px; font-size:.72rem; margin-right:4px; }
        .chip.blue { background:var(--bluewash); color:var(--blue); }
        .chip.red { background:var(--redwash); color:var(--red); }
        .tool { font-family: monospace; display:inline-block; border:1px solid var(--rule); border-radius:2px; padding:3px 8px; margin:2px; background:white; }
        .tool.hot { border-color:var(--red); background:var(--redwash); color:var(--red); font-weight:700; }
        .gate { border:1px solid var(--rule); padding:.85rem; margin-bottom:.65rem; background:white; }
        .gate.pass { border-left:4px solid var(--green); }
        .gate.warn { border-left:4px solid var(--amber); }
        .gate.fail { border-left:4px solid var(--red); }
        .callout { border-left:4px solid var(--blue); background:var(--bluewash); padding: .9rem 1rem; margin: 1rem 0; }
        .callout.red { border-left-color:var(--red); background:var(--redwash); }
        code { background: var(--panel); padding: 1px 5px; border-radius: 2px; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def chips(values: Iterable[str], kind: str = "") -> str:
    cls = f"chip {kind}".strip()
    return " ".join(f'<span class="{cls}">{html.escape(v)}</span>' for v in values)


def tool_chain(chain: list[str], hot: list[str] | None = None) -> str:
    hot = hot or []
    if not chain:
        return '<span style="color:#8b93a0;font-style:italic">No tool calls - reasoning-layer finding</span>'
    parts = []
    for tool in chain:
        cls = "tool hot" if tool in hot else "tool"
        parts.append(f'<span class="{cls}">{html.escape(tool)}</span>')
    return " → ".join(parts)


def target_by_name(targets: list[dict], name: str) -> dict:
    return next(target for target in targets if target["name"] == name)
