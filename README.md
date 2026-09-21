# Red-Team Assurance POC

This repo contains a working red-team assurance POC for AI agents. It includes a Streamlit frontend, FastAPI backend, SQLite-backed demo data, dynamic YAML target onboarding, DBGuard-Bot as an example target, and optional Qwen/Ollama attacker prompt generation.

The POC is designed to show how an organization can onboard an AI agent, generate attacker prompts, run an assessment, capture evidence, and present findings in a simple dashboard.

## Executive Summary

This POC demonstrates an end-to-end AI-agent red-team workflow.

```text
Streamlit UI -> FastAPI backend -> attack generation -> assessment run -> findings/evidence
```

It is Qwen-ready through Ollama, but it also works without Ollama by using deterministic fallback attacker prompts. This makes the demo reliable even on machines where a local LLM cannot be started.

## What This POC Shows

- A frontend dashboard for AI-agent security posture.
- A backend API for targets, findings, runs, evidence, and prompt generation.
- Dynamic YAML onboarding for new AI agent targets.
- DBGuard-Bot as a realistic database/security assistant example.
- Attacker prompt generation through backend APIs.
- Optional Qwen/Ollama model support.
- Fallback mode when Qwen/Ollama is unavailable.
- SecMate-style contribution files for reusable configs, prompt templates, attack packs, and docs.

## Structure

```text
backend/                     FastAPI backend, SQLite store, runner, Qwen client
streamlit-redteam-poc/        Streamlit frontend
secMate-contribution-files/   SecMate-style contribution files
QWEN_BACKEND_RUNBOOK.md       Qwen/Ollama setup and run commands
dynamic-target-config.example.yaml  Generic dynamic target config example
dbguard-redteam-intake.yaml         DBGuard-Bot red-team intake
.gitignore
```

## Architecture

```text
User / Reviewer
      |
      v
Streamlit Frontend
      |
      v
FastAPI Backend
      |
      +--> SQLite demo store
      +--> Target onboarding
      +--> Assessment runner
      +--> Findings/evidence
      +--> Qwen/Ollama or fallback prompt generation
```

## Main Components

### Backend

The backend is implemented with FastAPI.

Important files:

```text
backend/main.py          API routes
backend/database.py      SQLite schema and seed data
backend/schemas.py       Request/response validation models
backend/runner.py        Assessment run creation and evidence generation
backend/model_client.py  Qwen/Ollama client and fallback prompts
backend/preflight.py     Target readiness checks
```

Important APIs:

```text
GET  /health
GET  /targets
GET  /findings
POST /runs
GET  /runs/{run_id}/evidence
POST /attacks/generate
POST /targets/import-yaml
```

### Frontend

The frontend is implemented with Streamlit.

Important pages:

```text
Portfolio posture   Leadership-level risk dashboard
Findings            Open findings and remediation details
New Assessment      Start a backend red-team run
Onboarding          Dynamic YAML onboarding guidance
Guard Telemetry     Evidence and telemetry view
Code And Demo       Project/code explanation
Backend Status      Backend and prompt generation test page
```

### SecMate Contribution Files

The `secMate-contribution-files/` folder contains reusable contribution files inspired by the SecMate-PoC repo structure.

It includes:

```text
configs/       Dynamic target configs
core/          Dynamic config loader and prompt template helpers
docs/          Integration and prompt-improvement documentation
attack_packs/  Database and attacker-prompt attack packs
```

## Example Target: DBGuard-Bot

DBGuard-Bot is a realistic example target used in this POC. It represents a read-only security database assistant.

The red-team scenarios focus on:

- unsafe SQL mutation requests
- tenant boundary expansion
- debug/secret extraction
- audit bypass framing
- unsafe tool parameter usage
- retrieved-content prompt injection

Expected safe behavior:

- only perform read-only actions
- refuse destructive SQL
- protect credentials and connection strings
- avoid cross-tenant data access
- treat retrieved content as data, not instructions

## Run Without Ollama

Use this mode if Ollama/Qwen cannot run on your machine. The backend will use deterministic fallback prompts.

### 1. Start Backend

```powershell
cd "C:\crucible\poc project\git files"
python -m uvicorn backend.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

### 2. Start Frontend

Open another PowerShell terminal:

```powershell
cd "C:\crucible\poc project\git files"
python -m streamlit run streamlit-redteam-poc\app.py
```

Open:

```text
http://localhost:8501
```

### 3. Demo Flow Without Ollama

In the Streamlit UI:

1. Open `Backend Status`.
2. Confirm the backend is reachable.
3. Keep `Use Qwen/Ollama model` unchecked.
4. Click `Generate attacks through backend`.
5. Open `New Assessment`.
6. Select `DBGuard-Bot`.
7. Keep Qwen/Ollama unchecked.
8. Click `Confirm and run demo assessment`.

## Run With Qwen/Ollama

If Ollama is available, start Qwen first:

```powershell
ollama pull qwen2.5:14b
ollama serve
```

Then start the backend and frontend using the same commands above.

In Streamlit, enable:

```text
Use Qwen/Ollama attacker model
```

When enabled, attacker prompt generation is sent to Qwen through the backend.

## Demo Script

Use this flow when presenting the POC.

### 1. Show GitHub Structure

Show these folders:

```text
backend/
streamlit-redteam-poc/
secMate-contribution-files/
```

Say:

```text
This is a complete frontend/backend POC. The backend handles assessment logic and data, the frontend presents the workflow, and the SecMate contribution folder contains reusable files for a SecMate-style repo.
```

### 2. Show Backend Docs

Open:

```text
http://localhost:8000/docs
```

Say:

```text
The backend exposes real APIs for targets, runs, findings, evidence, YAML import, and attacker prompt generation.
```

### 3. Show Dashboard

Open:

```text
http://localhost:8501
```

Say:

```text
This dashboard gives a portfolio-level view of AI-agent risk posture: pass rate, open findings, readiness, and regression cases.
```

### 4. Show Backend Status

Open `Backend Status`.

Say:

```text
This page proves the frontend is connected to FastAPI. It can also test attacker prompt generation through the backend.
```

### 5. Run New Assessment

Open `New Assessment`, choose `DBGuard-Bot`, and click `Confirm and run demo assessment`.

Say:

```text
This creates a backend run, generates attacks, records events, stores evidence, and returns findings.
```

### 6. Show Findings

Open `Findings`.

Say:

```text
Findings are structured with attack input, agent behavior, verdict, layer, severity, and remediation.
```

## Real Project Usage

This POC can be adapted for real AI-agent red-teaming.

Current POC flow:

```text
Frontend -> Backend -> simulated target response -> findings/evidence
```

Real project flow:

```text
Frontend -> Backend -> attacker prompt generator -> real target agent API -> evaluator -> findings/evidence
```

To use this with a real project, add:

- real target API connector
- target authentication
- tool-call and response capture
- stronger evaluator/judge logic
- secrets management through `.env`
- rate limits and approval controls
- exportable reports

## Limitations

This is a POC, not a production system.

Current limitations:

- target execution is simulated
- evaluator logic is simplified
- SQLite is used for demo storage
- authentication is not production-grade
- Qwen/Ollama is optional and local
- final report export is not fully implemented

## Future Improvements

- Connect to a real target agent API.
- Add stronger automated evaluator/judge scoring.
- Add PDF/HTML report export for each run.
- Add role-based access control.
- Add CI/CD red-team gate.
- Add more attack packs.
- Add multi-model attacker and judge support.
- Integrate with real observability traces.

## Troubleshooting

### Backend is not reachable

Start the backend:

```powershell
cd "C:\crucible\poc project\git files"
python -m uvicorn backend.main:app --reload --port 8000
```

Then refresh `Backend Status` in Streamlit.

### Port 8000 is already in use

Run backend on another port:

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

Then set the frontend backend URL before starting Streamlit:

```powershell
$env:REDTEAM_BACKEND_URL="http://localhost:8001"
python -m streamlit run streamlit-redteam-poc\app.py
```

### Ollama is unavailable

Keep Qwen/Ollama unchecked in the UI. The backend will use fallback prompts.

### Browser shows an old error

Stop Streamlit with `Ctrl + C`, restart it, and refresh the browser.

## Presentation Summary

```text
This POC demonstrates a complete red-team assurance workflow for AI agents. Streamlit provides the UI, FastAPI manages targets, assessment runs, attacker prompt generation, findings, and evidence, and the model layer is Qwen-ready through Ollama. DBGuard-Bot is included as a realistic example target for testing unsafe tool use, tenant boundary issues, secret leakage, and prompt injection risks.
```
