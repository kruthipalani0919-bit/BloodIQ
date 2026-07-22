import streamlit as st


def show_auth_forms():
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", use_container_width=True):
            return {
                "action": "login",
                "email": email,
                "password": password,
            }

    with tab2:
        st.subheader("Create Account")

        full_name = st.text_input(
            "Full Name",
            key="register_name"
        )

        email = st.text_input(
            "Email",
            key="register_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        if st.button("Register", use_container_width=True):
            return {
                "action": "register",
                "full_name": full_name,
                "email": email,
                "password": password,
                "age": age,
                "gender": gender,
            }

    return None