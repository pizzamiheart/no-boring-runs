import streamlit as st
import auth
import database
from strava_utils import get_strava_client, strava_callback, get_strava_activities
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Not Boring Runs", page_icon="🏃", layout="wide")

def main():
    st.title("Not Boring Runs 🏃")

    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        display_dashboard()
    else:
        display_login_register()

def display_login_register():
    choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign Up"])
    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            if submit_button:
                success, message = auth.login(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
    else:
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_button = st.form_submit_button("Register")
            if submit_button:
                success, message = auth.register(new_username, new_password, confirm_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

def display_dashboard():
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout"):
        message = auth.logout()
        st.success(message)
        st.rerun()

    menu = ["Journey Setup", "Add Run", "Strava Activities"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Journey Setup":
        st.subheader("Set Up Your Journey")
        # TODO: Implement journey setup form

    elif choice == "Add Run":
        st.subheader("Add New Run")
        with st.form("add_run_form"):
            distance = st.number_input("Distance (miles)", min_value=0.1, step=0.1)
            date = st.date_input("Date")
            submit_button = st.form_submit_button("Save Run")
            if submit_button:
                # TODO: Implement add_run function in database.py
                st.success("Run added successfully!")

    elif choice == "Strava Activities":
        st.subheader("Strava Activities")
        user_data = database.get_user_data(st.session_state.user)
        if user_data and user_data.get('strava_token'):
            # TODO: Implement Strava activities display
            st.info("Strava activities will be displayed here")
        else:
            st.warning("Strava account not connected")
            if st.button("Connect with Strava"):
                # TODO: Implement Strava OAuth flow
                st.info("Strava connection flow will be implemented here")

    # Placeholder for map and progress bar
    st.subheader("Your Journey Progress")
    st.info("Map and progress bar will be displayed here")

if __name__ == "__main__":
    main()
