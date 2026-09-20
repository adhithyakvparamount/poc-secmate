from __future__ import annotations

import os
from typing import Any

import requests


BACKEND_URL = os.getenv("REDTEAM_BACKEND_URL", "http://localhost:8000")


class BackendUnavailable(RuntimeError):
    pass


def _url(path: str) -> str:
    return f"{BACKEND_URL.rstrip('/')}/{path.lstrip('/')}"


def health(timeout: float = 2.0) -> dict[str, Any]:
    try:
        response = requests.get(_url("/health"), timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise BackendUnavailable(str(exc)) from exc


def backend_available() -> bool:
    try:
        health()
        return True
    except BackendUnavailable:
        return False


def list_targets() -> list[dict[str, Any]]:
    response = requests.get(_url("/targets"), timeout=10)
    response.raise_for_status()
    return response.json()


def list_findings() -> list[dict[str, Any]]:
    response = requests.get(_url("/findings"), timeout=10)
    response.raise_for_status()
    return response.json()


def get_preflight(target_id: str) -> dict[str, Any]:
    response = requests.get(_url(f"/targets/{target_id}/preflight"), timeout=10)
    response.raise_for_status()
    return response.json()


def create_run(target_id: str, tier: str = "deep", use_model: bool = False) -> dict[str, Any]:
    response = requests.post(
        _url("/runs"),
        json={"target_id": target_id, "tier": tier, "use_model": use_model},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()


def get_run_evidence(run_id: str) -> list[dict[str, Any]]:
    response = requests.get(_url(f"/runs/{run_id}/evidence"), timeout=10)
    response.raise_for_status()
    return response.json()


def generate_attacks(target_purpose: str, vulnerability: str, count: int = 3, use_model: bool = True) -> list[str]:
    response = requests.post(
        _url("/attacks/generate"),
        json={"target_purpose": target_purpose, "vulnerability": vulnerability, "count": count, "use_model": use_model},
        timeout=180,
    )
    response.raise_for_status()
    return response.json().get("attacks", [])
