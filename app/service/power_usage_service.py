from typing import Optional
from pymongo.collection import Collection
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "mydatabase"
MONGO_COLLECTION = "power_usage_contract"

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
        document = self.collection.find_one({
            'metro': metro,
            'city': city,
            'cntr': cntr,
            'year': year,
            'month': month
        })
        if document:
            power_usage = document['powerUsage']
            cust_count = document['custCnt']
            average_power_usage = power_usage / cust_count
            return average_power_usage
        else:
            return None

    @staticmethod
    def get_ratio(a: float, b: float) -> float:
        change = b - a
        ratio = (change / a) * 100
        return ratio
