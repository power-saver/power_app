from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["mydatabase"]

collection = db["power_usage_contract"]

distinct_cities = collection.distinct("city")

file_name = "distinct_cities.txt"

with open(file_name, "w") as file:
    for city in distinct_cities:
        file.write(city + "\n")

print("done")
