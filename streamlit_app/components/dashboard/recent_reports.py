import streamlit as st


def show_recent_reports():
    """
    Dashboard recent reports section.
    """

    st.subheader("📄 Recent Reports")

    reports = [
        "Blood Report - July 13",
        "Blood Report - July 10",
        "Blood Report - July 05",
    ]

    for report in reports:
        st.markdown(
            f"""
            <div style="
                padding:15px;
                margin-bottom:10px;
                border-radius:12px;
                background:#181818;
                border:1px solid #303030;
            ">
                📄 {report}
            </div>
            """,
            unsafe_allow_html=True,
        )