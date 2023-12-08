import pymongo

class DataService(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient()
        self.db = mongo_client.testdb
        self.collection = self.db.testdb

    def db_get(self, query=None):
        if query:
            cursor = self.collection.find(query)
        else:
            cursor = self.collection.find()
        return list(cursor)

    def db_post(self, doc: dict):
        self.collection.insert_one(doc)
        return