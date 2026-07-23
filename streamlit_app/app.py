import traceback

try:
    import streamlit as st

    from rag.rag import build_rag_chain
    from database import (
    init_db,
    save_report,
    update_analysis,
    update_diet,
    save_message,
    get_chat_history,
    get_all_reports,
    get_report_by_id,
    get_dashboard_stats,
    delete_report,
)

    from database.connection import get_session
    from views.login import show_login
    from views.register import show_register
    from views.dashboard import show_dashboard
    from views.analysis import show_analysis
    from config import get_settings
    from providers.llm_factory import get_llm
    from utils.logger import configure_logging
    from components.auth_forms import show_auth_forms
    from components.sidebar import show_sidebar
    from views.reports import show_reports
    from views.assistant import show_assistant

    from services.auth_service import (
        register_user,
        authenticate_user,
        verify_token,
    )

    from models.analysis_models import BloodAnalysis

    print("✅ All imports completed successfully")

except Exception:
    traceback.print_exc()
    raise

# ─────────────────────────────────────────────

settings = get_settings()
logger = configure_logging()
logger.info("Launching %s", settings.app_name)

init_db()

llm = get_llm(temperature=0.1)

st.set_page_config(
    page_title="BloodIQ",
    page_icon="🩸",
    layout="wide",
)


# ------------------------------
# Session State Initialization
# ------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if "user" not in st.session_state:
    st.session_state.user = None

if "token" not in st.session_state:
    st.session_state.token = None

# ── STYLES ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}
.stApp { background: #0c0c0e; color: #e8e8e8; }
#MainMenu, footer, header { visibility: hidden; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #111114 !important;
    border-right: 1px solid #1f1f24 !important;
    padding: 0 !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }

.sb-logo {
    padding: 1.5rem 1.2rem 1rem 1.2rem;
    border-bottom: 1px solid #1f1f24;
    margin-bottom: 0.5rem;
}
.sb-logo-title {
    font-size: 1.15rem; font-weight: 700;
    color: #fff; letter-spacing: -0.3px;
    display: flex; align-items: center; gap: 8px;
}
.sb-logo-dot { color: #e63946; }
.sb-logo-sub { font-size: 0.72rem; color: #555; margin-top: 2px; }

.sb-section-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 2px;
    color: #444; text-transform: uppercase;
    padding: 0.8rem 1.2rem 0.3rem 1.2rem;
}

.sb-new-btn {
    margin: 0 0.8rem 0.5rem 0.8rem;
}

.history-card {
    margin: 0 0.8rem 0.4rem 0.8rem;
    background: #18181c;
    border: 1px solid #1f1f24;
    border-radius: 8px;
    padding: 10px 12px;
    cursor: pointer;
    transition: all 0.15s;
}
.history-card:hover { border-color: #e63946; background: #1c1c21; }
.history-card.active { border-color: #e63946; background: #1a1014; }
.hc-date { font-size: 0.68rem; color: #555; margin-bottom: 3px; }
.hc-preview { font-size: 0.78rem; color: #aaa; line-height: 1.4; }
.hc-badges { display: flex; gap: 4px; margin-top: 6px; flex-wrap: wrap; }
.hc-badge {
    font-size: 0.6rem; font-weight: 600; letter-spacing: 0.8px;
    padding: 2px 6px; border-radius: 4px; text-transform: uppercase;
}
.hc-badge.analysis { background: rgba(230,57,70,0.15); color: #e63946; }
.hc-badge.diet     { background: rgba(42,157,143,0.15); color: #2a9d8f; }

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1.2rem 0 1.5rem 0;
    border-bottom: 1px solid #1f1f24;
    margin-bottom: 1.8rem;
}
.topbar-title { font-size: 1.05rem; font-weight: 600; color: #e8e8e8; }
.topbar-sub   { font-size: 0.78rem; color: #555; margin-top: 2px; }
.topbar-badge {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 1px;
    color: #e63946; background: rgba(230,57,70,0.1);
    border: 1px solid rgba(230,57,70,0.2);
    padding: 4px 12px; border-radius: 20px; text-transform: uppercase;
}

/* ── STAGE HEADERS ── */
.stage-row {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 1rem;
}
.stage-num {
    width: 24px; height: 24px; background: #e63946;
    border-radius: 6px; font-size: 0.7rem; font-weight: 700;
    color: #fff; display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.stage-lbl {
    font-size: 0.75rem; font-weight: 600; color: #888;
    letter-spacing: 1.8px; text-transform: uppercase;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background: #111114 !important;
    color: #e4e4e4 !important;
    border: 1px solid #1f1f24 !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    line-height: 1.7 !important;
    caret-color: #e63946 !important;
}
.stTextArea textarea:focus {
    border-color: #e63946 !important;
    box-shadow: 0 0 0 3px rgba(230,57,70,0.1) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #333 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: #e63946 !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    padding: 0.55rem 1.2rem !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    transition: all 0.15s ease !important; width: 100% !important;
}
.stButton > button:hover {
    background: #c1121f !important;
    box-shadow: 0 4px 16px rgba(230,57,70,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── STATUS CARDS ── */
.card-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.sc {
    background: #111114; border: 1px solid #1f1f24;
    border-left: 3px solid #333; border-radius: 8px;
    padding: 10px 12px; min-height: 82px;
    display: flex; flex-direction: column; justify-content: space-between;
}
.sc.high   { border-left-color: #e63946; }
.sc.low    { border-left-color: #f4a261; }
.sc.normal { border-left-color: #2a9d8f; }
.sc-name  { font-size: 0.68rem; font-weight: 600; color: #555; text-transform: uppercase; letter-spacing: 1px; }
.sc-value { font-size: 1rem; font-weight: 700; color: #f0f0f0; font-family: 'JetBrains Mono', monospace; margin: 3px 0; }
.sc-ref   { font-size: 0.66rem; color: #3a3a3a; }
.sc-badge { display: inline-block; font-size: 0.58rem; font-weight: 700; letter-spacing: 1px; padding: 2px 7px; border-radius: 4px; margin-top: 5px; text-transform: uppercase; }
.sc-badge.high   { background: rgba(230,57,70,0.15);  color: #e63946; }
.sc-badge.low    { background: rgba(244,162,97,0.15);  color: #f4a261; }
.sc-badge.normal { background: rgba(42,157,143,0.15);  color: #2a9d8f; }

/* ── DIET BOX ── */
.diet-box {
    background: #111114; border: 1px solid #1f1f24;
    border-top: 3px solid #e63946; border-radius: 10px;
    padding: 1.4rem 1.6rem; color: #ccc;
    line-height: 1.9; font-size: 0.88rem;
}
.diet-box strong, .diet-box b { color: #e63946; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center; padding: 3rem 1rem;
    color: #333;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }
.empty-title { font-size: 0.9rem; font-weight: 600; color: #444; margin-bottom: 0.4rem; }
.empty-sub   { font-size: 0.78rem; color: #333; }

/* ── DIVIDER ── */
.sdiv { border: none; border-top: 1px solid #1f1f24; margin: 2rem 0 1.8rem 0; }

/* ── CHAT ── */
[data-testid="stChatMessage"] {
    background: #111114 !important;
    border: 1px solid #1f1f24 !important;
    border-radius: 10px !important;
    margin-bottom: 8px !important;
    padding: 0.8rem 1rem !important;
}
[data-testid="stChatInputContainer"] {
    background: #111114 !important;
    border: 1px solid #1f1f24 !important;
    border-radius: 10px !important;
}
[data-testid="stChatInputContainer"] textarea { color: #e4e4e4 !important; }

/* ── MISC ── */
.stAlert { background: #111114 !important; border: 1px solid #1f1f24 !important; color: #888 !important; border-radius: 8px !important; }
.stSuccess { background: rgba(42,157,143,0.08) !important; border: 1px solid rgba(42,157,143,0.25) !important; color: #2a9d8f !important; border-radius: 8px !important; }
.stSpinner > div { color: #e63946 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── HELPERS ───────────────────────────────────────────────────────────────
def render_cards(raw: str):
    lines = raw.strip().splitlines()
    html = '<div class="card-grid">'
    count = 0
    for line in lines:
        line = line.strip()
        if not line or "TEST:" not in line:
            continue
        try:
            parts = {p.split(":")[0].strip(): ":".join(p.split(":")[1:]).strip()
                     for p in line.split("|") if ":" in p}
            test   = parts.get("TEST", "—")
            value  = parts.get("VALUE", "—")
            status = parts.get("STATUS", "NORMAL").upper().strip()
            ref    = parts.get("REF", "—")
            css    = "high" if "HIGH" in status else ("low" if "LOW" in status else "normal")
            html += f"""<div class="sc {css}">
  <div class="sc-name">{test}</div>
  <div class="sc-value">{value}</div>
  <div class="sc-ref">Ref: {ref}</div>
  <span class="sc-badge {css}">{status}</span>
</div>"""
            count += 1
        except Exception:
            continue
    html += "</div>"
    return html, count


def extract_answer(result):
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        return result.get("answer", result.get("output", str(result)))
    return str(result)


def serialize_blood_analysis(analysis) -> str:
    blood_values = getattr(analysis, "blood_values", None)
    if isinstance(analysis, dict):
        blood_values = analysis.get("blood_values", blood_values)

    if not blood_values:
        return ""

    lines = []
    for blood_value in blood_values:
        parameter = getattr(blood_value, "parameter", None)
        value = getattr(blood_value, "value", None)
        status = getattr(blood_value, "status", None)
        reference_range = getattr(blood_value, "reference_range", None)

        if isinstance(blood_value, dict):
            parameter = blood_value.get("parameter", parameter)
            value = blood_value.get("value", value)
            status = blood_value.get("status", status)
            reference_range = blood_value.get("reference_range", reference_range)

        lines.append(
            f"TEST: {parameter or '—'} | VALUE: {value or '—'} | STATUS: {status or 'NORMAL'} | REF: {reference_range or '—'}"
        )

    return "\n".join(lines)


# ── SIDEBAR ───────────────────────────────────────────────────────────────

if st.session_state.logged_in:
    show_sidebar()

# ── TOPBAR ────────────────────────────────────────────────────────────────
report_id = st.session_state.get("report_id")
is_loaded = report_id is not None

st.markdown(f"""
<div class="topbar">
    <div>
        <div class="topbar-title">{"📋 Report #" + str(report_id) if is_loaded else "New Analysis"}</div>
        <div class="topbar-sub">{"Loaded from history — all stages restored" if is_loaded else "Paste a blood report to get started"}</div>
    </div>
    <div class="topbar-badge">Gemma 4 · RAG · ChromaDB</div>
</div>
""", unsafe_allow_html=True)


# # ── STAGE 1 ───────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="stage-row">
#     <div class="stage-num">1</div>
#     <div class="stage-lbl">Paste Report &amp; Analyze</div>
# </div>
# """, unsafe_allow_html=True)

# left, right = st.columns([1, 1], gap="large")

# with left:
#     default_text = st.session_state.get("report_text", "")
#     blood_report = st.text_area(
#         label="report",
#         value=default_text,
#         placeholder="Paste your blood report here...\n\nHemoglobin: 10.2 g/dL  (Ref: 13.5–17.5)\nWBC: 11,000 /µL  (Ref: 4,500–11,000)\n...",
#         height=380,
#         label_visibility="collapsed"
#     )
#     analyze_clicked = st.button("🔬  Analyze Report", use_container_width=True)

# with right:
#     if not st.session_state.get("extracted_values"):
#         st.markdown("""
#         <div class="empty-state">
#             <div class="empty-icon">📊</div>
#             <div class="empty-title">Test results appear here</div>
#             <div class="empty-sub">Paste a report on the left<br>and click Analyze</div>
#         </div>
#         """, unsafe_allow_html=True)

#     if analyze_clicked:
#         if not blood_report.strip():
#             st.warning("Paste a blood report first.")
#         else:
#             with st.spinner("Reading and classifying values..."):
#                 prompt_text = f"""You are a medical data extraction assistant.

# Extract EVERY test from the blood report. For each test output EXACTLY this format — one per line:
# TEST: <name> | VALUE: <result> | STATUS: <HIGH/LOW/NORMAL> | REF: <reference range>

# Rules:
# - STATUS must be exactly HIGH, LOW, or NORMAL only
# - No intro, no summary, no blank lines
# - Include every single test

# Blood Report:
# {blood_report}"""
#                 structured_llm = llm.with_structured_output(BloodAnalysis)

#                 analysis = structured_llm.invoke(prompt_text)
#                 raw = serialize_blood_analysis(analysis)

#                 st.session_state["analysis_summary"] = getattr(analysis, "patient_summary", None)
#                 st.session_state["health_score"] = getattr(analysis, "health_score", None)
#                 st.session_state["risk_level"] = getattr(analysis, "risk_level", None)
#                 st.session_state["extracted_values"] = raw
#                 st.session_state["report_text"]      = blood_report

#                 # Save or update in database
#                 if not st.session_state.get("report_id"):
#                     rid = save_report(blood_report)
#                     st.session_state["report_id"] = rid
#                 else:
#                     rid = st.session_state["report_id"]
#                 update_analysis(rid, raw)
#                 st.rerun()

#     if st.session_state.get("extracted_values"):
#         cards_html, count = render_cards(st.session_state["extracted_values"])
#         if count > 0:
#             st.markdown(cards_html, unsafe_allow_html=True)
#         else:
#             st.info("Could not parse structured results. Check the report format.")


# # ── STAGE 2 ───────────────────────────────────────────────────────────────
# if st.session_state.get("extracted_values"):
#     st.markdown('<hr class="sdiv"/>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="stage-row">
#         <div class="stage-num">2</div>
#         <div class="stage-lbl">Indian Diet Plan</div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Show saved diet plan if loaded from history
#     if st.session_state.get("diet_plan"):
#         st.markdown(
#             f'<div class="diet-box">{st.session_state["diet_plan"].replace(chr(10), "<br>")}</div>',
#             unsafe_allow_html=True
#         )
#         if st.button("🔄  Regenerate Diet Plan", use_container_width=False):
#             st.session_state.pop("diet_plan", None)
#             st.rerun()
#     else:
#         if st.button("🥗  Generate Diet Plan", use_container_width=False):
#             with st.spinner("Building your personalized diet plan..."):
#                 diet_prompt = f"""You are a clinical nutritionist specializing in Indian dietary habits.

# From the blood work below, identify ONLY the abnormal values (HIGH or LOW).
# Respond in exactly this structure:

# **Health Summary**
# 3-4 sentences in simple language about what the key abnormal results mean for this patient's health. Speak like a caring doctor.

# **Foods to Avoid**
# - List 4-5 specific Indian foods that directly worsen the abnormal values. One per line.

# **Foods to Eat More**
# - List 4-5 specific Indian foods that directly help correct the abnormal values. One per line.

# Focus only on abnormal values. Be concise.

# Blood Work:
# {st.session_state["extracted_values"]}"""
#                 diet_resp = llm.invoke(diet_prompt)
#                 diet_text = diet_resp.content
#                 if isinstance(diet_text, list):
#                     diet_text = "\n".join([r if isinstance(r, str) else r.get("text","") for r in diet_text])

#                 st.session_state["diet_plan"] = diet_text
#                 update_diet(st.session_state["report_id"], diet_text)

#             st.markdown(
#                 f'<div class="diet-box">{diet_text.replace(chr(10), "<br>")}</div>',
#                 unsafe_allow_html=True
#             )


# # ── STAGE 3 ───────────────────────────────────────────────────────────────
# if st.session_state.get("report_text"):
#     st.markdown('<hr class="sdiv"/>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="stage-row">
#         <div class="stage-num">3</div>
#         <div class="stage-lbl">Health Assistant Chat</div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Build RAG chain if not already built
#     if "rag_chain" not in st.session_state:
#         with st.spinner("Initialising health assistant..."):
#             combined = f"""BLOOD REPORT:
# {st.session_state["report_text"]}

# ANALYSIS:
# {st.session_state.get("extracted_values", "")}"""
#             st.session_state["rag_chain"] = build_rag_chain(combined)
#         st.success("✅ Assistant ready — ask anything about your health or your report.")

#     if "chat_history" not in st.session_state:
#         st.session_state["chat_history"] = []

#     # Render existing chat
#     for msg in st.session_state["chat_history"]:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Suggested questions when chat is empty
#     if not st.session_state["chat_history"]:
#         st.markdown("""
#         <div style="margin:0.5rem 0 1rem 0;">
#             <div style="font-size:0.72rem;color:#444;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.5rem;">Try asking</div>
#         </div>
#         """, unsafe_allow_html=True)
#         suggestions = [
#             "What does it mean if my hemoglobin is low?",
#             "Which of my values are most concerning?",
#             "What is the difference between HDL and LDL cholesterol?",
#             "What lifestyle changes can help improve my results?"
#         ]
#         cols = st.columns(2)
#         for i, suggestion in enumerate(suggestions):
#             with cols[i % 2]:
#                 if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
#                     st.session_state["chat_history"].append({"role": "user", "content": suggestion})
#                     save_message(st.session_state["report_id"], "user", suggestion)
#                     with st.spinner("Thinking..."):
#                         result = st.session_state["rag_chain"].invoke(
#                             {"input": suggestion},
#                             config={"configurable": {"session_id": f"session_{st.session_state['report_id']}"}}
#                         )
#                         answer = extract_answer(result)
#                     st.session_state["chat_history"].append({"role": "assistant", "content": answer})
#                     save_message(st.session_state["report_id"], "assistant", answer)
#                     st.rerun()

#     user_question = st.chat_input("Ask about your report or any health topic...")

#     if user_question:
#         st.session_state["chat_history"].append({"role": "user", "content": user_question})
#         save_message(st.session_state["report_id"], "user", user_question)

#         with st.chat_message("user"):
#             st.markdown(user_question)

#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 result = st.session_state["rag_chain"].invoke(
#                     {"input": user_question},
#                     config={"configurable": {"session_id": f"session_{st.session_state['report_id']}"}}
#                 )
#                 answer = extract_answer(result)
#             st.markdown(answer)
#             save_message(st.session_state["report_id"], "assistant", answer)
#             st.session_state["chat_history"].append({"role": "assistant", "content": answer})


if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"

if not st.session_state.logged_in:

    auth = show_auth_forms()

    if auth:

        with get_session() as db:

            if auth["action"] == "register":
                try:
                    register_user(
                        db=db,
                        email=auth["email"],
                        password=auth["password"],
                        full_name=auth["full_name"],
                        age=auth["age"],
                        gender=auth["gender"],
                    )
                    st.success("Registration Successful! Please login.")

                except Exception as e:
                    st.error(str(e))

            elif auth["action"] == "login":

                result = authenticate_user(
                    db=db,
                    email=auth["email"],
                    password=auth["password"],
                )

                if result:

                    user, token = result

                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.token = token
                    st.rerun()

                else:
                    st.error("Invalid email or password")

else:
    if st.session_state.current_page == "dashboard":
     show_dashboard()

    elif st.session_state.current_page == "analysis":
      show_analysis(
        llm=llm,
        save_report=save_report,
        update_analysis=update_analysis,
        update_diet=update_diet,
        render_cards=render_cards,
        serialize_blood_analysis=serialize_blood_analysis,
        BloodAnalysis=BloodAnalysis,
        build_rag_chain=build_rag_chain,
        extract_answer=extract_answer,
        save_message=save_message,
    )

    elif st.session_state.current_page == "reports":
      show_reports()
    elif st.session_state.current_page == "assistant":
      show_assistant()