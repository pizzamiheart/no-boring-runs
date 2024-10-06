import streamlit as st
import auth
import database
from strava_utils import get_strava_client, strava_callback, get_strava_activities
import logging
import map_utils
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="No Boring Runs", page_icon="🏃", layout="wide")

def main():
    st.title("No Boring Runs 🏃")

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
        with st.form("journey_setup_form"):
            total_distance = st.number_input("Total planned distance (miles)", min_value=1.0, step=0.1)
            start_date = st.date_input("Start date")
            end_date = st.date_input("End date")
            submit_button = st.form_submit_button("Start Journey")
            if submit_button:
                success, message = setup_journey(st.session_state.user, total_distance, start_date, end_date)
                if success:
                    st.success(message)
                    # Display the starting point on a map
                    journey = database.get_user_journey(st.session_state.user)
                    if journey:
                        total_miles, start_date, end_date, current_lat, current_lon = journey
                        st.map(pd.DataFrame({'lat': [float(current_lat)], 'lon': [float(current_lon)]}))
                else:
                    st.error(message)

    elif choice == "Add Run":
        st.subheader("Add New Run")
        with st.form("add_run_form"):
            distance = st.number_input("Distance (miles)", min_value=0.1, step=0.1)
            date = st.date_input("Date")
            submit_button = st.form_submit_button("Save Run")
            if submit_button:
                success = database.add_run(st.session_state.user, distance, date)
                if success:
                    st.success("Run added successfully!")
                else:
                    st.error("Failed to add run. Please try again.")

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

    # Display journey progress
    journey = database.get_user_journey(st.session_state.user)
    if journey:
        st.subheader("Your Journey Progress")
        total_miles, start_date, end_date, current_lat, current_lon = journey
        progress = (float(current_lat) / float(total_miles)) * 100
        st.progress(progress)
        st.map(pd.DataFrame({'lat': [float(current_lat)], 'lon': [float(current_lon)]}))

        # Display user's runs
        runs = database.get_user_runs(st.session_state.user)
        if runs:
            st.subheader("Your Runs")
            for run in runs:
                st.write(f"Date: {run['date']}, Distance: {run['distance']} miles")
        else:
            st.info("No runs recorded yet. Add a run to see your progress!")
    else:
        st.info("Set up your journey to see your progress!")

def setup_journey(username, total_distance, start_date, end_date):
    try:
        starting_point = map_utils.generate_random_start_point()
        success = database.create_user_journey(username, float(total_distance), start_date, end_date, starting_point)
        if success:
            return True, "Journey set up successfully!"
        else:
            return False, "Failed to set up journey. Please try again."
    except Exception as e:
        logger.error(f"Error setting up journey: {str(e)}")
        return False, "An error occurred while setting up the journey. Please try again."

if __name__ == "__main__":
    main()