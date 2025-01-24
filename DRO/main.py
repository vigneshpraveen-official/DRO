import requests
from flask import Flask, request, jsonify, render_template
import json
import openai  # Ensure you have `openai` installed

# Configuration
TOMTOM_API_KEY = "Y4d95dZrj0C8SsOqAXq6fUGqITwfFipU"
OPENWEATHER_API_KEY = "ea96c69aff8dab6f6b1be765c0ef4b8a"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/drobro')
def drobro():
    return render_template('drobro.html')


def get_coordinates(place_name):
    """Get coordinates using TomTom Geocoding API"""
    try:
        url = f"https://api.tomtom.com/search/2/geocode/{place_name}.json"
        params = {
            "key": TOMTOM_API_KEY,
            "limit": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for bad status codes
        
        data = response.json()
        if data.get('results') and len(data['results']) > 0:
            location = data['results'][0]['position']
            return location['lat'], location['lon']
        return None
    except Exception as e:
        print(f"Error in get_coordinates: {str(e)}")
        return None

def get_route(start_coords, end_coords):
    """Get route using TomTom Routing API"""
    try:
        start_point = f"{start_coords[0]},{start_coords[1]}"
        end_point = f"{end_coords[0]},{end_coords[1]}"
        
        url = f"https://api.tomtom.com/routing/1/calculateRoute/{start_point}:{end_point}/json"
        params = {
            "key": TOMTOM_API_KEY,
            "routeType": "fastest",
            "traffic": "true",
            "instructionsType": "text",
            "language": "en-US"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"Error in get_route: {str(e)}")
        return None

def get_weather(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in get_weather: {str(e)}")
        return None

def get_traffic_density(coords):
    try:
        lat, lon = coords
        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
        params = {
            "key": TOMTOM_API_KEY,
            "point": f"{lat},{lon}"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        if 'flowSegmentData' in data:
            free_flow_speed = data['flowSegmentData'].get('freeFlowSpeed', 0)
            current_speed = data['flowSegmentData'].get('currentSpeed', 0)
            
            if free_flow_speed == 0:
                return "Unknown"
            
            ratio = current_speed / free_flow_speed if free_flow_speed > 0 else 0
            
            if ratio < 0.5:
                return "Heavy"
            elif ratio < 0.8:
                return "Moderate"
            else:
                return "Light"
        return "Unknown"
    except Exception as e:
        print(f"Error in get_traffic_density: {str(e)}")
        return "Unknown"

def calculate_emissions(distance_km, vehicle_type="car"):
    emissions_factor = {
        "car": 0.120,
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
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        start = data.get("start", "").strip()
        end = data.get("end", "").strip()
        vehicle_type = data.get("vehicle_type", "car").strip().lower()

        if not start or not end:
            return jsonify({"error": "Start and end locations are required"}), 400

        print(f"Processing route from {start} to {end} via {vehicle_type}")

        start_coords = get_coordinates(start)
        if not start_coords:
            return jsonify({"error": f"Could not find coordinates for {start}"}), 400

        end_coords = get_coordinates(end)
        if not end_coords:
            return jsonify({"error": f"Could not find coordinates for {end}"}), 400

        print(f"Coordinates found - Start: {start_coords}, End: {end_coords}")

        route_data = get_route(start_coords, end_coords)
        if not route_data:
            return jsonify({"error": "Unable to calculate route"}), 400

        # Extract route information
        route = route_data.get('routes', [{}])[0]
        summary = route.get('summary', {})
        
        distance_meters = summary.get('lengthInMeters', 0)
        distance_km = distance_meters / 1000
        travel_time = summary.get('travelTimeInSeconds', 0)

        # Extract route points
        route_points = []
        if 'legs' in route and route['legs']:
            points = route['legs'][0].get('points', [])
            route_points = [{'latitude': point['latitude'], 
                           'longitude': point['longitude']} 
                          for point in points]

        # Get navigation instructions
        instructions = []
        if 'guidance' in route and 'instructions' in route['guidance']:
            instructions = [item.get('message', '') 
                          for item in route['guidance']['instructions']]

        # Get additional information
        traffic_density = get_traffic_density(start_coords)
        weather_data = get_weather(*start_coords)
        weather_status = "Unknown"
        if weather_data and 'weather' in weather_data and weather_data['weather']:
            weather_status = weather_data['weather'][0].get('description', 'Unknown')

        emissions = calculate_emissions(distance_km, vehicle_type)

        response_data = {
            "distance_km": round(distance_km, 2),
            "travel_time_minutes": round(travel_time / 60, 1),
            "traffic_density": traffic_density,
            "weather_status": weather_status,
            "emissions_kg": round(emissions, 2),
            "start_coords": start_coords,
            "end_coords": end_coords,
            "route_points": route_points,
            "navigation_instructions": instructions
        }

        print("Successfully processed route")
        return jsonify(response_data)

    except Exception as e:
        print(f"Error in optimize_route: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
