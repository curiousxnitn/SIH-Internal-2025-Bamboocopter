import osmnx as ox
import networkx as nx
import folium
from folium.plugins import AntPath
import webbrowser
import os
import requests
import matplotlib.pyplot as plt
import json

def get_elevations(coords):
    """Fetch elevation data from Open-Elevation API"""
    elevations = []
    url = "https://api.open-elevation.com/api/v1/lookup"
    batch_size = 50
    for i in range(0, len(coords), batch_size):
        batch = coords[i:i+batch_size]
        locations = [{"latitude": lat, "longitude": lon} for lat, lon in batch]
        try:
            response = requests.post(url, json={"locations": locations}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                batch_elevs = [res["elevation"] for res in data["results"]]
                elevations.extend(batch_elevs)
            else:
                elevations.extend([0]*len(batch))
        except requests.exceptions.RequestException:
            elevations.extend([0]*len(batch))
    return elevations

def drone_path_simulation(start_city, end_city, buffer_dist=7000):
    print("📥 Downloading road network data...")

    # Get coordinates of cities
    start_point = ox.geocode(start_city + ", India")
    end_point = ox.geocode(end_city + ", India")

    # Midpoint graph for small towns
    mid_lat = (start_point[0] + end_point[0]) / 2
    mid_lon = (start_point[1] + end_point[1]) / 2
    G = ox.graph_from_point((mid_lat, mid_lon), dist=buffer_dist, network_type="drive")

    # Nearest nodes
    orig_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
    dest_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

    # Shortest path
    shortest_route = nx.shortest_path(G, orig_node, dest_node, weight="length")
    route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_route]

    # Elevation data
    print("📈 Fetching elevation data from Open-Elevation...")
    elevations = get_elevations(route_coords)

    # --- MAP ---
    m = folium.Map(location=start_point, zoom_start=13, tiles="OpenStreetMap")

    # Animated route line
    AntPath(route_coords, color="blue", weight=5, delay=1000).add_to(m)

    # Start & end markers
    folium.Marker(start_point, tooltip="Start: " + start_city, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(end_point, tooltip="End: " + end_city, icon=folium.Icon(color="red")).add_to(m)

    # --- Drone icon animation ---
    # You can replace this URL with any small drone PNG
    drone_icon_url = "https://cdn-icons-png.flaticon.com/512/744/744467.png"

    latlngs_json = json.dumps(route_coords)
    js = f"""
        var latlngs = {latlngs_json};
        var droneIcon = L.icon({{
            iconUrl: '{drone_icon_url}',
            iconSize: [32, 32],
            iconAnchor: [16, 16]
        }});
        var marker = L.marker(latlngs[0], {{icon: droneIcon}}).addTo(map);
        var i = 0;
        var speed = 50; // ms per step
        function moveDrone() {{
            if (i < latlngs.length - 1) {{
                var start = latlngs[i];
                var end = latlngs[i+1];
                var steps = 10;
                var step = 0;
                function interpolate() {{
                    var lat = start[0] + (end[0]-start[0]) * step/steps;
                    var lon = start[1] + (end[1]-start[1]) * step/steps;
                    marker.setLatLng([lat, lon]);
                    step++;
                    if (step <= steps) {{
                        setTimeout(interpolate, speed);
                    }} else {{
                        i++;
                        moveDrone();
                    }}
                }}
                interpolate();
            }}
        }}
        moveDrone();
    """
    m.get_root().script.add_child(folium.Element(js))

    # Save and open map
    file_path = "drone_simulation.html"
    m.save(file_path)
    webbrowser.open("file://" + os.path.realpath(file_path))
    print(f"✅ Drone simulation saved as {file_path}")

    # --- Elevation profile plot ---
    plt.figure(figsize=(10, 4))
    plt.plot(range(len(elevations)), elevations, color="brown", linewidth=2)
    plt.fill_between(range(len(elevations)), elevations, color="tan", alpha=0.5)
    plt.title(f"Terrain Elevation Profile: {start_city} → {end_city}")
    plt.xlabel("Path Point Index")
    plt.ylabel("Elevation (m)")
    plt.grid(True, alpha=0.3)
    plt.show()

start_city = input("Enter city 1: ")
end_city = input("Enter city 2: ")
drone_path_simulation(start_city, end_city)
