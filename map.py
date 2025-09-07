import osmnx as ox
import networkx as nx
import folium
from folium import PolyLine
import geopy.distance

def get_city_coordinates(city_name):
    try:
        lat, lon = ox.geocode(city_name + ", India")
        return lat, lon
    except Exception as e:
        print(f"Error: Could not geocode {city_name}. Check spelling.")
        exit()

def create_google_style_map(city1, city2, buffer_km=20):
    # Get coordinates
    lat1, lon1 = get_city_coordinates(city1)
    lat2, lon2 = get_city_coordinates(city2)

    # Midpoint for map centering
    mid_lat = (lat1 + lat2)/2
    mid_lon = (lon1 + lon2)/2

    # Estimate distance between cities to set graph radius
    dist = geopy.distance.distance((lat1, lon1), (lat2, lon2)).km
    radius = max(dist/2 + buffer_km, buffer_km)

    # Download road network
    print("Downloading road network data...")
    G = ox.graph_from_point((mid_lat, mid_lon), dist=radius*1000, network_type='drive')

    # Nearest nodes
    orig_node = ox.distance.nearest_nodes(G, X=lon1, Y=lat1)
    dest_node = ox.distance.nearest_nodes(G, X=lon2, Y=lat2)

    # --- Shortest path ---
    shortest_route = nx.shortest_path(G, orig_node, dest_node, weight='length')

    # --- All paths (all shortest paths of same distance) ---
    all_routes = list(nx.all_shortest_paths(G, orig_node, dest_node, weight='length'))

    # --- Create Folium map ---
    fmap_all = folium.Map(location=[mid_lat, mid_lon], zoom_start=10, tiles='OpenStreetMap')
    fmap_shortest = folium.Map(location=[mid_lat, mid_lon], zoom_start=10, tiles='OpenStreetMap')

    # Add city markers
    folium.Marker([lat1, lon1], popup=city1, icon=folium.Icon(color='green')).add_to(fmap_all)
    folium.Marker([lat2, lon2], popup=city2, icon=folium.Icon(color='red')).add_to(fmap_all)
    folium.Marker([lat1, lon1], popup=city1, icon=folium.Icon(color='green')).add_to(fmap_shortest)
    folium.Marker([lat2, lon2], popup=city2, icon=folium.Icon(color='red')).add_to(fmap_shortest)

    # --- Draw all shortest paths (blue) ---
    for route in all_routes:
        route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route]
        PolyLine(route_coords, color='blue', weight=3, opacity=0.7).add_to(fmap_all)

    # --- Draw shortest route (red) ---
    route_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in shortest_route]
    PolyLine(route_coords, color='red', weight=5, opacity=1).add_to(fmap_shortest)

    # Save maps
    fmap_all.save("all_routes_map.html")
    fmap_shortest.save("shortest_route_map.html")
    print("Maps saved as 'all_routes_map.html' and 'shortest_route_map.html'")

if __name__ == "__main__":
    city1 = input("Enter first city: ")
    city2 = input("Enter second city: ")
    create_google_style_map(city1, city2)
