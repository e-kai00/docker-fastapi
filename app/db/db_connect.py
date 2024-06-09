from pymongo import MongoClient
import os
import env

DB_URI = os.environ["MONGODB_URI"]

def connectDB():
    client = MongoClient(DB_URI)
    db = client['DOCK-DATA-API']
    posts_collection = db['posts']
    comments_collection = db['comments']
    return client, db, posts_collection, comments_collection