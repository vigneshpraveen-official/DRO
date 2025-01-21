import requests
from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim

# Configuration
ORS_API_KEY = "5b3ce3597851110001cf6248f94a610ca0b04b0a979845b220b29acd"
OPENWEATHER_API_KEY = "ea96c69aff8dab6f6b1be765c0ef4b8a"
TOMTOM_API_KEY = "Y4d95dZrj0C8SsOqAXq6fUGqITwfFipU"  # Replace with your key

app = Flask(__name__)


def get_coordinates(place_name):
    geolocator = Nominatim(user_agent="route_optimizer")
    location = geolocator.geocode(place_name)
    if location:
        return location.latitude, location.longitude
    else:
        return None


def get_route(start_coords, end_coords):
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    headers = {"Authorization": ORS_API_KEY}
    params = {
        "start": f"{start_coords[1]},{start_coords[0]}",  # lng,lat format
        "end": f"{end_coords[1]},{end_coords[0]}"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None


def get_weather(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


def get_traffic_density(coords):
    lat, lon = coords
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?key={TOMTOM_API_KEY}&point={lat},{lon}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        free_flow_speed = data['flowSegmentData']['freeFlowSpeed']
        current_speed = data['flowSegmentData']['currentSpeed']
        if current_speed < 0.5 * free_flow_speed:
            return "Heavy"
        elif current_speed < 0.8 * free_flow_speed:
            return "Moderate"
        else:
            return "Light"
    return "Unknown"


def calculate_emissions(distance_km, vehicle_type="car"):
    emissions_factor = {
        "car": 0.120,  # kg CO2 per km
        "motorcycle": 0.072,
        "bus": 0.100,
        "truck": 0.250
    }
    return distance_km * emissions_factor.get(vehicle_type, 0.120)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/optimize', methods=['POST'])
def optimize_route():
    data = request.json
    start = data.get("start").strip().lower()
    end = data.get("end").strip().lower()
    vehicle_type = data.get("vehicle_type", "car").strip().lower()

    start_coords = get_coordinates(start)
    end_coords = get_coordinates(end)

    if not start_coords or not end_coords:
        return jsonify({"error": "Invalid start or end location."}), 400

    route = get_route(start_coords, end_coords)
    if not route:
        return jsonify({"error": "Unable to calculate route."}), 500

    distance_meters = route['features'][0]['properties']['segments'][0]['distance']
    distance_km = distance_meters / 1000

    traffic_density = get_traffic_density(start_coords)

    weather_start = get_weather(*start_coords)
    weather_status = weather_start['weather'][0]['description'] if weather_start else "Unknown"

    emissions = calculate_emissions(distance_km, vehicle_type)

    return jsonify({
        "distance_km": round(distance_km, 2),
        "traffic_density": traffic_density,
        "weather_status": weather_status,
        "emissions_kg": round(emissions, 2),
        "start_coords": start_coords,
        "end_coords": end_coords
    })


@app.route('/get_map', methods=['POST'])
def get_map():
    data = request.json
    start_coords = data.get("start_coords")
    end_coords = data.get("end_coords")

    if not start_coords or not end_coords:
        return jsonify({"error": "Invalid coordinates for map display."}), 400

    # Fixing bbox ordering: minLon, minLat, maxLon, maxLat
    min_lat = min(start_coords[0], end_coords[0])
    max_lat = max(start_coords[0], end_coords[0])
    min_lon = min(start_coords[1], end_coords[1])
    max_lon = max(start_coords[1], end_coords[1])

    # Construct the TomTom Static Map URL
    map_url = (
        f"https://api.tomtom.com/map/1/staticimage?"
        f"layer=basic&style=main&format=png&zoom=12&center={start_coords[1]},{start_coords[0]}"
        f"&width=512&height=512&key={TOMTOM_API_KEY}"
        f"&traffic=true&bbox={min_lon},{min_lat},{max_lon},{max_lat}"
    )

    return jsonify({"map_url": map_url})


if __name__ == "__main__":
    app.run(debug=True)
