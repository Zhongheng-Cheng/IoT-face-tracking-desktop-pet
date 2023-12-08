import pymongo

mongo_client = pymongo.MongoClient()
db = mongo_client.testdb

cursor = db.testdb.find()
for doc in cursor:
    print(doc.items())