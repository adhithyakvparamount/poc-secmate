from __future__ import annotations


def evaluate_preflight(target: dict) -> list[dict]:
    endpoints = target.get("endpoints") or []
    roles = {endpoint.get("role") for endpoint in endpoints}
    route = target.get("route", "B")

    gates = [
        {
            "key": "cache",
            "state": "pass",
            "title": "Gateway cache bypass",
            "description": "Red-team requests will carry no-cache and run-id tags.",
            "why": "Prevents cached answers producing false stable pass rates.",
        },
        {
            "key": "manifest",
            "state": "pass" if "front_door" in roles else "fail",
            "title": "Tool manifest parity",
            "description": "A front-door endpoint is required so /_redteam/manifest can be checked.",
            "why": "Reduced staging capability creates false passes.",
        },
        {
            "key": "live",
            "state": "pass" if "staging" in roles else "fail",
            "title": "Target liveness and multi-turn",
            "description": "A staging endpoint is required for health and turn-history probes.",
            "why": "Multi-turn attacks must not silently degrade to single-turn.",
        },
        {
            "key": "soc",
            "state": "warn",
            "title": "SOC coordination",
            "description": "POC marks this as warning until a real SOC acknowledgement is connected.",
            "why": "Red-team traffic can page responders if uncoordinated.",
        },
        {
            "key": "roe",
            "state": "pass" if target.get("protected_window") else "warn",
            "title": "Rules of engagement",
            "description": "Protected testing window is present." if target.get("protected_window") else "Protected testing window is missing.",
            "why": "Without written scope, a run can look like an incident.",
        },
    ]

    if route == "B" and "trace" not in roles:
        gates.append(
            {
                "key": "trace",
                "state": "fail",
                "title": "Trace endpoint",
                "description": "Route B needs a trace endpoint to harvest tool-call evidence.",
                "why": "Action-layer cases need tool-call evidence with parameters and outputs.",
            }
        )
    if route == "C" and "proxy" not in roles:
        gates.append(
            {
                "key": "proxy",
                "state": "fail",
                "title": "MCP proxy endpoint",
                "description": "Route C needs a proxy endpoint for tool-call capture and enforcement.",
                "why": "MCP tools must be captured at the proxy path.",
            }
        )

    return gates
