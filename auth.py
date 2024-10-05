import streamlit as st
import database
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login(username, password):
    try:
        if database.authenticate_user(username, password):
            st.session_state.user = username
            logger.info(f"User {username} logged in successfully")
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            logger.warning(f"Failed login attempt for user {username}")
            st.error("Invalid username or password")
    except Exception as e:
        logger.error(f"Error during login process: {str(e)}")
        st.error(f"An error occurred during login. Please try again later.")

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
