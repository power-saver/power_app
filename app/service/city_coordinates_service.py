from typing import Optional
from pymongo.collection import Collection
from pymongo import MongoClient
import math

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "city_coordinates"


class CityCoordinateService:
    def __init__(self):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.mongo_collection = MONGO_COLLECTION
        self.collection = self._connect_to_mongodb()

    def _connect_to_mongodb(self) -> Collection:
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        return db[self.mongo_collection]

    def get_nearest_cities(self, target_city: str):

        distances = []

        nearest_cities = list(self.collection.find(
            {
                "City": {"$ne": target_city}
            }
        ))
        target_city =  list(self.collection.find(
            {
              "City": target_city 
            }
        ))[0]
        
        for city in nearest_cities:
            city_lat = city['Latitude']
            city_lon = city['Longitude']
            distance = self.calculate_distance(target_city['Latitude'], target_city['Longitude'], city_lat, city_lon)
            distances.append((city["City"], distance))
    
         # 거리를 기준으로 오름차순 정렬
        distances.sort(key=lambda x: x[1])
    
          # 최단거리의 도시 추출
        nearest_cities = [city[0] for city in distances[:5]]
        return nearest_cities


    def calculate_distance(self,lat1, lon1, lat2, lon2):
    # 위도 및 경도를 라디안 단위로 변환
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # 경도 및 위도의 차이 계산
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # 구면 코사인 법칙을 사용하여 거리 계산
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6371 * c  # 지구 반경 6371km 사용

        return distance