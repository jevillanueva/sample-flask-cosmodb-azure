from pymongo import MongoClient
from bson import ObjectId
import os 

client = MongoClient(os.getenv("MONGOURL"))
print (client)