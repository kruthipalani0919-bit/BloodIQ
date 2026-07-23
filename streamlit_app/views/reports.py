import streamlit as st
from database import (
    get_all_reports,
    get_report_by_id,
    get_chat_history,
)

def show_reports():

    st.title("📂 My Reports")
    st.write("View all your previous blood reports.")

    user_id = (
        st.session_state.user.id
        if st.session_state.get("user")
        else None
    )

    reports = get_all_reports(user_id)

    if not reports:
        st.info("No reports found.")
        return

    for report in reports:

        with st.container(border=True):

            st.write(f"**Date:** {report['created_at']}")
            st.write(report["preview"])

            col1, col2 = st.columns(2)

            with col1:
                if st.button("📄 Open", key=f"open_{report['id']}"):

                   user_id = st.session_state.user.id

                   data = get_report_by_id(report["id"], user_id)

                   st.session_state.report_id = data["id"]
                   st.session_state.report_text = data["report_text"]
                   st.session_state.extracted_values = data["extracted_values"]
                   st.session_state.diet_plan = data["diet_plan"]

                   st.session_state.chat_history = get_chat_history(
                        data["id"],
                        user_id,
                    )

                   st.session_state.current_page = "analysis"

                   st.rerun()
            with col2:
                st.button("🗑 Delete", key=f"delete_{report['id']}")