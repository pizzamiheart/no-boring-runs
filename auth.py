import streamlit as st
import database
import logging
from strava_utils import get_strava_client, strava_auth_url

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login(username, password):
    try:
        logger.info(f"Attempting login for user: {username}")
        user_data = database.get_user_data(username)
        if user_data and user_data['password'] == password:
            st.session_state.user = username
            logger.info(f"User {username} logged in successfully")
            st.success(f"Logged in as {username}")
            if user_data['strava_token']:
                st.success("Strava account connected")
            else:
                st.warning("Strava account not connected")
                client = get_strava_client()
                auth_url = strava_auth_url(client)
                st.markdown(f"[Connect Strava Account]({auth_url})")
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
    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif database.get_user_data(new_username):
            st.error("Username already exists")
        else:
            try:
                database.create_user(new_username, new_password)
                logger.info(f"User {new_username} registered successfully")
                st.success("Account created successfully. Please log in.")
                st.rerun()
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                st.error("An error occurred during registration. Please try again later.")

def logout():
    st.session_state.user = None
    logger.info("User logged out")
    st.success("Logged out successfully")
    st.rerun()
