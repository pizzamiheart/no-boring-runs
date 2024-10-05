import streamlit as st
import logging
from database import get_db_connection, init_db, authenticate_user, create_user, user_exists, get_user_journey, add_run, get_user_runs
import datetime
import auth

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up page config
st.set_page_config(page_title="Not Boring Runs", page_icon="🏃", layout="wide")

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.title("Not Boring Runs 🏃")

    # Check if user is logged in
    if st.session_state.user:
        logger.info(f"User {st.session_state.user} is logged in")
        st.sidebar.success(f"Logged in as {st.session_state.user}")
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
    else:
        logger.info("No user logged in")

    # Sidebar for navigation
    menu = ["Home", "Login", "Register", "Dashboard", "Add Run"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home()
    elif choice == "Login":
        login()
    elif choice == "Register":
        register()
    elif choice == "Dashboard":
        if st.session_state.user:
            dashboard()
        else:
            st.warning("Please login to view your dashboard.")
    elif choice == "Add Run":
        if st.session_state.user:
            add_run_page()
        else:
            st.warning("Please login to add a new run.")

def home():
    st.subheader("Welcome to Not Boring Runs!")
    st.write("Gamify your running experience with virtual journeys across the world!")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        logger.info(f"Login attempt for user: {username}")
        if authenticate_user(username, password):
            st.session_state.user = username
            logger.info(f"User {username} logged in successfully")
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            logger.warning(f"Failed login attempt for user {username}")
            st.error("Invalid username or password")

def register():
    auth.register()

def dashboard():
    st.subheader(f"Welcome, {st.session_state.user}!")
    journey = get_user_journey(st.session_state.user)
    if journey:
        total_miles, start_date, end_date, current_position = journey
        st.write(f"Total Distance: {total_miles} miles")
        st.write(f"Start Date: {start_date}")
        st.write(f"End Date: {end_date}")
        st.write(f"Current Position: {current_position}")
        
        runs = get_user_runs(st.session_state.user)
        if runs:
            st.subheader("Your Runs")
            for run in runs:
                st.write(f"Date: {run['date']}, Distance: {run['distance']} miles")
        else:
            st.info("You haven't logged any runs yet. Start running!")
    else:
        st.info("You haven't started a journey yet. Add a run to begin your adventure!")

def add_run_page():
    st.subheader("Add New Run")
    distance = st.number_input("Distance (miles)", min_value=0.1, step=0.1)
    date = st.date_input("Date", max_value=datetime.date.today())
    if st.button("Save Run"):
        add_run(st.session_state.user, distance, date)
        st.success("Run added successfully!")
        st.rerun()

if __name__ == "__main__":
    init_db()  # Initialize the database
    main()
