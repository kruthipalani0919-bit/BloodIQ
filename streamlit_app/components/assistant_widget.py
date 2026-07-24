import streamlit as st


def show_assistant_widget(llm):

    # Track whether the assistant is open
    if "assistant_open" not in st.session_state:
        st.session_state.assistant_open = False

    # Store conversation history
    if "assistant_messages" not in st.session_state:
        st.session_state.assistant_messages = [
            {
                "role": "assistant",
                "content": (
                    "👋 Hi! I'm your BloodIQ Assistant.\n\n"
                    "Ask me anything about health or BloodIQ."
                ),
            }
        ]

    # Floating button
    if not st.session_state.assistant_open:

        if st.button("💬", key="floating_chat"):
            st.session_state.assistant_open = True
            st.rerun()

        return

    # Assistant Window
    with st.container(border=True):

        st.subheader("🤖 BloodIQ Assistant")

        # Show previous messages
        for message in st.session_state.assistant_messages:
                with st.chat_message(
                    message["role"],
                    avatar="🤖" if message["role"] == "assistant" else "👤",
                ):
                 st.write(message["content"])

        # User input
        prompt = st.chat_input("Ask me anything...")

        if prompt:

            # Show user message
            st.session_state.assistant_messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

            try:

                system_prompt = """
You are BloodIQ Assistant.

You answer:

1. General health questions.

2. Questions about using the BloodIQ application.

Examples:
- How do I upload a report?
- Where is My Reports?
- What does Analyze Report do?
- What is BloodIQ?

Never diagnose diseases.

If the user asks medical questions, provide educational information only and recommend consulting a doctor when appropriate.

Be friendly.

Keep answers short.
"""

                full_prompt = f"""
{system_prompt}

User Question:
{prompt}
"""

                response = llm.invoke(full_prompt)

                print("========== DEBUG ==========")
                print(type(response))
                print(response)
                print("===========================")

                answer = response.content

                if isinstance(answer, list):
                    answer = "\n".join(
                        [
                            item if isinstance(item, str)
                            else item.get("text", "")
                            for item in answer
                        ]
                    )

            except Exception as e:

                answer = f"❌ Error: {str(e)}"

            # Save assistant reply
            st.session_state.assistant_messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            st.rerun()

        if st.button("❌ Close"):
            st.session_state.assistant_open = False
            st.rerun()