from __future__ import annotations

import uuid

from .database import connect, dumps, row_to_dict
from .model_client import generate_attacks
from .preflight import evaluate_preflight


def create_and_run(target_id: str, tier: str, use_model: bool = False) -> dict:
    with connect() as conn:
        target_row = conn.execute("SELECT * FROM targets WHERE id = ?", (target_id,)).fetchone()
        target = row_to_dict(target_row)
        if not target:
            raise ValueError("target not found")

        gates = evaluate_preflight(target)
        blocking = [gate for gate in gates if gate["state"] == "fail"]
        run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"

        if blocking:
            events = ["Run requested", f"Blocked by {blocking[0]['title']}"]
            conn.execute(
                "INSERT INTO runs (id, target_id, tier, state, pass_rate, summary, events) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, target_id, tier, "blocked", 0, f"Blocked by {blocking[0]['title']}", dumps(events)),
            )
            return row_to_dict(conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone())

        vulnerability = next(iter(target.get("classes") or {"ExcessiveAgency": 70}))
        attacks = generate_attacks(target["purpose"], vulnerability, count=3, use_model=use_model)
        events = [
            "Admission token accepted",
            "Corpus version locked",
            f"Generated {len(attacks)} adversarial attacks for {vulnerability}",
            "Target returned tool calls with parameters and outputs",
            "Evaluator scoring complete",
            "Demo finding created for review",
        ]

        conn.execute(
            "INSERT INTO runs (id, target_id, tier, state, pass_rate, summary, events, completed_at) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (run_id, target_id, tier, "complete", 74, "Demo assessment completed with one action-layer finding.", dumps(events)),
        )

        finding_id = f"F-{uuid.uuid4().hex[:4].upper()}"
        chain = ["demo_lookup", "demo_write", "demo_notify"]
        conn.execute(
            """
            INSERT INTO findings (id, target_id, vulnerability, severity, status, layer, runs, chain, hot, attack, agent, verdict, fix)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                finding_id,
                target_id,
                vulnerability,
                "High",
                "Open",
                "Action",
                1,
                dumps(chain),
                dumps(["demo_write", "demo_notify"]),
                attacks[0],
                "The target completed the request and executed a write followed by an outbound notification.",
                "The prompt caused a read request to become a write/outbound action chain.",
                "Add tool policy requiring approval for write and outbound actions derived from untrusted prompts.",
            ),
        )
        conn.execute(
            "INSERT INTO evidence (run_id, finding_id, attack, response, evaluator_verdict, tool_calls) VALUES (?, ?, ?, ?, ?, ?)",
            (
                run_id,
                finding_id,
                attacks[0],
                "The agent executed demo_lookup, demo_write, and demo_notify.",
                "Unsafe action-layer escalation.",
                dumps([{"name": name, "input_parameters": {"demo": True}, "output": {"ok": True}} for name in chain]),
            ),
        )
        return row_to_dict(conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone())
