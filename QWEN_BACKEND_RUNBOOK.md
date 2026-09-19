# Qwen Backend Runbook

This project is now wired for a Qwen-backed red-team flow.

## What Runs Where

```text
Streamlit UI        http://localhost:8501
FastAPI backend     http://localhost:8000
Ollama/Qwen         http://localhost:11434
```

## 1. Start Qwen With Ollama

Install Ollama separately if it is not installed.

Pull the model:

```powershell
ollama pull qwen2.5:14b
```

Start Ollama if it is not already running:

```powershell
ollama serve
```

## 2. Start Backend

From the project root:

```powershell
cd "C:\crucible\poc project"
python -m uvicorn backend.main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

## 3. Start Streamlit UI

Open another PowerShell:

```powershell
cd "C:\crucible\poc project"
python -m streamlit run streamlit-redteam-poc\app.py
```

Open:

```text
http://localhost:8501
```

## 4. Test Qwen From UI

Go to:

```text
Backend status
```

Click:

```text
Generate attacks through backend
```

If Qwen/Ollama is running, Qwen generates the prompts.
If not, the backend falls back to demo prompts.

## 5. Run Assessment With Qwen

Go to:

```text
New assessment
```

Check:

```text
Use Qwen/Ollama attacker model when backend is available
```

Then start the assessment.

## Environment Variables

Defaults are already set in code:

```text
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen2.5:14b
REDTEAM_BACKEND_URL=http://localhost:8000
```

Override if needed:

```powershell
$env:OLLAMA_MODEL="qwen2.5:32b"
$env:REDTEAM_BACKEND_URL="http://localhost:8000"
```
