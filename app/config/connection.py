from pymongo import MongoClient

class MongoDBConnection:
    def __init__(self, uri, database, collection):
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.collection = self.db[collection]

    def get_collection(self):
        return self.collection
