# Dynamic Target Configuration

## Why This Is Needed

The current SecMate configs are fixed persona YAML files. They work well for known personas, but new company agents may need extra details such as:

- owning team
- protected test window
- API endpoint
- target transport
- agent tools
- tool parameters
- custom vulnerabilities
- architecture facts
- trace/proxy endpoints

This contribution adds a richer dynamic config structure while preserving compatibility with the existing persona YAML format.

## New Config Sections

```yaml
target:
  id: dbguard
  name: DBGuard-Bot
  owning_team: Security Data Platform
  purpose: "..."

agent:
  description: "..."
  system_prompt: "..."
  guardrails: []
  tools: []

api:
  base_url: "https://target.staging.internal"
  turn_path: "/_redteam/turn"
  manifest_path: "/_redteam/manifest"
  health_path: "/_redteam/health"

architecture:
  calls_tools: true
  ingests_untrusted: true

endpoints: []
custom_vulnerabilities: []
```

## Backward Compatibility

The loader in `core/dynamic_config.py` also accepts current SecMate configs like:

```yaml
name: "DBGuard-Bot"
description: "..."
system_prompt: "..."
guardrails:
  - "..."
tools:
  - name: query_security_db
```

It normalizes those files into the dynamic structure automatically.

## Example Files

- `configs/dynamic_agent_template.yaml`
- `configs/dbguard_dynamic_target.yaml`
- `attack_packs/database_ops_attacks.yaml`
