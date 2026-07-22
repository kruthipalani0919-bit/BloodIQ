import streamlit as st
from components.styles import load_css


def show_register():

    load_css()

    st.title("🩸 BloodIQ")

    st.caption("Create your BloodIQ account")

    st.write("")

    left, center, right = st.columns([1, 2, 1])

    with center:

        st.subheader("Create Account")

        with st.form("register_form"):

            full_name = st.text_input(
                "Full Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email",
                placeholder="Enter your email"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password"
            )

            register_clicked = st.form_submit_button("Create Account")

        st.write("")

        back_clicked = st.button("← Back to Login")

    return {
        "register": register_clicked,
        "back": back_clicked,
        "name": full_name,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
    }