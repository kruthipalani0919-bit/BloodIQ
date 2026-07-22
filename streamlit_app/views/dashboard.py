from scipy import stats
import streamlit as st

from components.dashboard.welcome_banner import show_welcome_banner
from components.dashboard.metric_card import show_metric_card
from components.dashboard.quick_actions import show_quick_actions
from components.dashboard.recent_reports import show_recent_reports
from database import get_dashboard_stats


def show_dashboard():
    user_name = (
    st.session_state.user.full_name
    if st.session_state.get("user")
    else "Guest"
)
    
    stats = get_dashboard_stats()
    show_welcome_banner(user_name)

 
    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        show_metric_card(
    "❤️",
    "Health Score",
    str(stats["health_score"])
)
    with c2:
        show_metric_card(
    "📄",
    "Reports",
    str(stats["reports"])
)
        
    with c3:
        show_metric_card(
    "⚠️",
    "Risk Level",
    stats["risk"]
)
    with c4:
       show_metric_card(
    "🤖",
    "AI Status",
    stats["status"]
)
    st.write("")

    show_quick_actions()

    st.write("")

    show_recent_reports()