from pymongo import MongoClient
from bson import ObjectId
import os 

client = MongoClient(os.getenv("MONGOURL"))
db = client.sample_flask_mongo 
print (db)