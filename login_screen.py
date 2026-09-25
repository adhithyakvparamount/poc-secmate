"""
login_screen.py — SecMate sign-in screen, as a reusable function.

VISUAL MOCKUP NOTICE:
render_login_screen() checks only that email + password are non-empty —
there is no real authentication yet. Replace the check inside
`_attempt_sign_in()` with a call to your real auth backend (verify
credentials, look up the organization, etc.) before setting
st.session_state.authenticated = True.

NOTE ON COLOR: this screen and the default dashboard use the SecMate
enterprise-blue visual system defined in theme.py.
"""

import streamlit as st

from theme import shield_logo_svg
from workspace import initialize_workspace_state, load_workspace_profile

BLUE = "#2F6FED"
BLUE_LIGHT = "#4C8DFF"
CANVAS = "#070E1F"
CANVAS_2 = "#0B1730"
CARD_BG = "#0E1B36"
BORDER = "#1E2E4F"
TEXT_PRIMARY = "#F1F5FB"
TEXT_SECONDARY = "#9AA7C2"
GREEN = "#22C55E"


def _inject_login_css():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

        /* Hide sidebar entirely — this is a pre-login screen */
        section[data-testid="stSidebar"] {{ display: none; }}
        #MainMenu {{ visibility: hidden; }}
        footer {{ visibility: hidden; }}
        header[data-testid="stHeader"] {{ background: transparent; }}

        .stApp {{
            background: radial-gradient(1200px 600px at 20% 0%, {CANVAS_2} 0%, {CANVAS} 55%);
        }}

        .block-container {{
            padding-top: 2.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}

        .topbar {{
            display: flex; align-items: center; justify-content: space-between;
            margin-bottom: 60px;
        }}
        .brand {{ display: flex; align-items: center; gap: 12px; }}
        .brand svg {{ filter: drop-shadow(0 0 18px rgba(45,158,255,.3)); }}
        .brand-name {{ font-size: 22px; font-weight: 700; color: {TEXT_PRIMARY}; line-height: 1.1; }}
        .brand-tag {{ font-size: 12.5px; color: {TEXT_SECONDARY}; }}
        .env-pill {{
            display: inline-flex; align-items: center; gap: 6px;
            background: rgba(34,197,94,0.12); border: 1px solid rgba(34,197,94,0.3);
            color: {GREEN}; font-size: 12.5px; font-weight: 600;
            padding: 5px 12px; border-radius: 16px; margin-right: 10px;
        }}
        .env-pill .dot {{ width: 6px; height: 6px; border-radius: 50%; background: {GREEN}; }}
        .gateway-link {{ color: {TEXT_SECONDARY}; font-size: 13px; }}

        .hero {{ padding-top: 90px; max-width: 640px; }}
        .hero h1 {{
            font-size: 44px; font-weight: 800; line-height: 1.2;
            color: {TEXT_PRIMARY}; margin: 0;
        }}
        .hero h1 .accent {{ color: {BLUE_LIGHT}; }}
        .hero p {{
            font-size: 16px; color: {TEXT_SECONDARY}; line-height: 1.6;
            margin-top: 22px; max-width: 480px;
        }}

        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"] {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 32px 34px 26px 34px;
        }}
        .login-title {{ font-size: 22px; font-weight: 700; color: {TEXT_PRIMARY}; }}
        .login-sub {{ font-size: 13.5px; color: {TEXT_SECONDARY}; margin-top: 4px; margin-bottom: 22px; }}
        .help-link {{ font-size: 12.5px; color: {TEXT_SECONDARY}; text-align: right; }}
        .help-link a {{ color: {BLUE_LIGHT}; text-decoration: none; }}

        div[data-testid="stColumn"]:nth-child(2) div[data-testid="stTextInput"] input,
        div[data-testid="stColumn"]:nth-child(2) div[data-baseweb="select"] > div {{
            background-color: #0A1530 !important;
            border: 1px solid {BORDER} !important;
            border-radius: 8px !important;
            color: {TEXT_PRIMARY} !important;
        }}
        div[data-testid="stColumn"]:nth-child(2) label {{
            color: {TEXT_PRIMARY} !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
        }}
        div[data-testid="stColumn"]:nth-child(2) .stButton > button {{
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            padding: 10px 0;
        }}
        .st-key-sign_in button {{
            background-color: {BLUE} !important;
            color: white !important;
            border: none !important;
        }}
        .st-key-sign_in button:hover {{ background-color: {BLUE_LIGHT} !important; }}
        .st-key-sso button {{
            background-color: transparent !important;
            color: {TEXT_PRIMARY} !important;
            border: 1px solid {BLUE} !important;
        }}
        .st-key-sso button:hover {{ background-color: rgba(47,111,237,0.08) !important; }}

        .divider-row {{ display:flex; align-items:center; gap:12px; margin: 14px 0; }}
        .divider-row hr {{ flex:1; border: none; border-top: 1px solid {BORDER}; margin:0; }}
        .divider-row span {{ color: {TEXT_SECONDARY}; font-size: 12.5px; }}

        .forgot-row {{ text-align: right; margin-top: -8px; margin-bottom: 14px; }}
        .forgot-row a {{ color: {BLUE_LIGHT}; font-size: 12.5px; text-decoration: none; }}

        .signup-row {{ text-align: center; font-size: 13px; color: {TEXT_SECONDARY}; margin-top: 18px; }}
        .signup-row a {{ color: {BLUE_LIGHT}; text-decoration: none; }}

        @media (max-width: 900px) {{
            .topbar {{ margin-bottom: 12px; }}
            .hero {{ padding: 38px 0 22px; }}
            .hero h1 {{ font-size: 38px; }}
            div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2) > div[data-testid="stVerticalBlock"] {{ padding: 26px 22px; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_login_screen():
    """
    Renders the full sign-in screen. On successful (mock) sign-in, sets
    st.session_state.authenticated = True and reruns the app so app.py's
    gate lets the dashboard render instead.
    """
    _inject_login_css()

    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand">
                {shield_logo_svg(46)}
                <div>
                    <div class="brand-name">SecMate</div>
                    <div class="brand-tag">Secure AI. Trust What Runs.</div>
                </div>
            </div>
            <div>
                <span class="env-pill"><span class="dot"></span>Production</span>
                <span class="gateway-link">Enterprise Gateway</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_hero, col_card = st.columns([1.35, 1], gap="large")

    with col_hero:
        st.markdown(
            f"""
            <div class="hero">
                <h1>Adversarial testing for<br><span class="accent">AI agents, built for enterprise.</span></h1>
                <p>SecMate helps you identify vulnerabilities, validate guardrails, and ensure
                policy compliance before you deploy AI agents in production.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_card:
        st.markdown(
            """
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="login-title">Welcome back</div>
                    <div class="login-sub">Sign in to your SecMate account</div>
                </div>
                <div class="help-link">Need help?<br><a href="#">Contact support</a></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.selectbox("Organization", ["Paramount Computer Systems", "Acme Corp", "Northwind Security"], key="login_org")
        email = st.text_input("Work email", placeholder="you@company.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")

        st.markdown('<div class="forgot-row"><a href="#">Forgot password?</a></div>', unsafe_allow_html=True)

        if st.button("Sign In", key="sign_in"):
            _attempt_sign_in(email, password)

        st.markdown('<div class="divider-row"><hr><span>or</span><hr></div>', unsafe_allow_html=True)

        if st.button("🏢  Sign in with SSO", key="sso"):
            st.info("SSO flow not connected yet. (Visual confirmation only.)")
        st.markdown(
            f'<div style="text-align:center; font-size:11.5px; color:{TEXT_SECONDARY}; margin-top:-6px;">'
            "Recommended for enterprise organizations</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="signup-row">New to SecMate? <a href="#">Contact your administrator</a></div>',
            unsafe_allow_html=True,
        )



def _attempt_sign_in(email: str, password: str):
    """
    MOCK AUTH: only checks that both fields are filled in.
    Replace this body with a real credential check against your backend.
    """
    if not email or not password:
        st.error("Enter your work email and password.")
        return
    initialize_workspace_state()
    st.session_state.authenticated = True
    st.session_state.user_email = email
    st.session_state.onboarding_seen = load_workspace_profile(email)
    if not st.session_state.onboarding_seen:
        st.session_state.language_pref = "English"
        st.session_state.workspace_environment = "Staging"
        st.session_state.dashboard_density = "Comfortable"
        st.session_state.dashboard_theme = "SecMate Dark"
        st.session_state.reduced_motion = False
        st.session_state.onboarding_user_type = "Security Analyst"
        st.session_state.onboarding_use_case = "Testing an internal AI agent"
        st.session_state.onboarding_goal = ""
    st.session_state.sync_sidebar_preferences = True
    st.session_state.onboarding_loading = not st.session_state.onboarding_seen
    st.rerun()
