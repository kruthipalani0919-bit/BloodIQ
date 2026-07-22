import streamlit as st
from components.styles import load_css


def show_login():

    load_css()

    st.title("🩸 BloodIQ")

    st.caption("AI Powered Blood Report Analysis Platform")

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.subheader("Welcome Back")

        st.write("Sign in to continue")

        with st.form("login_form"):

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            login_clicked = st.form_submit_button("Login")

        st.write("")

        register_clicked = st.button("Create New Account")

    return {
        "login": login_clicked,
        "register": register_clicked,
        "email": email,
        "password": password,
    }