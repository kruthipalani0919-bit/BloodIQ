import streamlit as st

def show_welcome_banner(user_name="Guest"):

  

    st.markdown(
        f"""
        <div style="background:red;padding:30px;border-radius:20px;">
            <h1 style="color:white;">Hello {user_name}</h1>
           <p style="
            margin-top:12px;
        color:#f3f4f6;
        font-size:18px;
        line-height:1.7;
        ">
        Your AI-powered health companion is ready to analyze reports,
        generate personalized diet plans, and answer your medical questions.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )