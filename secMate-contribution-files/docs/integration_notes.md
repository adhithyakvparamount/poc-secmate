# Integration Notes

These notes explain how to wire the contribution into the existing SecMate-PoC app.

## 1. Add The Files

Copy these into the SecMate-PoC repo:

```text
configs/dynamic_agent_template.yaml
configs/dbguard_dynamic_target.yaml
core/dynamic_config.py
docs/dynamic_target_config.md
docs/integration_notes.md
attack_packs/database_ops_attacks.yaml
```

## 2. Use Dynamic Loader In Python

The existing code uses:

```python
from core.loader import load_target_profile

profile = load_target_profile(config_path)
```

For dynamic configs, use:

```python
from core.dynamic_config import load_dynamic_target_config

loaded = load_dynamic_target_config(config_path)
profile = loaded.profile
summary = loaded.config
```

`profile` is still a `TargetAgentProfile`, so it can be passed into the existing `AuditOrchestrator`.

## 3. Streamlit UI Suggestion

In `app.py`, detect whether a config file contains a top-level `target` block.

Pseudo-code:

```python
if "target" in yaml.safe_load(open(config_path)):
    loaded = load_dynamic_target_config(config_path)
    profile = loaded.profile
else:
    profile = load_target_profile(config_path)
```

## 4. Attack Library Extension

The file `attack_packs/database_ops_attacks.yaml` can be merged into or shown alongside `attack_library.yaml`.

It adds DB-specific tests for:

- SQL mutation intent rewrite
- cross-tenant scope expansion
- connection string debug extraction
- audit bypass framing

## 5. Contribution Summary

This contribution makes SecMate more generic. It can now onboard arbitrary agent projects with API details and tool schemas instead of depending only on fixed persona YAML files.
