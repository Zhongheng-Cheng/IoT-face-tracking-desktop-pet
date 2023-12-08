import pymongo

mongo_client = pymongo.MongoClient()
db = mongo_client.testdb

def db_get():
    cursor = db.testdb.find()
    return list(cursor)

def db_post(doc: dict):
    db.testdb.insert_one(doc)
    return

print(db_post({"name": "cccc", "age": 15}))

print(db_get())
