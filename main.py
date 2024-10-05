import streamlit as st
import folium
from streamlit_folium import folium_static
import auth
import database
import map_utils
import run_utils

st.set_page_config(page_title="Not Boring Runs", page_icon="🏃", layout="wide")

# Apply custom CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

def main():
    st.title("Not Boring Runs 🏃")

    # Sidebar for navigation
    menu = ["Home", "Login", "Register", "Dashboard", "New Run"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Welcome to Not Boring Runs!")
        st.image("assets/logo.svg", width=300)
        st.write("Gamify your running experience with virtual journeys across the world!")

    elif choice == "Login":
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Login")
            if submit_button:
                auth.login()

    elif choice == "Register":
        auth.register()

    elif choice == "Dashboard":
        if st.session_state.user:
            show_dashboard()
        else:
            st.warning("Please login to view your dashboard.")

    elif choice == "New Run":
        if st.session_state.user:
            add_new_run()
        else:
            st.warning("Please login to add a new run.")

def show_dashboard():
    st.subheader(f"Welcome, {st.session_state.user}!")

    # Fetch user's journey details
    journey = database.get_user_journey(st.session_state.user)
    if not journey:
        st.warning("You haven't started a journey yet. Let's create one!")
        create_journey()
    else:
        total_miles, start_date, end_date, current_position = journey
        
        # Calculate progress
        runs = database.get_user_runs(st.session_state.user)
        total_run_miles = sum(run['distance'] for run in runs)
        progress = min(total_run_miles / total_miles, 1.0)
        
        # Display progress bar
        st.subheader("Journey Progress")
        st.progress(progress)
        st.write(f"Total Distance: {total_run_miles:.2f} / {total_miles} miles")
        st.write(f"Start Date: {start_date}")
        st.write(f"End Date: {end_date}")

        # Display map
        m = map_utils.create_map(current_position)
        
        # Add polyline to show user's path
        path_coordinates = map_utils.get_run_coordinates(st.session_state.user)
        folium.PolyLine(locations=path_coordinates, weight=2, color='red').add_to(m)
        
        folium_static(m)

        # Display run history
        if runs:
            st.subheader("Run History")
            for run in runs:
                st.write(f"Date: {run['date']}, Distance: {run['distance']} miles")
        else:
            st.info("No runs recorded yet. Start running!")

def create_journey():
    st.subheader("Create Your Journey")
    with st.form("journey_form"):
        total_miles = st.number_input("Total Planned Miles", min_value=1, value=100)
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        submitted = st.form_submit_button("Start Journey")

    if submitted:
        start_position = map_utils.generate_random_start_point()
        database.create_user_journey(st.session_state.user, total_miles, start_date, end_date, start_position)
        st.success("Journey created successfully!")
        st.rerun()

def add_new_run():
    st.subheader("Add New Run")
    with st.form("new_run_form"):
        distance = st.number_input("Distance (miles)", min_value=0.1, step=0.1)
        date = st.date_input("Date")
        submitted = st.form_submit_button("Save Run")

    if submitted:
        database.add_run(st.session_state.user, distance, date)
        new_position = run_utils.update_position(st.session_state.user, distance)
        database.update_user_position(st.session_state.user, new_position)
        st.success("Run added successfully!")
        st.rerun()

if __name__ == "__main__":
    main()
