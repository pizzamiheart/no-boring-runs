import streamlit as st
import logging
from database import get_db_connection, init_db, authenticate_user, create_user, user_exists, get_user_journey, add_run, get_user_runs
import datetime

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
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.user = username
            st.success(f"Logged in as {username}")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

def register():
    st.subheader("Create New Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif user_exists(new_username):
            st.error("Username already exists")
        else:
            create_user(new_username, new_password, False)
            st.success("Account created successfully. Please log in.")

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
        st.experimental_rerun()

if __name__ == "__main__":
    init_db()  # Initialize the database
    main()
