import streamlit as st
import database
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login(username, password):
    try:
        logger.info(f"Attempting login for user: {username}")
        user_data = database.get_user_data(username)
        if user_data:
            logger.info(f"User data found: {user_data[0]}, Password hash: {user_data[1][:10]}...")
        else:
            logger.warning(f"No user data found for {username}")
        auth_result = database.authenticate_user(username, password)
        logger.info(f"Authentication result: {auth_result}")
        if auth_result:
            logger.info(f"Session state before login: {st.session_state}")
            st.session_state.user = username
            logger.info(f"Session state after login: {st.session_state}")
            logger.info(f"User {username} logged in successfully")
            st.success(f"Logged in as {username}")
            st.experimental_rerun()
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
    strava_connect = st.checkbox("Connect with Strava (optional)")
    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif database.user_exists(new_username):
            st.error("Username already exists")
        else:
            try:
                database.create_user(new_username, new_password, strava_connect)
                logger.info(f"User {new_username} registered successfully")
                st.success("Account created successfully. Please log in.")
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                st.error("An error occurred during registration. Please try again later.")
