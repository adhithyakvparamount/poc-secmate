# Contribution Files For SecMate-PoC

These files are prepared to be added to the GitHub repo:

```text
https://github.com/Sai-Ashwin-AIDA/SecMate-PoC
```

They are kept in a separate local folder so you can copy only these contribution files into the repo and show your work clearly.

## What This Contribution Adds

This contribution improves the target YAML/config structure so SecMate can accept dynamic agent details instead of only fixed personas.

It adds support for:

- dynamic target metadata
- agent description
- system prompt
- guardrails
- API details
- tools and tool parameters
- architecture facts
- endpoints
- custom vulnerabilities
- compatibility with the existing SecMate-style persona YAML

## Files To Copy Into The Git Repo

Copy these files into the root of the SecMate-PoC repo:

```text
configs/dynamic_agent_template.yaml
configs/dbguard_dynamic_target.yaml
core/dynamic_config.py
docs/dynamic_target_config.md
docs/integration_notes.md
attack_packs/database_ops_attacks.yaml
attack_packs/improved_attacker_prompts.yaml
core/attacker_prompt_templates.py
docs/attacker_prompt_improvements.md
```

## Recommended Commit Message

```text
Add dynamic target config support for agent red-team assessments
```

## How To Explain Your Contribution

Use this sentence:

```text
I added a dynamic target configuration layer so SecMate can onboard any agent using YAML-defined metadata, API details, tools, guardrails and custom vulnerabilities, while staying compatible with the existing fixed persona configs.
```

Additional attacker prompt contribution:

```text
I also improved the attacker prompt layer by adding reusable, parameterized prompt patterns with expected defenses, so red-team probes are more realistic, repeatable and easier to evaluate.
```
