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

        if st.button("＋ New Analysis", use_container_width=True):
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

        st.markdown(
                   '<div class="sb-section-label">Report History</div>',
                  unsafe_allow_html=True,
            )

      
        user_id = (
            st.session_state.user.id
            if st.session_state.get("user")
            else None
        )
        all_reports = get_all_reports(user_id)


        if not all_reports:

            st.markdown("""
            <div style="padding:0.8rem 1.2rem;">
                <div style="font-size:0.75rem;color:#333;">
                    No reports yet.<br>
                    Run your first analysis above.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:

            for r in all_reports:

                is_active = (
                    st.session_state.get("report_id") == r["id"]
                )

                badges = ""

                if r["has_analysis"]:
                    badges += '<span class="hc-badge analysis">Analyzed</span>'

                if r["has_diet"]:
                    badges += '<span class="hc-badge diet">Diet Plan</span>'

                st.markdown(f"""
                <div class="history-card {'active' if is_active else ''}">
                    <div class="hc-date">{r["created_at"]}</div>
                    <div class="hc-preview">{r["preview"]}</div>
                    <div class="hc-badges">{badges}</div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([3, 1])

                with col1:

                    if st.button(
                        "Load",
                        key=f"load_{r['id']}",
                        use_container_width=True,
                    ):

                        data = get_report_by_id(
                            r["id"],
                            user_id,
                        )

                        st.session_state["report_id"] = data["id"]
                        st.session_state["report_text"] = data["report_text"]
                        st.session_state["extracted_values"] = data["extracted_values"]
                        st.session_state["diet_plan"] = data["diet_plan"]

                        st.session_state["chat_history"] = get_chat_history(
                            data["id"],
                            user_id,
                        )

                        st.session_state.pop("rag_chain", None)

                        st.rerun()

                with col2:

                    if st.button(
                        "🗑",
                        key=f"del_{r['id']}",
                        use_container_width=True,
                    ):

                        delete_report(
                            r["id"],
                            user_id,
                        )

                        if st.session_state.get("report_id") == r["id"]:

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



                        st.divider()

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
    ]:
        st.session_state.pop(key, None)

    st.rerun()