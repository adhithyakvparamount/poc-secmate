from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Endpoint(BaseModel):
    label: str
    role: Literal["front_door", "staging", "trace", "proxy"]
    url: str


class TargetCreate(BaseModel):
    id: str = Field(pattern=r"^[a-z0-9_-]+$")
    name: str
    owning_team: str
    purpose: str
    description: str = ""
    system_prompt: str = ""
    guardrails: list[str] = Field(default_factory=list)
    tools: list[dict[str, Any]] = Field(default_factory=list)
    api: dict[str, Any] = Field(default_factory=dict)
    surface: str = "Agentic project"
    auth: str = "workload"
    route: str = "B"
    transport: str = "http"
    protected_window: str = ""
    guides: list[str] = Field(default_factory=list)
    classes: dict[str, int] = Field(default_factory=dict)
    architecture: dict[str, Any] = Field(default_factory=dict)
    endpoints: list[Endpoint] = Field(default_factory=list)
    custom_vulnerabilities: list[dict[str, Any]] = Field(default_factory=list)


class RunCreate(BaseModel):
    target_id: str
    tier: Literal["ci", "deep", "framework"] = "deep"
    use_model: bool = False


class AttackGenerateRequest(BaseModel):
    target_purpose: str
    vulnerability: str
    count: int = 3
    use_model: bool = True


class FindingCreate(BaseModel):
    target_id: str
    vulnerability: str
    severity: Literal["High", "Medium", "Low"] = "Medium"
    status: str = "Open"
    layer: str = "Action"
    chain: list[str] = Field(default_factory=list)
    hot: list[str] = Field(default_factory=list)
    attack: str
    agent: str
    verdict: str
    fix: str


class TargetYamlImport(BaseModel):
    yaml_text: str
    upsert: bool = True
