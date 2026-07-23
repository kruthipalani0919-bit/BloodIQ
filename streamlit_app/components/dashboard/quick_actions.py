import streamlit as st


def show_quick_actions():
    """
    Dashboard quick action buttons.
    """

    st.subheader("⚡ Quick Actions")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if st.button("🩸 Analyze Report", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()

    with col2:
        if st.button("🤖 AI Health Assistant", use_container_width=True):
            st.info("AI Health Assistant will be added soon.")

   