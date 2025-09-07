import math
import time
import folium
from folium.plugins import TimestampedGeoJson
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
# ----------------------------
# Helper: Haversine distance
# ----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ----------------------------
# Drone class
# ----------------------------
class SimulatedDrone:
    def __init__(self, home_lat, home_lon, start_lat, start_lon, start_alt=20.0):
        self.home_lat = home_lat
        self.home_lon = home_lon
        self.lat = start_lat
        self.lon = start_lon
        self.alt = start_alt
        self.armed = 1
        self.path = [(self.lat, self.lon, self.alt)]

    def update_position(self, step_size=5.0):
        distance = self.distance_to_home()
        dx = self.home_lat - self.lat
        dy = self.home_lon - self.lon

        if distance > 1:
            ratio = min(step_size / distance, 1)
            self.lat += dx * ratio
            self.lon += dy * ratio

        if distance < 10:
            self.alt = max(self.alt - 0.5, 0)

        if distance < 1 and self.alt <= 0.5:
            self.armed = 0

        self.path.append((self.lat, self.lon, self.alt))

    def distance_to_home(self):
        return haversine(self.lat, self.lon, self.home_lat, self.home_lon)

# ----------------------------
# Geocode cities with retry and fallback
# ----------------------------
geolocator = Nominatim(user_agent="rtl_simulator", timeout=10)

def geocode_with_retry(city, max_retries=3, fallback=None):
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(city)
            if location:
                return location.latitude, location.longitude
        except Exception as e:
            print(f"Attempt {attempt+1} to geocode '{city}' failed: {e}")
        time.sleep(2)  # wait before retry
    if fallback:
        print(f"Using fallback coordinates for {city}: {fallback}")
        return fallback
    print(f"Could not geocode '{city}'. Exiting.")
    exit()

# ----------------------------
# Input city names
# ----------------------------
start_city = input("Enter Start City: ")
home_city = input("Enter Home City: ")

# Fallback coordinates if geocoding fails
fallback_coords = {
    "Namchi": (27.3112, 88.5663),
    "Ravangla": (27.2147, 88.5615)
}

start_lat, start_lon = geocode_with_retry(start_city, fallback=fallback_coords.get(start_city))
home_lat, home_lon = geocode_with_retry(home_city, fallback=fallback_coords.get(home_city))

print(f"Start: {start_city} -> ({start_lat}, {start_lon})")
print(f"Home: {home_city} -> ({home_lat}, {home_lon})")

# ----------------------------
# Initialize drone
# ----------------------------
drone = SimulatedDrone(home_lat, home_lon, start_lat, start_lon)

# ----------------------------
# Run simulation
# ----------------------------
print("\nSimulating RTL path...")
while drone.armed:
    drone.update_position(step_size=5.0)
    distance = drone.distance_to_home()
    time.sleep(0.02)

print("Drone has returned home and landed safely.")

# ----------------------------
# Create animated map
# ----------------------------
m = folium.Map(location=[home_lat, home_lon], zoom_start=6)
folium.Marker([home_lat, home_lon], tooltip=f'Home: {home_city}', icon=folium.Icon(color='green')).add_to(m)
folium.Marker([start_lat, start_lon], tooltip=f'Start: {start_city}', icon=folium.Icon(color='orange')).add_to(m)

# Prepare TimestampedGeoJson
features = []
start_time = datetime.now()
time_increment = timedelta(seconds=1)

for i, (lat, lon, alt) in enumerate(drone.path):
    feature = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": {
            "time": (start_time + i*time_increment).isoformat(),
            "popup": f"Altitude: {alt:.1f} m",
            "icon": "circle",
            "iconstyle": {
                "fillColor": "blue",
                "fillOpacity": 0.7,
                "stroke": "true",
                "radius": 5
            }
        }
    }
    features.append(feature)

folium.plugins.TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": features
}, period='PT1S', add_last_point=True, auto_play=True, loop=False, max_speed=10).add_to(m)

map_file = 'city_rtl_animation.html'
m.save(map_file)
print(f"Animated map saved as {map_file}. Open it in your browser to see the flight.")