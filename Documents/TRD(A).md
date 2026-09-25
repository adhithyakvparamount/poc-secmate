# SecMate Technical Requirements Document - Adhithya Branch

- **Document type:** As-built technical requirements and engineering knowledge base
- **Branch:** `adhithya`
- **Application:** SecMate Streamlit UI and assessment proof of concept
- **Last reviewed:** September 25, 2026

[Return to the project README](../README.md)

## 1. Purpose

This document is the source of truth for the software currently implemented on the `adhithya` branch. It describes the application as it exists today, including its architecture, workflows, interfaces, data lifecycle, limitations, and intended next steps.

It is written for developers, reviewers, automated coding agents, security engineers, and future project sessions that need to understand the repository without relying on assumptions from screenshots or older documentation.

### 1.1 Branch correlation context

This document may be used by an agent or contributor to correlate the implementation on the `adhithya` branch with product context, design history, or documentation found on the `main` branch.

That correlation is informational only. Nothing in a TRD or other document on `main` is a hardcoded instruction for work on `adhithya`, and content from `main` must not automatically override the current code, this as-built TRD, explicit user requirements, or later approved decisions. Differences between branches should be identified and evaluated rather than silently merged or treated as mandatory behavior.

### 1.2 Source-of-truth order

For work on `adhithya`, use this order when information conflicts:

1. Explicit requirements approved for the current task.
2. Current executable code and tests on `adhithya`.
3. This as-built TRD.
4. The root [README](../README.md).
5. Historical material or documentation from other branches.

The code remains the final authority for observed runtime behavior. This document should be updated whenever an approved change makes a section materially inaccurate.

## 2. Product Summary

SecMate is a Streamlit application for configuring and running basic adversarial HTTP tests against an authorized AI-agent endpoint. It combines a cybersecurity-oriented user interface with a small synchronous assessment runner.

The current application supports:

- Mock sign-in and first-run onboarding.
- Session-backed language, environment, dashboard density, and per-email onboarding profiles.
- A multi-page security dashboard.
- Configuration of an HTTP target and request credential.
- Selection of adversarial prompt categories.
- Sequential POST requests to the target.
- Rule-based evaluation of text responses.
- In-memory display of exchanges and findings.

The current application is a proof of concept. It is not yet an enterprise assessment platform, production authentication system, persistent audit service, semantic LLM judge, or action-space interception framework.

## 3. Repository Structure

```text
secmate_ui/
|-- app.py
|-- assessment_runner.py
|-- authcheck.py
|-- login_screen.py
|-- theme.py
|-- workspace.py
|-- requirements.txt
|-- README.md
|-- Documents/
|   `-- TRD(A).md
`-- pages/
    |-- 1_New_Assessment.py
    |-- 2_Red_Blue_Team.py
    |-- 3_VAPT_Findings.py
    |-- 4_Reports.py
    |-- 5_Integrations.py
    |-- 6_Settings.py
    `-- 7_Profile.py
```

Generated Python bytecode and local virtual environments are not application source and should not be used as documentation inputs.

## 4. Runtime Architecture

### 4.1 Architecture overview

The application is a monolithic Streamlit multipage application.

```text
Browser
  |
  v
Streamlit process
  |-- app.py                 Login gate, onboarding, dashboard
  |-- pages/*.py             Page-level workflows and presentation
  |-- assessment_runner.py   Synchronous HTTP probes and evaluation
  |-- authcheck.py           Session-state route guard
  |-- login_screen.py        Mock sign-in interface
  `-- theme.py               Shared styling and UI helpers
```

There is no separate backend service, database, worker queue, repository layer, API server, or persistent audit store. Streamlit reruns the active script in response to user interactions, and most state is maintained in `st.session_state`.

### 4.2 Entry point

The application starts with:

```bash
streamlit run app.py
```

`app.py` configures the page and controls the top-level sequence:

1. Initialize the authentication state if needed.
2. Render the login screen when unauthenticated.
3. Apply the shared visual theme.
4. Render onboarding until it has been completed for the session.
5. Render the sidebar and dashboard.

### 4.3 Major modules

#### `app.py`

Responsibilities:

- Application entry point.
- Authentication gate.
- First-login onboarding flow.
- Dashboard layout.
- Static summary metrics, risk distribution, and recent-run data.
- Navigation to the assessment page.

Important functions:

- `get_onboarding_steps()`
- `render_onboarding_loading()`
- `render_onboarding_page()`
- `get_summary_metrics()`
- `get_risk_distribution()`
- `get_recent_runs()`
- `render_dashboard_header()`
- `render_quick_start_panel()`

#### `assessment_runner.py`

Responsibilities:

- Store the predefined adversarial prompt bank.
- Build a bounded list of prompts.
- Send synchronous JSON requests to a target endpoint.
- Extract response text from common JSON fields.
- Evaluate responses with string-based heuristics.
- Create in-memory finding records.

Important functions and constants:

- `PROMPT_BANK`
- `REFUSAL_MARKERS`
- `LEAK_MARKERS`
- `build_prompts()`
- `run_assessment()`
- `call_target()`
- `extract_response_text()`
- `evaluate_response()`
- `build_finding()`
- `remediation_for()`

#### `authcheck.py`

`require_auth()` protects Streamlit pages by requiring both an authenticated session and completed onboarding. A failed check redirects the user to `app.py` and stops execution of the requested page.

#### `login_screen.py`

Provides the sign-in presentation and `_attempt_sign_in()` behavior. Authentication is currently mocked and accepts any nonempty email and password.

#### `theme.py`

Contains shared color definitions, theme presets, global CSS, sidebar branding, status helpers, metric cards, severity badges, and logout behavior.

#### `workspace.py`

Defines the session-backed workspace model, translations, stable option values, per-email onboarding profiles, and preference load/save helpers. Language changes primary shell text, environment is attached to assessment runs, and dashboard density changes shared spacing and card padding.

## 5. User Journey

### 5.1 Sign-in

The user selects an organization and enters an email and password. The current implementation does not verify either value against an identity provider or database. Any nonempty email and password result in an authenticated session.

Successful sign-in initializes:

- `authenticated = True`
- `user_email = <entered email>`

If the email has a completed onboarding profile in the current session, the application restores its language, environment, density, user type, use case, and goal and skips onboarding. Otherwise, onboarding is shown.

The organization selector is visual only, and SSO is not connected.

### 5.2 Onboarding

After sign-in, the application displays a loading transition and an onboarding page. It collects:

- User type.
- Intended SecMate use case.
- Optional free-text goal.
- Language.
- Workspace environment.
- Dashboard density.

Selecting **Enter Dashboard** stores these values in a per-email session profile and sets `onboarding_seen = True`. The profile is restored when the same email signs in again during the same Streamlit session.

### 5.3 Dashboard

The dashboard contains:

- Workspace header and onboarding context.
- Quick-start guidance.
- Summary metric cards.
- Risk distribution visualization.
- Findings by severity.
- Recent-assessment table.

These dashboard values are currently hardcoded sample data and do not update from assessment history.

### 5.4 Assessment execution

The New Assessment page collects target, credential, model, module, and attack-category settings. When validation succeeds, it calls `run_assessment()` synchronously and stores the result in session state.

### 5.5 Result review

The Red/Blue Team and VAPT Findings pages read the latest in-session assessment history. If no usable assessment data exists, these pages can display sample data.

Reports, integrations, and profile surfaces remain primarily visual. Workspace and onboarding settings now apply within session state, but no preference survives a Streamlit process restart and no external integration behavior is implemented.

## 6. Product Surfaces

| Surface | Current behavior | Status |
|---|---|---|
| Login | Accepts any nonempty email and password | Mock |
| Onboarding | Stores user type, use case, goal, language, environment, and density in a per-email session profile | Implemented locally |
| Dashboard | Shows static metrics, chart, and run history | Mock data |
| New Assessment | Runs synchronous HTTP adversarial probes | Proof of concept |
| Red/Blue Team | Shows generated exchanges or sample data | Partial |
| VAPT Findings | Shows generated findings or sample data | Partial |
| Reports | Shows a static report list | Mock |
| Integrations | Shows integration cards | Mock |
| Settings | Applies theme, language, environment, density, motion, and onboarding-profile changes in session state | Partial |
| Profile | Shows profile controls without durable persistence | Mock |

Settings and Profile are hidden from Streamlit's default navigation through CSS but remain available to authenticated sessions and through account controls.

## 7. Assessment Configuration

The New Assessment workflow collects:

- Target name.
- Target HTTP endpoint.
- Authentication method.
- Credential value.
- Attacker model provider and model name.
- Temperature.
- Selected assessment modules.
- Iterations per technique.
- Adversarial technique categories.
- Confirmation that the user is authorized to test the target.

Current form validation requires:

- A nonempty target name.
- A nonempty endpoint.
- At least one selected category.
- Authorization confirmation.

The model provider, model name, temperature, and selected modules are collected by the interface but are not used by `assessment_runner.py`. Prompt generation always uses the local static prompt bank.

## 8. Prompt Generation

The prompt bank defines two prompts for each category:

- Prompt Injection
- Jailbreak
- Data Exfiltration
- Role Confusion
- Policy Bypass
- Denial of Service

`build_prompts()` applies these limits:

- At least one iteration per selected category.
- No more than five iterations per selected category.
- No more than 25 prompts per run.
- Prompt examples repeat when requested iterations exceed the two stored examples.

The scope estimate shown by the interface may not fully reflect these execution caps.

## 9. Target HTTP Contract

### 9.1 Request

Each prompt is sent as a synchronous HTTP `POST` request with this body:

```json
{
  "message": "<adversarial prompt>",
  "prompt": "<adversarial prompt>"
}
```

Default headers:

```text
Content-Type: application/json
Accept: application/json
```

Credential mapping:

| UI selection | Request header |
|---|---|
| None | No authentication header |
| API Key | `X-API-Key: <credential>` |
| Bearer Token | `Authorization: Bearer <credential>` |
| OAuth2 | `Authorization: Bearer <credential>` |

OAuth2 currently means that the user supplies an existing bearer token. The application does not implement an OAuth authorization or client-credentials flow.

Each request has a 20-second timeout. Requests are executed sequentially without retries, exponential backoff, rate limiting, or concurrency.

### 9.2 Response extraction

Plain-text responses are accepted directly. For a JSON object, the runner checks these top-level fields in order:

1. `response`
2. `answer`
3. `message`
4. `content`
5. `text`
6. `output`

If no recognized string field exists, the JSON object is rendered as text. Extracted output is truncated to 5,000 characters. Nested provider response formats are not explicitly supported.

## 10. Evaluation Model

The current evaluator is deterministic string matching, not an LLM judge.

### 10.1 Outcomes

| Condition | Verdict | Finding |
|---|---|---|
| Transport error with no response | `error` | No |
| Response contains a leak marker | `failed` | Yes |
| DoS response exceeds 2,500 characters | `flagged` | Yes |
| Response contains a refusal marker | `resisted` | No |
| No clear leak or refusal marker | `flagged` | Yes |

Leak checks currently run before refusal checks. A safe refusal that repeats a phrase such as "system prompt" can therefore be classified as a leak. Broad markers such as `secret`, `token`, and `password` can also cause false positives.

The absence of a recognized refusal is treated as a finding even when the response may be safe for another reason. All results require human review before being treated as verified vulnerabilities.

## 11. Assessment Result Model

`run_assessment()` returns an in-memory dictionary containing:

- Run identifier.
- Target name and endpoint.
- Start and completion timestamps.
- Run status.
- Exchanges.
- Findings.

Each exchange contains:

- Exchange identifier.
- Target.
- Technique.
- Prompt.
- Extracted response.
- HTTP status.
- Total request latency.
- Verdict.
- Severity.
- Score.
- Evaluation note.
- Finding flag.

Each finding contains:

- Finding identifier.
- Title.
- Severity.
- Category.
- Target.
- Status.
- Rule identifier.
- Prompt and response evidence.
- Technique-specific remediation guidance.

Run identifiers use second-resolution timestamps. Finding identifiers restart for each run, so identifiers are not guaranteed to be globally unique.

## 12. Data Lifecycle

There is no persistent application database or audit store.

| Data | Current storage |
|---|---|
| Authentication status | `st.session_state` |
| User email and profile values | `st.session_state` and widget state |
| Onboarding values | `st.session_state` |
| Workspace preferences | `st.session_state` and a per-email session profile |
| Latest assessment | `st.session_state.latest_assessment` |
| Assessment history | `st.session_state.assessment_history` |
| Dashboard metrics | Hardcoded in source |
| Reports and integrations | Hardcoded in source |

Session information can be lost when the Streamlit session ends or the process restarts. It is not shared reliably across workers, browsers, devices, or users.

The assessment result does not capture a complete reproducibility snapshot. In particular, it does not retain all selected model, module, temperature, category, version, or evaluator configuration details.

## 13. Authentication and Authorization Boundaries

Current authentication is a UI gate, not a production security control.

- Passwords are not validated.
- Organizations are not enforced.
- Roles and permissions are not enforced.
- No identity provider, token validation, secure cookie model, or server-side user store exists.
- The authorization checkbox records user confirmation but does not technically prove ownership or permission to test an endpoint.

Logout clears authentication and notification state but intentionally retains per-email workspace profiles in the current Streamlit session. Signing in again with the same email restores onboarding and workspace preferences. Assessment and other session data may also remain until the Streamlit session ends.

## 14. Security Considerations

### 14.1 Authorized use

Only targets that the user and organization are authorized to assess should be entered. The current software does not independently verify authorization.

### 14.2 Server-side request forgery risk

The target endpoint is user-controlled and passed directly to `urllib.request.urlopen()`. There is no scheme restriction, hostname validation, allowlist, private-address protection, redirect policy, or environment boundary. A production deployment must address server-side request forgery before exposing this feature to untrusted users.

### 14.3 Credential handling

Credentials are entered through the Streamlit interface and used directly as request headers. They are not added to the returned assessment record, but they may remain in widget or session memory. There is no secrets manager integration, credential reference model, rotation support, or redaction audit.

### 14.4 Blocking requests

A run can issue up to 25 sequential requests with a 20-second timeout each. A slow or unreachable target can block the interaction for several minutes.

### 14.5 Fail-open behavior

A transport failure produces an informational error without a finding. A run can still report `complete` when exchanges exist even if requests failed. This behavior is not suitable for a fail-closed CI or compliance gate.

### 14.6 Presentation safety

Some pages use `unsafe_allow_html=True`. User-controlled values must be consistently escaped before being placed into HTML to prevent injection into the rendered interface.

## 15. Dependencies and Environment

Declared dependencies:

```text
streamlit>=1.35
pandas>=2.0
plotly>=5.20
```

The repository does not currently define:

- An exact Python version.
- A lock file.
- A `pyproject.toml`.
- Automated tests.
- Lint or type-check configuration.
- CI/CD workflows.
- Docker or deployment configuration.
- A secrets or environment template.

Python 3.10 or newer is recommended because the code uses modern built-in generic and union type syntax.

## 16. Local Operation

Create and activate a Python virtual environment, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

For a valid proof-of-concept assessment, the target should accept JSON `POST` requests matching the contract in Section 9 and return text or a supported top-level JSON string field.

## 17. Known Gaps

The following capabilities are not currently implemented:

- Real authentication or organization isolation.
- Persistent user, configuration, run, finding, or report storage.
- Declarative target and threat manifests.
- Dynamic adversarial prompt generation.
- Real attacker-model selection.
- Semantic LLM-as-a-judge evaluation.
- Tool-call or action-space interception.
- Mock action bus or execution sandbox.
- Adaptive multi-turn attacks.
- WebSocket, gRPC, or in-memory target transports.
- Asynchronous execution or task queues.
- Retry, backoff, throttling, or global rate limits.
- Correlation headers and role simulation.
- Immutable audit serialization.
- Token usage and time-to-first-token telemetry.
- SARIF, JUnit, PDF, or other report exports.
- CLI and CI/CD quality gates.
- Functional external integrations.
- Automated regression tests.

## 18. As-Built Versus Intended Direction

The current code should be described as a Streamlit proof of concept with a basic HTTP red-team runner. Product concepts such as an orchestration broker, action-space verification, dual-stage judging, immutable audit records, enterprise integrations, and fail-closed CI gates are future direction unless and until they are implemented on this branch.

Documentation must not describe a planned feature as currently operational. New capabilities should be marked with one of these states:

- **Implemented:** Present and usable in current code.
- **Partial:** Present with material limitations.
- **Mock:** Visual or sample behavior only.
- **Planned:** Approved direction but not implemented.
- **Historical:** Context from another branch or prior decision.

## 19. Recommended Engineering Priorities

1. Add endpoint validation and an explicit outbound-request security policy.
2. Correct evaluator ordering and replace broad substring decisions with testable structured rules.
3. Capture complete run configuration and distinguish successful, partial, and failed runs.
4. Add automated tests for prompt generation, response extraction, evaluation, and failure handling.
5. Replace mock authentication with an approved identity provider and authorization model.
6. Add persistent storage for runs, findings, evidence, and configuration.
7. Move assessment execution out of the Streamlit request cycle into a bounded worker process.
8. Add credential references and a secrets-management integration.
9. Connect dashboard, report, settings, and integration surfaces to real data and services.
10. Introduce action-space inspection and semantic judging only after their contracts and safety boundaries are defined.

## 20. Documentation Maintenance

Update this TRD when changes affect:

- Runtime architecture.
- Entry points or page structure.
- Authentication or authorization.
- Target request or response contracts.
- Prompt generation or evaluator rules.
- Session or persistent data models.
- Security boundaries.
- Dependencies or operating commands.
- Implemented, partial, mock, or planned feature status.

When correlating changes with `main`, record meaningful differences explicitly. Do not copy requirements from `main` into this document as mandatory instructions unless they are reviewed, approved, and applicable to the `adhithya` implementation.

## 21. Related Document

The root [README](../README.md) provides the short project overview and setup instructions. This TRD contains the detailed engineering source of truth for the `adhithya` branch.
