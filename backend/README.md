# Red Team POC Backend

This is the FastAPI backend for the generic red-team assurance POC.

It provides:

- Targets API
- Findings API
- Preflight checks
- Run creation and simulated execution
- Evidence API
- Optional Qwen2.5/Ollama attack generation fallback
- SQLite storage

## Install

From the project root:

```powershell
python -m pip install -r backend\requirements.txt
```

## Run

```powershell
cd "C:\crucible\poc project"
python -m uvicorn backend.main:app --reload --port 8000
```

Open API docs:

```text
http://localhost:8000/docs
```

Health check:

```text
http://localhost:8000/health
```

## Optional Qwen2.5 With Ollama

Install and run Ollama separately, then pull a Qwen model:

```powershell
ollama pull qwen2.5:14b
```

The backend uses these defaults:

```text
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5:14b
```

If Ollama is not available, the backend falls back to demo attack prompts.

See also:

```text
..\QWEN_BACKEND_RUNBOOK.md
```

## Main Endpoints

- `GET /targets`
- `POST /targets`
- `GET /targets/{target_id}/preflight`
- `GET /findings`
- `POST /findings`
- `POST /runs`
- `GET /runs`
- `GET /runs/{run_id}`
- `GET /runs/{run_id}/evidence`
- `POST /attacks/generate`

## Current Scope

This backend is production-shaped but still POC-safe. It does not call real company project endpoints yet. The next step is adding `target_client.py` that calls each real target's `/_redteam/turn`, `/_redteam/manifest`, and `/_redteam/health` endpoints.
