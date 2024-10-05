import streamlit as st
import database

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if database.authenticate_user(username, password):
            st.session_state.user = username
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    strava_connect = st.checkbox("Connect with Strava")
    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif database.user_exists(new_username):
            st.error("Username already exists")
        else:
            database.create_user(new_username, new_password, strava_connect)
            st.success("Account created successfully. Please log in.")
