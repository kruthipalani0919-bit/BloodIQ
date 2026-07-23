import streamlit as st

from database import (
    get_all_reports,
    get_report_by_id,
    get_chat_history,
    delete_report,
)


def show_sidebar():

    with st.sidebar:

        st.markdown("""
        <div class="sb-logo">
            <div class="sb-logo-title">🩸 Blood<span class="sb-logo-dot">IQ</span></div>
            <div class="sb-logo-sub">AI-powered blood work analysis</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sb-section-label">Actions</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-new-btn">', unsafe_allow_html=True)

        if st.button("➕ New Analysis", use_container_width=True):

               st.session_state.current_page = "analysis"

               for key in [
                "report_id",
                "report_text",
                "extracted_values",
                "diet_plan",
                "rag_chain",
                "chat_history",
                ]:
                st.session_state.pop(key, None)

                st.rerun()

        if st.button("🏠 Dashboard", use_container_width=True):
           st.session_state.current_page = "dashboard"
           st.rerun()

        if st.button("📂 My Reports", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


            # ---------------- Logout ----------------
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.token = None

            for key in [
                "report_id",
                "report_text",
                "extracted_values",
                "diet_plan",
                "chat_history",
                "rag_chain",
                "analysis_summary",
                "health_score",
                "risk_level",
            ]:
               st.session_state.pop(key, None)

            st.rerun()
