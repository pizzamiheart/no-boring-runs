import folium
import random

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
    return (lat, lon)
