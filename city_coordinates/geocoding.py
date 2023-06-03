from geopy.geocoders import Nominatim

file_name = "./distinct_cities.txt"

with open(file_name, "r") as file:
    cities = file.readlines()
    cities = [city.strip() for city in cities]

city_data = []

geolocator = Nominatim(user_agent="my_geocoder")

for city in cities:
    location = geolocator.geocode(city)
    
    if location:
        latitude = location.latitude
        longitude = location.longitude
        
        city_info = {"city": city, "latitude": latitude, "longitude": longitude}
        city_data.append(city_info)

output_file = "city_coordinates.txt"

with open(output_file, "w") as file:
    for data in city_data:
        file.write(f"City: {data['city']}\n")
        file.write(f"Latitude: {data['latitude']}\n")
        file.write(f"Longitude: {data['longitude']}\n")
        file.write("\n")

print("done")
