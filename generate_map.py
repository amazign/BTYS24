import json
import folium
from statistics import mean

# Function to create map with bus locations
def create_map(bus_locations, output_path):
    # Calculate average latitude and longitude for centering the map
    avg_latitude = mean([bus['latitude'] for bus in bus_locations])
    avg_longitude = mean([bus['longitude'] for bus in bus_locations])

    # Create a Folium map with OpenStreetMap tiles
    bus_map = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=12, tiles='OpenStreetMap')

    # Add bus markers to the map
    for bus in bus_locations:
        folium.Marker(
            location=[bus['latitude'], bus['longitude']],
            popup=f"Bus ID: {bus['id']}",
            icon=folium.Icon(icon='bus', prefix='fa')
        ).add_to(bus_map)

    # Add a button to load new data
    bus_map.get_root().html.add_child(folium.Element(f"""
        <button onclick="updateMap()">Load New Data</button>
        <script>
            function updateMap() {{
                fetch('https://amazign.github.io/BTYS24/data/new_bus_data.json')
                    .then(response => response.json())
                    .then(data => {{
                        // Clear existing markers
                        document.querySelectorAll('.leaflet-marker-icon').forEach(el => el.remove());
                        document.querySelectorAll('.leaflet-popup').forEach(el => el.remove());

                        // Add new markers
                        data.forEach(bus => {{
                            const marker = L.marker([bus.latitude, bus.longitude])
                                .addTo(window.map)
                                .bindPopup('Bus ID: ' + bus.id);
                        }});
                    }});
            }}
        </script>
    """))

    # Save the map to an HTML file
    bus_map.save(output_path)

# Load JSON data from file
file_path = '/home/codespace/BTYS24/data/bus_location_data.json'
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"Error: The file {file_path} was not found. Make sure the file exists in the correct directory.")
    exit(1)

# Extract bus locations
bus_locations = [
    {
        'id': entity['vehicle']['trip']['trip_id'],
        'latitude': entity['vehicle']['position']['latitude'],
        'longitude': entity['vehicle']['position']['longitude']
    }
    for entity in data['entity']
]

# Create map with initial bus locations
output_path = 'index.html'
create_map(bus_locations, output_path)

print(f"Map saved to {output_path}")
