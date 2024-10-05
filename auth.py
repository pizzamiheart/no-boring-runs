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
            return True, f"Logged in as {username}"
        else:
            logger.warning(f"Failed login attempt for user {username}")
            return False, "Invalid username or password"
    except Exception as e:
        logger.error(f"Error during login process: {str(e)}")
        return False, "An error occurred during login. Please try again later."

def register(new_username, new_password, confirm_password):
    if new_password != confirm_password:
        return False, "Passwords do not match"
    elif database.get_user_data(new_username):
        return False, "Username already exists"
    else:
        try:
            database.create_user(new_username, new_password)
            logger.info(f"User {new_username} registered successfully")
            return True, "Account created successfully. Please log in."
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}")
            return False, "An error occurred during registration. Please try again later."

def logout():
    st.session_state.user = None
    logger.info("User logged out")
    return "Logged out successfully"
