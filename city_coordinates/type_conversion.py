import pandas as pd

file_path = './city_coordinates.txt'

data = []

with open(file_path, 'r') as file:
    lines = file.readlines()

for line in lines:
    if line.startswith('City:'):
        city = line.strip().split(': ')[1]
    elif line.startswith('Latitude:'):
        latitude = float(line.strip().split(': ')[1])
    elif line.startswith('Longitude:'):
        longitude = float(line.strip().split(': ')[1])
        data.append({"City": city, "Latitude": latitude, "Longitude": longitude})

df = pd.DataFrame(data)

df.to_json('city_coordinates.json', orient='records', force_ascii=False)