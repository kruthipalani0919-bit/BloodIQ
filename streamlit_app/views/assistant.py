import streamlit as st

def show_assistant():

    st.title("🤖 AI Health Assistant")

    st.markdown("""
Ask anything related to:

- 🩸 Blood Reports
- 🥗 Diet Plans
- 💊 Medical Terms
- ❤️ Health
- 🏃 Lifestyle

Your assistant remembers your report context.
""")

    question = st.chat_input("Ask me anything...")

    if question:
        st.chat_message("user").write(question)

        st.chat_message("assistant").write(
            "🚧 AI Assistant will be connected in the next step."
        )