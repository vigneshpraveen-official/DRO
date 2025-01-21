# Dynamic Route Optimizer

Dynamic Route Optimizer is an advanced web application designed to revolutionize urban transportation by optimizing routes based on real-time data. It addresses challenges like traffic congestion, road safety, and environmental sustainability, making travel efficient, safe, and eco-friendly.

---

## Features

### 1. Real-Time Route Optimization
- Calculates efficient routes using the **OpenRouteService API**.
- Factors in distance, traffic density, and weather conditions.

### 2. Traffic Density Analysis
- Monitors live traffic conditions with the **TomTom Traffic API**.
- Classifies traffic as **Heavy**, **Moderate**, or **Light**.

### 3. Weather Integration
- Fetches real-time weather updates via **OpenWeather API**.
- Provides detailed weather insights for safer travel.

### 4. Emissions Estimation
- Calculates CO2 emissions based on route distance and vehicle type.
- Promotes eco-friendly travel choices.

### 5. Map Visualization
- Displays optimized routes with the **TomTom Static Map API**.
- Offers intuitive, visually appealing maps.

---

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **APIs Used**:
  - OpenRouteService
  - TomTom Traffic & Maps
  - OpenWeather
- **Geolocation**: Nominatim Library

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/dynamic-route-optimizer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd dynamic-route-optimizer
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Access the application in your browser at:
   ```
   http://127.0.0.1:5000/
   ```

---

## Usage

1. Enter the start and end locations.
2. Select the vehicle type.
3. Click on "Optimize Route" to get:
   - Distance
   - Traffic density
   - Weather conditions
   - Estimated CO2 emissions
   - Visualized route map

---

## Screenshots

### Home Page
![Home Page](https://via.placeholder.com/600x300)

### Results
![Results](https://via.placeholder.com/600x300)

---

## Potential Enhancements

- **AI Integration**: Predictive traffic and hazard analysis.
- **Dynamic Signal Control**: Traffic signal optimization.
- **Incident Detection**: Integrate IoT and camera systems.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Email**: vigneshpraveenofficial@gmail.com  
- **GitHub**: [vigneshpraveen-official](https://github.com/vigneshpraveen-official)  
- **LinkedIn**: [Vignesh Praveen](https://www.linkedin.com/in/vigneshpraveen)
