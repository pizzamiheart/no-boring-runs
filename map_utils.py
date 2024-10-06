import folium
import random
from math import radians, sin, cos, sqrt, atan2

def create_map(current_position):
    m = folium.Map(location=current_position, zoom_start=4)
    folium.Marker(
        current_position,
        popup="Your current position",
        icon=folium.Icon(color="red", icon="info-sign"),
    ).add_to(m)
    return m

def generate_random_start_point():
    # Generate a random latitude and longitude
    lat = random.uniform(-90, 90)
    lon = random.uniform(-180, 180)
    return (float(lat), float(lon))

def get_run_coordinates(username):
    runs = database.get_user_runs(username)
    coordinates = []
    journey = database.get_user_journey(username)
    if journey:
        current_position = (journey[3], journey[4])
        coordinates.append(current_position)
    
    for run in runs:
        new_position = run_utils.update_position(username, run['distance'])
        coordinates.append(new_position)
    
    return coordinates

def calculate_distance(start_point, end_point):
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1 = start_point
    lat2, lon2 = end_point
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance * 0.621371  # Convert to miles
