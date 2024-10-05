import math
import database

def update_position(username, distance):
    journey = database.get_user_journey(username)
    if not journey:
        return None

    total_miles, _, _, current_position = journey
    lat, lon = current_position[0], current_position[1]

    # Convert distance from miles to degrees (approximate)
    distance_deg = distance / 69

    # Generate a random angle for the direction
    angle = math.radians(random.uniform(0, 360))

    # Calculate new position
    new_lat = lat + (distance_deg * math.cos(angle))
    new_lon = lon + (distance_deg * math.sin(angle))

    # Ensure the new position is within valid bounds
    new_lat = max(min(new_lat, 90), -90)
    new_lon = (new_lon + 180) % 360 - 180

    return (new_lat, new_lon)
