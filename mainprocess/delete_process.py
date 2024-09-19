import os
import json
from db import db_connection
import logging
from datetime import datetime, timedelta



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def delete_logs():
    db = db_connection()
    collection = db["delete_logs"]

    # Calculate the date three days ago
    three_days_ago = datetime.now() - timedelta(days=15)
    print("today =", datetime.now())

    # Query the database for logs within the last three days
    logs = collection.find({"date": {"$gte": three_days_ago.strftime("%d-%b-%Y")}})

    # Keep track of seen file names and their corresponding latest dates
    seen_file_names = {}

    for log in logs:
        log_date = datetime.strptime(log["date"], "%d-%b-%Y")
        # Check if the file_name has been seen before
        if log["file_name"] in seen_file_names:
            # If the current log is newer, update the latest date
            if log_date > seen_file_names[log["file_name"]]:
                seen_file_names[log["file_name"]] = log_date
            else:
                # If the current log is older, delete it
                print('deleting', log["_id"])
                collection.delete_one({"_id": log["_id"]})
        else:
            # If the file_name is not seen, add it to the dictionary
            seen_file_names[log["file_name"]] = log_date

def backup_logs():
    db = db_connection()
    collection = db["backup_logs"]

    # Calculate the date three days ago
    three_days_ago = datetime.now() - timedelta(days=15)
    print("today =", datetime.now())

    # Query the database for logs within the last three days
    logs = collection.find({"date": {"$gte": three_days_ago.strftime("%d-%b-%Y")}})

    # Keep track of seen file names and their corresponding latest dates
    seen_file_names = {}

    for log in logs:
        log_date = datetime.strptime(log["date"], "%d-%b-%Y")
        # Check if the file_name has been seen before
        if log["file_name"] in seen_file_names:
            # If the current log is newer, update the latest date
            if log_date > seen_file_names[log["file_name"]]:
                seen_file_names[log["file_name"]] = log_date
            else:
                # If the current log is older, delete it
                print('deleting', log["_id"])
                collection.delete_one({"_id": log["_id"]})
        else:
            # If the file_name is not seen, add it to the dictionary
            seen_file_names[log["file_name"]] = log_date



def find_log(file_name):
    db = db_connection()
    collection = db["upload_logs"]
    log = collection.find_one({"file_name": file_name})
    print(log)
    return log

if __name__ == "__main__":
    delete_logs()
    backup_logs()
    # list = ['PMBJK09703_13_फरवरी_2024_07_37_41_अपराह्न.bak.gz','PMBJK09703_13_फरवरी_2024_08_43_50_अपराह्न.bak.gz']
    # delete_perticular_log(list)

