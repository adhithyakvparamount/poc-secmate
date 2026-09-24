# SecMate — Frontend Redesign (Visual Mockup)

This is a **frontend-only** redesign of the SecMate Streamlit interface.
It implements the dark navy cybersecurity SaaS look, page layout, and
navigation structure discussed in the design concept. It does **not**
implement or replace any backend logic (Red Team generation, Blue Team
evaluation, or VAPT rule analysis).

## What's real vs. mock

Every page currently renders with **placeholder sample data** so you can
see the full UI working end-to-end. Anywhere data is mocked, the file has
a `MOCK DATA — replace with backend calls` section and a docstring note
at the top of the file. Buttons like "Launch Assessment," "Generate New
Report," and "Save Settings" show a visual confirmation only — they do
not call any real logic yet.

## Structure

```
secmate_ui/
├── app.py                       # SINGLE ENTRY POINT — login gate + Dashboard
├── login_screen.py              # Sign-in UI, rendered by app.py when not logged in
├── authcheck.py                 # require_auth() — imported by every page in pages/
├── theme.py                     # Colors, CSS, and reusable UI components (dashboard pages)
├── requirements.txt
└── pages/
    ├── 1_New_Assessment.py      # Target / model / test suite configuration
    ├── 2_Red_Blue_Team.py       # Red Team + Blue Team results (tabbed)
    ├── 3_VAPT_Findings.py       # Findings list with severity filters
    ├── 4_Reports.py             # Report list + generate/download
    └── 5_Settings.py            # Default target/model/test-suite settings
```

There is now **one way to run the app**: `streamlit run app.py`. It checks
`st.session_state.authenticated` — if you're not signed in, it renders
`login_screen.py` (no sidebar) and stops. Once you sign in, it sets
`authenticated = True`, reruns, and shows the Dashboard with the sidebar
nav. Every file under `pages/` calls `authcheck.require_auth()` as its
first line, so navigating to any page directly while signed out bounces
you back to the login screen. A "Log out" button in the sidebar (on
every page) resets the session and returns you to login.

`login_screen.py` uses a **blue** accent (`#2F6FED`) matching the
reference design, while the dashboard pages use a **teal** accent
(`#00D9A3`) from `theme.py`. Unify these in `theme.py` if you want one
consistent accent product-wide.

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Sign-in is still a mock** — `login_screen.py`'s `_attempt_sign_in()`
only checks that email and password are non-empty; it doesn't verify
credentials against anything real yet. Replace that function's body
with a call to your actual auth backend when you have one.

## Wiring in your real backend

1. **Dashboard (`app.py`)** — replace `get_summary_metrics()`,
   `get_risk_distribution()`, and `get_recent_runs()` with reads from
   your assessment history store.
2. **New Assessment (`pages/1_New_Assessment.py`)** — replace the
   `st.success(...)` on launch with a call to your existing run-trigger
   function, passing the form values already collected.
3. **Red/Blue Team (`pages/2_Red_Blue_Team.py`)** — replace
   `get_red_team_exchanges()` / `get_blue_team_evaluations()` with the
   actual prompt/response/evaluation records for the selected run.
4. **VAPT Findings (`pages/3_VAPT_Findings.py`)** — replace
   `get_findings()` with your VAPT module's output; the `severity` field
   must be one of `critical / high / medium / low / info` to match the
   color system in `theme.py`.
5. **Reports (`pages/4_Reports.py`)** — replace `get_reports()` with your
   report store, and wire the `Download` buttons to serve the actual
   files (e.g. `st.download_button` with the file bytes).
6. **Settings (`pages/5_Settings.py`)** — replace the `st.success(...)`
   on save with a call to your configuration persistence layer, and
   pre-fill each widget's `value=` from the currently stored config.

## Design tokens

All colors, fonts, badge styles, and card styles live in `theme.py`
(`COLORS` dict + `apply_theme()`). Change a value there and it updates
everywhere — no page file hardcodes a color.
