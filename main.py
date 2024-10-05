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
        st.sidebar.success(f"Logged in as {st.session_state.user}")
        if st.sidebar.button("Logout"):
            auth.logout()
    else:
        choice = st.sidebar.selectbox("Login/Signup", ["Login", "Sign Up"])
        if choice == "Login":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                auth.login(username, password)
        else:
            auth.register()

    if st.session_state.user:
        menu = ["Dashboard", "Add Run", "Strava Activities"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Dashboard":
            st.subheader("Dashboard")
            # Add dashboard content here

        elif choice == "Add Run":
            st.subheader("Add New Run")
            distance = st.number_input("Distance (miles)", min_value=0.1, step=0.1)
            date = st.date_input("Date")
            if st.button("Save Run"):
                database.add_run(st.session_state.user, distance, date)
                st.success("Run added successfully!")

        elif choice == "Strava Activities":
            st.subheader("Strava Activities")
            user_data = database.get_user_data(st.session_state.user)
            if user_data and user_data['strava_token']:
                client = get_strava_client()
                activities = get_strava_activities(client, user_data['strava_token']['access_token'])
                for activity in activities:
                    st.write(f"{activity.name} - {activity.distance.num:.2f} miles")
            else:
                st.warning("Strava account not connected")
                client = get_strava_client()
                auth_url = client.authorization_url(
                    client_id=st.secrets["STRAVA_CLIENT_ID"],
                    redirect_uri=st.secrets["STRAVA_REDIRECT_URI"],
                    scope=['read', 'activity:read_all']
                )
                st.markdown(f"[Connect Strava Account]({auth_url})")

    else:
        st.subheader("Welcome to Not Boring Runs!")
        st.write("Please login or sign up to start your running journey.")

if __name__ == "__main__":
    main()
