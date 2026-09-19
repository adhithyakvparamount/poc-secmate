# Red-Team Assurance POC

This repo contains a Streamlit frontend, FastAPI backend, SQLite-backed demo data, dynamic YAML target onboarding, and optional Qwen/Ollama attacker prompt generation.

## Structure

```text
backend/                    FastAPI backend, SQLite store, runner, Qwen client
streamlit-redteam-poc/       Streamlit frontend
secMate-contribution-files/  Files prepared for SecMate-PoC contribution
QWEN_BACKEND_RUNBOOK.md      Qwen/Ollama setup and run commands
dynamic-target-config.example.yaml
dbguard-redteam-intake.yaml
```

## Run Qwen/Ollama

```powershell
ollama pull qwen2.5:14b
ollama serve
```

## Run Backend

```powershell
python -m uvicorn backend.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## Run Frontend

```powershell
python -m streamlit run streamlit-redteam-poc\app.py
```

Open:

```text
http://localhost:8501
```

Use the `Backend status` page to test FastAPI and Qwen prompt generation.
