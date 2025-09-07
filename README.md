# SIH-Internal-2025-Bamboocopter

# 🚁 Team Bamboocopter – Internal Hackathon (SIH)

This repository contains the codebase developed by **Team Bamboocopter** for the **Internal Hackathon (SIH)**.  
It demonstrates drone path planning, simulation, MAVLink communication, and object detection modules.

## 📂 Repository Structure
```
├── map.py # Generates road network maps & shortest paths between cities
├── mavlink.py # Connects to drone via MAVLink, arms, takes off & lands
├── objectdetection.py # Detects nearby objects in a video feed using OpenCV
├── realsim.py # Drone path simulation with map animation & elevation profiling
├── rtlsimuint.py # Simulates drone path on a map using RTLS coordinates
├── satel.py # Handles satellite data & positioning for drone navigation
├── drone-in-sky-for-ml_slowed.mp4 # Sample drone video for object detection
├── README.md # Project overview, setup instructions, and usage
```

## ⚙️ Features

### 1. `map.py` – City-to-City Mapping  
- Uses **OSMnx** + **NetworkX** to fetch road networks.  
- Computes **shortest route** and **all shortest paths** between two cities.  
- Generates interactive **Folium maps** (`all_routes_map.html`, `shortest_route_map.html`).  

### 2. `mavlink.py` – Drone Control  
- Connects to a drone (via `COM3`, 115200 baud).  
- Sets **GUIDED mode**, arms motors, takes off to **10m altitude**, and lands.  
- Uses **pymavlink** for communication.  

### 3. `objectdetection.py` – Object Detection  
- Reads a **video feed** (`drone-in-sky-for-ml_slowed.mp4`).  
- Applies adaptive thresholding + contour detection.  
- Detects rectangular/box-like objects and overlays bounding boxes.  
- Displays annotated video in real-time.  

### 4. `realsim.py` – Drone Path Simulation  
- Fetches road network & computes **shortest path** between two cities.  
- Retrieves **elevation data** via Open-Elevation API.  
- Generates a **drone animation** on a Folium map with moving drone icon.  
- Plots an **elevation profile graph** of the route.

### 5. `rtlsimuint.py` – Return-to-Launch Simulation
- Uses Folium + Geopy for geocoding & mapping.
- Simulates drone flying back from start city to home city.
- Stepwise movement + altitude descent until safe landing.
- Generates animated map (`city_rtl_animation.html`) with drone path & altitude.

### 6. `satel.py` – Satellite Map Routing
- Uses OSMnx + NetworkX for city-to-city routing.
- Computes shortest route + all equal shortest paths.
- Folium maps with satellite basemap (Esri).
- Saves as `all_routes_satellite_map.html` & `shortest_route_satellite_map.html`, opens in browser.

## 🚀 Getting Started

### 🔧 Requirements
Install dependencies:
```bash
pip install osmnx networkx folium geopy pymavlink opencv-python numpy requests matplotlib folium geopy
```

## ▶️ Usage

### 1. Mapping (Shortest Routes)
```bash
python map.py
```

- Enter two city names when prompted (within 30km for faster results).

- Generates:

  - `all_routes_map.html` → shows all shortest paths.

  - `shortest_route_map.html` → highlights the single shortest path.

 ### 2. Drone Control (MAVLink)
 ```bash
python mavlink.py
```

- Connects to a drone or simulator via MAVLink (COM3, baud 115200).
- Sets GUIDED mode, arms motors, takes off to 10 meters (for testing purposes), then lands.
- ⚠️ Requires a real drone or SITL (Software-In-The-Loop) simulator

### 3. Object Detection
```bash
python objectdetection.py
```
- Reads video: `drone-in-sky-for-ml_slowed.mp4`.
- Detects and highlights objects with bounding boxes.
- Press `q` to exit the video window.

### 4. Drone Path Simulation
```bash
python realsim.py
```
- Generates drone_simulation.html with an animated drone moving along the route.
- Fetches terrain data from Open-Elevation API.
- Displays an elevation profile plot of the path.

### 5. Return to Launch Path
```bash
python rtlsimuint.py
```
- Enter a Start City and a Home City when prompted.
- The drone simulation will:
  - Take off from the start city.
  - Gradually move toward the home city.
  - Descend smoothly and land safely when close.
- Generates:
  - `city_rtl_animation.html` → interactive animated map showing the RTL flight path with altitude info.

### 6. Satellite Map Route Planner
```bash
python satel.py
```
- Enter the first city and the second city when prompted.
- The script will:
  - Download road network data.
  - Calculate the routes.
  - Generate interactive satellite maps with the routes drawn.

- Output:
  - `all_routes_satellite_map.html`
  - `shortest_route_satellite_map.html`

## 🎉 About
This code was built with passion, teamwork, and a little bit of caffeine ☕  
by **Team Bamboocopter** for the **Internal Hackathon (SIH)**.  

💡 Innovation takes flight 🚁
