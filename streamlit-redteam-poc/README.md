# Streamlit Red Team Assurance POC

This is a Streamlit UI version of the generic red-team assurance POC.

## Run

From this folder:

```powershell
pip install -r requirements.txt
streamlit run app.py
```

Or from the project root:

```powershell
pip install -r streamlit-redteam-poc\requirements.txt
streamlit run streamlit-redteam-poc\app.py
```

## Pages

- `Portfolio posture` - target overview and risk posture.
- `Findings triage` - evidence-backed finding review.
- `New assessment` - preflight gates and live run simulation.
- `Project onboarding` - intake form and YAML parser.
- `Guard telemetry` - runtime guard signals and limits.
- `Code + demo notes` - demo script, protocol and file layout.

## Applying Real Project Info

Use these files:

- `APPLY-YOUR-PROJECT-INFO.md` - step-by-step instructions.
- `project-info-template.py` - copy/paste target and finding templates.
- `data.py` - replace demo projects/findings with real values.
- `../generic-project-intake.yaml` - fill real onboarding details.

## Why Streamlit

Streamlit is useful for this POC because it is quick to run, easy to explain, and ready to connect to Python-based backend logic later.

## Backend + Qwen Mode

Run the backend first:

```powershell
cd "C:\crucible\poc project"
python -m uvicorn backend.main:app --reload --port 8000
```

Optional Qwen/Ollama:

```powershell
ollama pull qwen2.5:14b
ollama serve
```

Then run Streamlit and open the `Backend status` page.

Full instructions are in:

```text
..\QWEN_BACKEND_RUNBOOK.md
```
