import streamlit as st

def show_analysis(
    llm,
    save_report,
    update_analysis,
    update_diet,
    render_cards,
    serialize_blood_analysis,
    BloodAnalysis,
    build_rag_chain,
    extract_answer,
    save_message,
):

    st.markdown("""
    <div class="stage-row">
        <div class="stage-num">1</div>
        <div class="stage-lbl">Paste Report &amp; Analyze</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")
        
    with left:
        default_text = st.session_state.get("report_text", "")
        blood_report = st.text_area(
            label="report",
            value=default_text,
            placeholder="Paste your blood report here...\n\nHemoglobin: 10.2 g/dL  (Ref: 13.5–17.5)\nWBC: 11,000 /µL  (Ref: 4,500–11,000)\n...",
            height=380,
            label_visibility="collapsed"
        )
        analyze_clicked = st.button("🔬  Analyze Report", use_container_width=True)

        if analyze_clicked:
            if not blood_report.strip():
                st.warning("Paste a blood report first.")
            else:
                with st.spinner("Reading and classifying values..."):
                    prompt_text = f"""You are a medical data extraction assistant.

    Extract EVERY test from the blood report. For each test output EXACTLY this format — one per line:
    TEST: <name> | VALUE: <result> | STATUS: <HIGH/LOW/NORMAL> | REF: <reference range>

    Rules:
    - STATUS must be exactly HIGH, LOW, or NORMAL only
    - No intro, no summary, no blank lines
    - Include every single test

    Blood Report:
    {blood_report}"""
                    structured_llm = llm.with_structured_output(BloodAnalysis)

                    analysis = structured_llm.invoke(prompt_text)
                    raw = serialize_blood_analysis(analysis)

                    st.session_state["analysis_summary"] = getattr(analysis, "patient_summary", None)
                    st.session_state["health_score"] = getattr(analysis, "health_score", None)
                    st.session_state["risk_level"] = getattr(analysis, "risk_level", None)
                    st.session_state["extracted_values"] = raw
                    st.session_state["report_text"]      = blood_report

                    # Save or update in database
                    if not st.session_state.get("report_id"):
                        rid = save_report(
                        report_text=blood_report,
                        user_id=st.session_state.user.id
                        )
                        st.session_state["report_id"] = rid
                    else:
                        rid = st.session_state["report_id"]

                    update_analysis(rid, raw)
                    st.rerun()





    with right:
        if not st.session_state.get("extracted_values"):
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📊</div>
                <div class="empty-title">Test results appear here</div>
                <div class="empty-sub">Paste a report on the left<br>and click Analyze</div>
            </div>
            """, unsafe_allow_html=True)

            
        if st.session_state.get("extracted_values"):
            cards_html, count = render_cards(st.session_state["extracted_values"])
            if count > 0:
                st.markdown(cards_html, unsafe_allow_html=True)
            else:
                st.info("Could not parse structured results. Check the report format.")


    # ── STAGE 2 ───────────────────────────────────────────────────────────────
    if st.session_state.get("extracted_values"):
        st.markdown('<hr class="sdiv"/>', unsafe_allow_html=True)
        st.markdown("""
        <div class="stage-row">
            <div class="stage-num">2</div>
            <div class="stage-lbl">Indian Diet Plan</div>
        </div>
        """, unsafe_allow_html=True)

        # Show saved diet plan if loaded from history
        if st.session_state.get("diet_plan"):
            st.markdown(
                f'<div class="diet-box">{st.session_state["diet_plan"].replace(chr(10), "<br>")}</div>',
                unsafe_allow_html=True
            )
            if st.button("🔄  Regenerate Diet Plan", use_container_width=False):
                st.session_state.pop("diet_plan", None)
                st.rerun()
        else:
            if st.button("🥗  Generate Diet Plan", use_container_width=False):
                with st.spinner("Building your personalized diet plan..."):
                    diet_prompt = f"""You are a clinical nutritionist specializing in Indian dietary habits.

    From the blood work below, identify ONLY the abnormal values (HIGH or LOW).
    Respond in exactly this structure:

    **Health Summary**
    3-4 sentences in simple language about what the key abnormal results mean for this patient's health. Speak like a caring doctor.

    **Foods to Avoid**
    - List 4-5 specific Indian foods that directly worsen the abnormal values. One per line.

    **Foods to Eat More**
    - List 4-5 specific Indian foods that directly help correct the abnormal values. One per line.

    Focus only on abnormal values. Be concise.

    Blood Work:
    {st.session_state["extracted_values"]}"""
                    diet_resp = llm.invoke(diet_prompt)
                    diet_text = diet_resp.content
                    if isinstance(diet_text, list):
                        diet_text = "\n".join([r if isinstance(r, str) else r.get("text","") for r in diet_text])

                    st.session_state["diet_plan"] = diet_text
                    update_diet(st.session_state["report_id"], diet_text)

                st.markdown(
                    f'<div class="diet-box">{diet_text.replace(chr(10), "<br>")}</div>',
                    unsafe_allow_html=True
                )

    # ── STAGE 3 ───────────────────────────────────────────────────────────────
    if st.session_state.get("report_text"):
        st.markdown('<hr class="sdiv"/>', unsafe_allow_html=True)
        st.markdown("""
        <div class="stage-row">
            <div class="stage-num">3</div>
            <div class="stage-lbl">Health Assistant Chat</div>
        </div>
        """, unsafe_allow_html=True)

        # Build RAG chain if not already built
        if "rag_chain" not in st.session_state:
            with st.spinner("Initialising health assistant..."):
                combined = f"""BLOOD REPORT:
    {st.session_state["report_text"]}

    ANALYSIS:
    {st.session_state.get("extracted_values", "")}"""
                st.session_state["rag_chain"] = build_rag_chain(combined)
            st.success("✅ Assistant ready — ask anything about your health or your report.")

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        # Render existing chat
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Suggested questions when chat is empty
        if not st.session_state["chat_history"]:
            st.markdown("""
            <div style="margin:0.5rem 0 1rem 0;">
                <div style="font-size:0.72rem;color:#444;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.5rem;">Try asking</div>
            </div>
            """, unsafe_allow_html=True)
            suggestions = [
                "What does it mean if my hemoglobin is low?",
                "Which of my values are most concerning?",
                "What is the difference between HDL and LDL cholesterol?",
                "What lifestyle changes can help improve my results?"
            ]
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                        st.session_state["chat_history"].append({"role": "user", "content": suggestion})
                        save_message(st.session_state["report_id"], "user", suggestion)
                        with st.spinner("Thinking..."):
                            result = st.session_state["rag_chain"].invoke(
                                {"input": suggestion},
                                config={"configurable": {"session_id": f"session_{st.session_state['report_id']}"}}
                            )
                            answer = extract_answer(result)
                        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
                        save_message(st.session_state["report_id"], "assistant", answer)
                        st.rerun()

        user_question = st.chat_input("Ask about your report or any health topic...")

        if user_question:
            st.session_state["chat_history"].append({"role": "user", "content": user_question})
            save_message(st.session_state["report_id"], "user", user_question)

            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = st.session_state["rag_chain"].invoke(
                        {"input": user_question},
                        config={"configurable": {"session_id": f"session_{st.session_state['report_id']}"}}
                    )
                    answer = extract_answer(result)
                st.markdown(answer)
                save_message(st.session_state["report_id"], "assistant", answer)
                st.session_state["chat_history"].append({"role": "assistant", "content": answer})