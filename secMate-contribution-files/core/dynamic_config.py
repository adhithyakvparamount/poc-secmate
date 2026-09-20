"""Dynamic target config support for SecMate-PoC.

This module lets SecMate load richer target YAML files with target metadata,
agent details, API settings, tools, endpoints, architecture facts, and custom
vulnerabilities, while remaining compatible with the existing fixed persona
YAML format used by configs/*.yaml.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import BaseModel, Field, ValidationError

from core.models import TargetAgentProfile, ToolDefinition


class DynamicEndpoint(BaseModel):
    label: str
    role: str
    url: str


class DynamicApiConfig(BaseModel):
    base_url: str = ""
    turn_path: str = "/_redteam/turn"
    manifest_path: str = "/_redteam/manifest"
    health_path: str = "/_redteam/health"
    timeout_seconds: int = 30
    headers: Dict[str, str] = Field(default_factory=dict)


class DynamicTargetMetadata(BaseModel):
    id: str
    name: str
    owning_team: str = "Unassigned"
    surface: str = "Agentic target"
    purpose: str = ""
    auth: str = "workload"
    transport: str = "http"
    route: str = "B"
    protected_window: str = ""


class DynamicAgentBlock(BaseModel):
    description: str = ""
    system_prompt: str = ""
    guardrails: List[str] = Field(default_factory=list)
    tools: List[ToolDefinition] = Field(default_factory=list)


class DynamicTargetConfig(BaseModel):
    target: DynamicTargetMetadata
    agent: DynamicAgentBlock = Field(default_factory=DynamicAgentBlock)
    api: DynamicApiConfig = Field(default_factory=DynamicApiConfig)
    architecture: Dict[str, Any] = Field(default_factory=dict)
    endpoints: List[DynamicEndpoint] = Field(default_factory=list)
    custom_vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list)
    raw_source: Dict[str, Any] = Field(default_factory=dict)

    def to_target_profile(self) -> TargetAgentProfile:
        description = self.agent.description or self.target.purpose or self.target.surface
        return TargetAgentProfile(
            name=self.target.name,
            description=description,
            system_prompt=self.agent.system_prompt,
            guardrails=self.agent.guardrails,
            tools=self.agent.tools,
        )


@dataclass
class DynamicTargetLoadResult:
    config: DynamicTargetConfig
    profile: TargetAgentProfile
    warnings: List[str] = field(default_factory=list)


def load_dynamic_target_config(path: str | Path) -> DynamicTargetLoadResult:
    """Load either the new dynamic schema or the existing SecMate persona schema."""
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle) or {}

    if not isinstance(raw, dict):
        raise ValueError(f"Target config {file_path} must be a YAML mapping/object.")

    warnings: List[str] = []
    if "target" in raw:
        config = _load_new_schema(raw)
    else:
        config = _load_legacy_persona_schema(raw, warnings)

    return DynamicTargetLoadResult(config=config, profile=config.to_target_profile(), warnings=warnings)


def _load_new_schema(raw: Dict[str, Any]) -> DynamicTargetConfig:
    try:
        target_block = raw.get("target") or {}
        agent_block = raw.get("agent") or {}
        normalized = {
            "target": target_block,
            "agent": agent_block,
            "api": raw.get("api") or {},
            "architecture": raw.get("architecture") or {},
            "endpoints": raw.get("endpoints") or [],
            "custom_vulnerabilities": raw.get("custom_vulnerabilities") or [],
            "raw_source": raw,
        }
        return DynamicTargetConfig.model_validate(normalized)
    except ValidationError as exc:
        raise ValueError(f"Dynamic target config validation failed: {exc}") from exc


def _load_legacy_persona_schema(raw: Dict[str, Any], warnings: List[str]) -> DynamicTargetConfig:
    """Convert existing SecMate configs/name-description-system_prompt-tools into the dynamic shape."""
    name = raw.get("name")
    if not name:
        raise ValueError("Legacy persona config must include a 'name'.")

    warnings.append("Loaded legacy persona YAML and normalized it to DynamicTargetConfig.")
    target_id = str(name).lower().replace(" ", "-").replace("_", "-")
    normalized = {
        "target": {
            "id": target_id,
            "name": name,
            "owning_team": raw.get("owning_team", "Unassigned"),
            "surface": raw.get("surface", "Agentic target"),
            "purpose": raw.get("description", ""),
            "auth": raw.get("auth", "workload"),
            "transport": raw.get("transport", "http"),
            "route": raw.get("route", "B"),
            "protected_window": raw.get("protected_window", ""),
        },
        "agent": {
            "description": raw.get("description", ""),
            "system_prompt": raw.get("system_prompt", ""),
            "guardrails": raw.get("guardrails") or [],
            "tools": raw.get("tools") or [],
        },
        "api": raw.get("api") or {},
        "architecture": raw.get("architecture") or {"calls_tools": bool(raw.get("tools")), "ingests_untrusted": True},
        "endpoints": raw.get("endpoints") or [],
        "custom_vulnerabilities": raw.get("custom_vulnerabilities") or [],
        "raw_source": raw,
    }
    return DynamicTargetConfig.model_validate(normalized)


def dynamic_config_to_summary(config: DynamicTargetConfig) -> Dict[str, Any]:
    """Small serializable summary useful for Streamlit UI panels."""
    return {
        "id": config.target.id,
        "name": config.target.name,
        "owning_team": config.target.owning_team,
        "surface": config.target.surface,
        "purpose": config.target.purpose,
        "tool_count": len(config.agent.tools),
        "guardrail_count": len(config.agent.guardrails),
        "endpoint_count": len(config.endpoints),
        "api_base_url": config.api.base_url,
        "custom_vulnerability_count": len(config.custom_vulnerabilities),
    }
