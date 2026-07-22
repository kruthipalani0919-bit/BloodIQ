import streamlit as st

def show_metric_card(icon, title, value):

    st.markdown(
        f"""
<div style="background:#161616;padding:20px;border-radius:15px;">
<h1>{icon}</h1>
<h4>{title}</h4>
<h2>{value}</h2>
</div>
""",
        unsafe_allow_html=True,
    )