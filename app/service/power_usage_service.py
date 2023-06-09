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

    def get_neighbor_city_power_usage_list(self, metro: str, city: str, cntr: str, year: str, month: str) -> Optional[float]:
        nearest_city_list = cityCoordinateService.get_nearest_cities(city)
        nearest_city_list.append(city)
        pipeline = [
            {
                '$match': {
                    'city': {'$in': nearest_city_list},
                    'metro': metro,
                    'cntr': cntr,
                    'year': year,
                    'month': month
                }
            },
            {
                '$group': {
                    '_id': "$city",
                    'averagePowerUsage': {
                        '$avg': {'$divide': ['$powerUsage', '$custCnt']}
                    }
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'name': '$_id',
                    'averagePowerUsage': 1
                }
            }
        ]
        
        document = list(self.collection.aggregate(pipeline))

        return document

    def get_top_city_power_usage_list(self, cntr: str, year: str, month: str):
        
        pipeline = [
            {
                '$match': {
                'cntr': cntr,
                'month': month,
                'year': year
                }
            },
            {
                '$addFields': {
                'powerUsagePerCust': {
                '$divide': ['$powerUsage', '$custCnt']
                }
            }
            },
            {
            '$group': {
                '_id': {'metro': '$metro', 'city': '$city'},
                'averagePowerUsage': {'$avg': '$powerUsagePerCust'}
                }
            },
            {
            '$project': {
                '_id': 0,
                'name': { '$concat': ['$_id.metro',' ','$_id.city'] },
                'averagePowerUsage': 1
                }
            },
            {
                '$sort': {'averagePowerUsage': -1}
            },
            {
                '$limit': 5
            }
        ]

        document = list(self.collection.aggregate(pipeline))
        return document

    def get_power_by_cntr(self, metro: str, city:str, year: str, month: str):
            
        pipeline = [
            {
                '$match': {
                    'metro': metro,
                    'city' : city,
                    'month': month,
                    'year': year
                }
            },
            {
                '$addFields': {
                'powerUsagePerCust': {
                '$divide': ['$powerUsage', '$custCnt']
                }
            }
            },
            {
            '$group': {
                '_id': {'cntr': '$cntr'},
                'averagePowerUsage': {'$avg': '$powerUsagePerCust'}
                }
            },
            {
            '$project': {
                '_id': 0,
                'name': '$_id.cntr',
                'averagePowerUsage': 1
                }
            }
        ]    
        document = list(self.collection.aggregate(pipeline))
        return document
        
    def get_ratio(self, a: float, b: float) -> float:
        change = b - a
        ratio = (change / a) * 100
        return ratio