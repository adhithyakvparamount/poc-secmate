"""
authcheck.py — shared auth guard for every dashboard page.

Import and call require_auth() as the FIRST line of logic in app.py's
dashboard branch and in every file under pages/. If the user has not
signed in (st.session_state.authenticated is not True), it sends them
back to the login screen at app.py.
"""

import streamlit as st


def require_auth():
    if not st.session_state.get("authenticated", False):
        st.switch_page("app.py")
        st.stop()
    if not st.session_state.get("onboarding_seen", False):
        st.switch_page("app.py")
        st.stop()
