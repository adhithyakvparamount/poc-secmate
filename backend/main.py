from __future__ import annotations

import uuid

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import connect, dumps, row_to_dict, rows_to_dicts, setup
from .model_client import generate_attacks
from .preflight import evaluate_preflight
from .runner import create_and_run
import yaml

from .schemas import AttackGenerateRequest, FindingCreate, RunCreate, TargetCreate, TargetYamlImport


setup()

app = FastAPI(title="Red Team Assurance POC Backend", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"ok": True, "service": "redteam-poc-backend"}


@app.get("/targets")
def list_targets() -> list[dict]:
    with connect() as conn:
        return rows_to_dicts(conn.execute("SELECT * FROM targets ORDER BY name").fetchall())


@app.get("/targets/{target_id}")
def get_target(target_id: str) -> dict:
    with connect() as conn:
        target = row_to_dict(conn.execute("SELECT * FROM targets WHERE id = ?", (target_id,)).fetchone())
        if not target:
            raise HTTPException(status_code=404, detail="target not found")
        return target


@app.post("/targets", status_code=201)
def create_target(payload: TargetCreate) -> dict:
    with connect() as conn:
        try:
            conn.execute(
                """
                INSERT INTO targets (id, name, owning_team, purpose, surface, description, system_prompt, guardrails, tools, api, auth, route, transport, protected_window, guides, classes, high, medium, rate, architecture, endpoints, custom_vulnerabilities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.id,
                    payload.name,
                    payload.owning_team,
                    payload.purpose,
                    payload.surface,
                    payload.description,
                    payload.system_prompt,
                    dumps(payload.guardrails),
                    dumps(payload.tools),
                    dumps(payload.api),
                    payload.auth,
                    payload.route,
                    payload.transport,
                    payload.protected_window,
                    dumps(payload.guides),
                    dumps(payload.classes),
                    0,
                    0,
                    0,
                    dumps(payload.architecture),
                    dumps([endpoint.model_dump() for endpoint in payload.endpoints]),
                    dumps(payload.custom_vulnerabilities),
                ),
            )
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return get_target(payload.id)


@app.post("/targets/import-yaml", status_code=201)
def import_target_yaml(payload: TargetYamlImport) -> dict:
    try:
        raw = yaml.safe_load(payload.yaml_text)
    except yaml.YAMLError as exc:
        raise HTTPException(status_code=400, detail=f"invalid yaml: {exc}") from exc
    if not isinstance(raw, dict):
        raise HTTPException(status_code=400, detail="yaml must be a mapping/object")

    target = normalize_target_yaml(raw)
    with connect() as conn:
        exists = conn.execute("SELECT 1 FROM targets WHERE id = ?", (target.id,)).fetchone()
        if exists and not payload.upsert:
            raise HTTPException(status_code=409, detail="target already exists")
        if exists:
            conn.execute(
                """
                UPDATE targets SET name=?, owning_team=?, purpose=?, surface=?, description=?, system_prompt=?, guardrails=?, tools=?, api=?, auth=?, route=?, transport=?, protected_window=?, guides=?, classes=?, architecture=?, endpoints=?, custom_vulnerabilities=?
                WHERE id=?
                """,
                (
                    target.name,
                    target.owning_team,
                    target.purpose,
                    target.surface,
                    target.description,
                    target.system_prompt,
                    dumps(target.guardrails),
                    dumps(target.tools),
                    dumps(target.api),
                    target.auth,
                    target.route,
                    target.transport,
                    target.protected_window,
                    dumps(target.guides),
                    dumps(target.classes),
                    dumps(target.architecture),
                    dumps([endpoint.model_dump() for endpoint in target.endpoints]),
                    dumps(target.custom_vulnerabilities),
                    target.id,
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO targets (id, name, owning_team, purpose, surface, description, system_prompt, guardrails, tools, api, auth, route, transport, protected_window, guides, classes, high, medium, rate, architecture, endpoints, custom_vulnerabilities)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    target.id,
                    target.name,
                    target.owning_team,
                    target.purpose,
                    target.surface,
                    target.description,
                    target.system_prompt,
                    dumps(target.guardrails),
                    dumps(target.tools),
                    dumps(target.api),
                    target.auth,
                    target.route,
                    target.transport,
                    target.protected_window,
                    dumps(target.guides),
                    dumps(target.classes),
                    0,
                    0,
                    0,
                    dumps(target.architecture),
                    dumps([endpoint.model_dump() for endpoint in target.endpoints]),
                    dumps(target.custom_vulnerabilities),
                ),
            )
    return get_target(target.id)


def normalize_target_yaml(raw: dict) -> TargetCreate:
    # Supports both the new dynamic schema and SecMate-style fixed persona YAML.
    if "target" in raw:
        target_block = raw.get("target") or {}
        agent_block = raw.get("agent") or raw.get("source_agent_config") or {}
        api = raw.get("api") or agent_block.get("api") or {}
        endpoints = raw.get("endpoints") or []
        name = target_block.get("name") or agent_block.get("name") or raw.get("name")
        purpose = target_block.get("purpose") or agent_block.get("description") or raw.get("description") or ""
        return TargetCreate(
            id=(target_block.get("id") or str(name).lower().replace(" ", "-").replace("_", "-")),
            name=name,
            owning_team=target_block.get("owning_team") or raw.get("owning_team") or "Unassigned",
            purpose=purpose,
            description=agent_block.get("description") or raw.get("description") or purpose,
            system_prompt=agent_block.get("system_prompt") or raw.get("system_prompt") or "",
            guardrails=agent_block.get("guardrails") or raw.get("guardrails") or [],
            tools=agent_block.get("tools") or raw.get("tools") or [],
            api=api,
            surface=target_block.get("surface") or raw.get("surface") or "Agentic project",
            auth=target_block.get("auth", "workload"),
            route=target_block.get("route", "B"),
            transport=target_block.get("transport", "http"),
            protected_window=target_block.get("protected_window", ""),
            guides=raw.get("guides") or derive_guides(raw.get("architecture") or {}),
            classes=raw.get("classes") or derive_classes(raw.get("architecture") or {}, raw.get("custom_vulnerabilities") or []),
            architecture=raw.get("architecture") or {},
            endpoints=endpoints,
            custom_vulnerabilities=raw.get("custom_vulnerabilities") or [],
        )

    name = raw.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="yaml must include name or target.name")
    return TargetCreate(
        id=str(name).lower().replace(" ", "-").replace("_", "-"),
        name=name,
        owning_team=raw.get("owning_team", "Unassigned"),
        purpose=raw.get("description", ""),
        description=raw.get("description", ""),
        system_prompt=raw.get("system_prompt", ""),
        guardrails=raw.get("guardrails", []),
        tools=raw.get("tools", []),
        api=raw.get("api", {}),
        surface=raw.get("surface", "Agentic project"),
        guides=raw.get("guides", ["Agents"]),
        classes=raw.get("classes", {"ToolOrchestrationAbuse": 70, "IndirectInstruction": 70}),
        architecture=raw.get("architecture", {"calls_tools": bool(raw.get("tools")), "ingests_untrusted": True}),
        endpoints=raw.get("endpoints", []),
        custom_vulnerabilities=raw.get("custom_vulnerabilities", []),
    )


def derive_guides(architecture: dict) -> list[str]:
    guides = []
    if architecture.get("calls_tools") or architecture.get("delegates_subagents"):
        guides.append("Agents")
    if architecture.get("retrieval_backed"):
        guides.append("RAG")
    if architecture.get("stateful_sessions"):
        guides.append("Conversational")
    return guides or ["Agents"]


def derive_classes(architecture: dict, custom_vulnerabilities: list[dict]) -> dict[str, int]:
    classes = {}
    if architecture.get("calls_tools"):
        classes.update({"ExcessiveAgency": 70, "ToolOrchestrationAbuse": 70, "ExploitToolAgent": 70})
    if architecture.get("ingests_untrusted"):
        classes["IndirectInstruction"] = 70
    if architecture.get("delegates_subagents"):
        classes["InsecureInterAgentCommunication"] = 70
    for vuln in custom_vulnerabilities:
        if isinstance(vuln, dict) and vuln.get("name"):
            classes[str(vuln["name"]).replace(" ", "")] = 70
    return classes or {"GoalTheft": 70}


@app.get("/targets/{target_id}/preflight")
def preflight(target_id: str) -> dict:
    target = get_target(target_id)
    gates = evaluate_preflight(target)
    return {"target_id": target_id, "blocking": [gate for gate in gates if gate["state"] == "fail"], "gates": gates}


@app.get("/findings")
def list_findings(target_id: str | None = None) -> list[dict]:
    query = """
        SELECT findings.*, targets.name AS target_name
        FROM findings JOIN targets ON findings.target_id = targets.id
    """
    params: tuple = ()
    if target_id:
        query += " WHERE findings.target_id = ?"
        params = (target_id,)
    query += " ORDER BY findings.created_at DESC"
    with connect() as conn:
        return rows_to_dicts(conn.execute(query, params).fetchall())


@app.get("/findings/{finding_id}")
def get_finding(finding_id: str) -> dict:
    with connect() as conn:
        finding = row_to_dict(
            conn.execute(
                """
                SELECT findings.*, targets.name AS target_name
                FROM findings JOIN targets ON findings.target_id = targets.id
                WHERE findings.id = ?
                """,
                (finding_id,),
            ).fetchone()
        )
        if not finding:
            raise HTTPException(status_code=404, detail="finding not found")
        return finding


@app.post("/findings", status_code=201)
def create_finding(payload: FindingCreate) -> dict:
    finding_id = f"F-{uuid.uuid4().hex[:6].upper()}"
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO findings (id, target_id, vulnerability, severity, status, layer, runs, chain, hot, attack, agent, verdict, fix)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                finding_id,
                payload.target_id,
                payload.vulnerability,
                payload.severity,
                payload.status,
                payload.layer,
                1,
                dumps(payload.chain),
                dumps(payload.hot),
                payload.attack,
                payload.agent,
                payload.verdict,
                payload.fix,
            ),
        )
    return get_finding(finding_id)


@app.post("/runs", status_code=201)
def create_run(payload: RunCreate) -> dict:
    try:
        return create_and_run(payload.target_id, payload.tier, payload.use_model)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/runs")
def list_runs() -> list[dict]:
    with connect() as conn:
        return rows_to_dicts(conn.execute("SELECT * FROM runs ORDER BY created_at DESC").fetchall())


@app.get("/runs/{run_id}")
def get_run(run_id: str) -> dict:
    with connect() as conn:
        run = row_to_dict(conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone())
        if not run:
            raise HTTPException(status_code=404, detail="run not found")
        return run


@app.get("/runs/{run_id}/evidence")
def get_run_evidence(run_id: str) -> list[dict]:
    with connect() as conn:
        return rows_to_dicts(conn.execute("SELECT * FROM evidence WHERE run_id = ? ORDER BY id", (run_id,)).fetchall())


@app.post("/attacks/generate")
def generate_attack_prompts(payload: AttackGenerateRequest) -> dict:
    attacks = generate_attacks(payload.target_purpose, payload.vulnerability, payload.count, use_model=payload.use_model)
    return {"attacks": attacks}
