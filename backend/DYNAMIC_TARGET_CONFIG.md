# Dynamic Target YAML Config

The backend now accepts dynamic target YAML instead of only fixed personas.

Use:

```http
POST /targets/import-yaml
```

Request body:

```json
{
  "yaml_text": "target:\n  id: dbguard\n  name: DBGuard-Bot\n...",
  "upsert": true
}
```

## Supported YAML Shapes

### 1. New Dynamic Schema

Use `dynamic-target-config.example.yaml`.

Top-level sections:

- `target` - id, name, owning team, purpose, route, transport, auth.
- `agent` - description, system prompt, guardrails and tools.
- `api` - base URL, red-team paths, timeout, headers.
- `architecture` - facts used to derive guide families and default vulnerability classes.
- `endpoints` - front door, staging, trace or proxy endpoints.
- `custom_vulnerabilities` - project-specific risks.

### 2. SecMate-Style Persona YAML

The backend also accepts the existing SecMate shape:

```yaml
name: "DBGuard-Bot"
description: "Assists analysts..."
system_prompt: >
  You are DBGuard...
guardrails:
  - "Only generate SELECT queries..."
tools:
  - name: query_security_db
    description: "Executes approved read-only SELECT queries."
    parameters:
      - name: sql_query
        type: string
        required: true
```

When this format is imported, the backend automatically creates a target id, purpose, basic architecture, guides and default classes.

## Why This Matters

This lets the POC onboard any agent dynamically:

- Database assistant
- SOC agent
- Identity access bot
- Claims assistant
- HR copilot
- Any future company project

No code change is required for new tools or guardrails.
