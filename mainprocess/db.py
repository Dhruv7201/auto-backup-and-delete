from pymongo import MongoClient

def db_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['backup_db']
    return db