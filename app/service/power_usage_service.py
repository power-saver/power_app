from typing import Optional
from pymongo.collection import Collection
from pymongo import MongoClient
from .city_coordinates_service import CityCoordinateService

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "power_usage_contract"

cityCoordinateService = CityCoordinateService()

class PowerUsageService:
    def __init__(self):
        self.mongo_uri = MONGO_URI
        self.mongo_db = MONGO_DB
        self.mongo_collection = MONGO_COLLECTION
        self.collection = self._connect_to_mongodb()

    def _connect_to_mongodb(self) -> Collection:
        client = MongoClient(self.mongo_uri)
        db = client[self.mongo_db]
        return db[self.mongo_collection]

    def get_average_power_usage(self, metro: str, city: str, cntr: str, year: str, month: str) -> Optional[float]:
        
        pipeline = [
                    {
                        "$match": {
                            "city": city,
                            "metro": metro,
                            "cntr": cntr,
                            "year": year,
                            "month": month
                        }
                    },
                    {
                        "$group": {
                            "_id": None,
                            "average_power_usage": {
                                "$avg": {
                                    "$divide": ["$powerUsage", "$custCnt"]
                                }
                            }
                        }
                    }
                ]
        
        document = list(self.collection.aggregate(pipeline))[0]
        if(document is None):
            return None
        
        average_power_usage = document['average_power_usage']
        return average_power_usage

    def get_ratio(self, a: float, b: float) -> float:
        change = b - a
        ratio = (change / a) * 100
        return ratio
