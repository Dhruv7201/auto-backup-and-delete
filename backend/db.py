from pymongo import MongoClient

def db_connection():
    client = MongoClient('mongodb://ethics-sftp-ui_mongodb_1:27017/')
    # client = MongoClient('mongodb://192.168.0.133:27017/')
    db = client['backup_db']
    return db
