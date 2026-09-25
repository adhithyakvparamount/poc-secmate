# SecMate - Adhithya Branch

SecMate is a Streamlit proof of concept for configuring and running basic adversarial HTTP assessments against authorized AI-agent endpoints. The repository combines a cybersecurity dashboard with a synchronous prompt runner and rule-based response evaluation.

The detailed source of truth for this branch is [Documents/TRD(A).md](Documents/TRD(A).md). It describes the as-built architecture, request contract, assessment behavior, data lifecycle, security boundaries, known gaps, and branch-correlation policy.

## Current Capabilities

- Mock sign-in and first-run onboarding.
- Session-backed language, environment, density, and onboarding preferences.
- Multipage Streamlit dashboard and assessment workflow.
- HTTP target, authentication, and attack-category configuration.
- Predefined adversarial prompt execution.
- Basic response extraction and deterministic evaluation.
- In-session Red/Blue exchange and VAPT finding views.

This is not yet a production security platform. Authentication, dashboard metrics, reports, integrations, settings, and profile persistence are mock or partial. Assessment results are stored only in Streamlit session state.

## Project Structure

```text
secmate_ui/
|-- app.py                       # Login gate, onboarding, and dashboard
|-- assessment_runner.py         # HTTP prompt runner and evaluator
|-- login_screen.py              # Mock sign-in interface
|-- authcheck.py                 # Page-level session guard
|-- theme.py                     # Shared styles and UI helpers
|-- workspace.py                 # Preferences, onboarding profiles, and localization
|-- requirements.txt
|-- Documents/
|   `-- TRD(A).md                # As-built technical source of truth
`-- pages/
    |-- 1_New_Assessment.py
    |-- 2_Red_Blue_Team.py
    |-- 3_VAPT_Findings.py
    |-- 4_Reports.py
    |-- 5_Integrations.py
    |-- 6_Settings.py
    `-- 7_Profile.py
```

## Run Locally

Python 3.10 or newer is recommended.

```bash
pip install -r requirements.txt
streamlit run app.py
```

The mock sign-in accepts any nonempty email and password. Do not treat it as a production authentication control.

## Assessment Contract

The proof-of-concept runner sends JSON `POST` requests containing both `message` and `prompt` fields. The target should return plain text or a supported top-level JSON string field such as `response`, `answer`, `message`, `content`, `text`, or `output`.

Only assess systems that you are explicitly authorized to test. The current implementation does not independently validate target ownership and does not yet protect against unsafe outbound endpoint selection.

## Documentation

- [As-built TRD and engineering knowledge base](Documents/TRD(A).md)

The TRD can correlate this branch with contextual material on `main`, but documentation from `main` is not a hardcoded instruction or automatic authority over the `adhithya` implementation.
