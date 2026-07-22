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
        if st.button("🎙 Voice Assistant", use_container_width=True):
            st.info("Voice Assistant will be added soon.")

    with col3:
        if st.button("💬 Health Chat", use_container_width=True):
            st.session_state.current_page = "analysis"
            st.rerun()

    with col4:
        if st.button("📜 Report History", use_container_width=True):
            st.info("History page coming soon.")