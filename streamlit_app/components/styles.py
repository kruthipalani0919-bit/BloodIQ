import streamlit as st


def load_css():
    st.markdown(
        """
        <style>

        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"]{
            font-family: 'Inter', sans-serif;
        }

        .stApp{
            background:#09090B;
            color:white;
        }

        section[data-testid="stSidebar"]{
            background:#111111;
            border-right:1px solid #202020;
        }

        h1,h2,h3{
            color:white;
        }

        .block-container{
            padding-top:2rem;
            padding-left:3rem;
            padding-right:3rem;
        }

        div[data-testid="stForm"]{
            background:#18181B;
            border:1px solid #2A2A2A;
            border-radius:16px;
            padding:30px;
        }

        .stTextInput input{
            background:#111111;
            color:white;
            border-radius:10px;
        }

        .stButton>button{
            width:100%;
            border-radius:10px;
            background:#EF4444;
            color:white;
            border:none;
            height:45px;
            font-weight:600;
        }

        .stButton>button:hover{
            background:#DC2626;
        }

        </style>
        """,
        unsafe_allow_html=True
    )