import os
import json
import logging
from colorama import init, Fore, Style
from datetime import datetime, timedelta
from delete_log import delete_logs
from db import db_connection


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Initialize colorama
init(autoreset=True)


def parse_date(date_str, file_name):
    date_formats = ["%d_%b_%Y", "%d_%m_%Y"]
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            logging.error(f"Invalid date format: {date_str} in file {file_name}")
            pass


def delete_files(client):
    bucket_name = os.getenv("BUCKET_NAME")
    bucket_path = os.getenv("BUCKET_PATH")
    zee_max_files = int(os.getenv("ZEE_MAX_FILES"))
    zota_max_files = int(os.getenv("ZOTA_MAX_FILES"))
    pmbi_max_files = int(os.getenv("PMBI_MAX_FILES"))
    gujco_max_files = int(os.getenv("GUJCO_MAX_FILES"))
    kendri_max_files = int(os.getenv("KENDRI_MAX_FILES"))

    # delete duplicate logs
    delete_logs()

    delete_repeating(client, bucket_name, bucket_path)
    db = db_connection()
    collection = db["delete_logs"]
    unique_store_code = get_unique_store_code(client, bucket_name, bucket_path)
    # For each store code
    for store_code, files in unique_store_code.items():
        # If store code has files
        if files:
            # Get FSize as the size of the latest date file to compare with other files after the 15th file
            FSize = files[0]["size"]
            if files[0]["dir"] == "zeel":
                if len(files) > zee_max_files:
                    # Take all files after the 15th file (start index from 14)
                    for file in files[zee_max_files:]:
                        # If the file size is less than FSize, delete the file
                        if FSize > file["size"]:
                            logging.warn(
                                f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                            # Delete file from the bucket
                            client.remove_object(bucket_name, file["path"])
                            collection.insert_one(
                                {
                                    "file_name": file["name"],
                                    "store_code": store_code,
                                    "size": file["size"],
                                    "date": datetime.now().strftime("%d-%b-%Y"),
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "status": "deleted",
                                }
                            )
                        else:
                            # If the file size is not greater than FSize, it might be corrupted, keep it
                            logging.info(f'Not deleting {file["name"]} from bucket')
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                else:
                    # no need to delete any thing in store code
                    pass
            if files[0]["dir"] == "zota":
                if len(files) > zota_max_files:
                    # Take all files after the 15th file (start index from 14)
                    for file in files[zota_max_files:]:
                        # If the file size is less than FSize, delete the file
                        if FSize > file["size"]:
                            logging.warn(
                                f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                            collection.insert_one(
                                {
                                    "file_name": file["name"],
                                    "store_code": store_code,
                                    "size": file["size"],
                                    "date": datetime.now().strftime("%d-%b-%Y"),
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "status": "deleted",
                                }
                            )
                            # Delete file from the bucket
                            client.remove_object(bucket_name, file["path"])
                        else:
                            # If the file size is not greater than FSize, it might be corrupted, keep it
                            logging.info(f'Not deleting {file["name"]} from bucket')
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                else:
                    # no need to delete any thing in store code
                    pass
            if files[0]["dir"] == "pmbi":
                if len(files) > pmbi_max_files:
                    # Take all files after the 15th file (start index from 14)
                    for file in files[pmbi_max_files:]:
                        # If the file size is less than FSize, delete the file
                        if FSize > file["size"]:
                            logging.warn(
                                f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                            collection.insert_one(
                                {
                                    "file_name": file["name"],
                                    "store_code": store_code,
                                    "size": file["size"],
                                    "date": datetime.now().strftime("%d-%b-%Y"),
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "status": "deleted",
                                }
                            )
                            # Delete file from the bucket
                            client.remove_object(bucket_name, file["path"])
                        else:
                            # If the file size is not greater than FSize, it might be corrupted, keep it
                            logging.info(f'Not deleting {file["name"]} from bucket')
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                else:
                    # no need to delete any thing in store code
                    pass
            if files[0]["dir"] == "gujco":
                if len(files) > gujco_max_files:
                    # Take all files after the 15th file (start index from 14)
                    for file in files[gujco_max_files:]:
                        # If the file size is less than FSize, delete the file
                        if FSize > file["size"]:
                            logging.warn(
                                f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                            collection.insert_one(
                                {
                                    "file_name": file["name"],
                                    "store_code": store_code,
                                    "size": file["size"],
                                    "date": datetime.now().strftime("%d-%b-%Y"),
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "status": "deleted",
                                }
                            )
                            # Delete file from the bucket
                            client.remove_object(bucket_name, file["path"])
                        else:
                            # If the file size is not greater than FSize, it might be corrupted, keep it
                            logging.info(f'Not deleting {file["name"]} from bucket')
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                else:
                    # no need to delete any thing in store code
                    pass
            if files[0]["dir"] == "kendri":
                if len(files) > kendri_max_files:
                    # Take all files after the 15th file (start index from 14)
                    for file in files[kendri_max_files:]:
                        # If the file size is less than FSize, delete the file
                        if FSize > file["size"]:
                            logging.warn(
                                f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                            # Delete file from the bucket
                            client.remove_object(bucket_name, file["path"])
                            collection.insert_one(
                                {
                                    "file_name": file["name"],
                                    "store_code": store_code,
                                    "size": file["size"],
                                    "date": datetime.now().strftime("%d-%b-%Y"),
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "status": "deleted",
                                }
                            )
                        else:
                            # If the file size is not greater than FSize, it might be corrupted, keep it
                            logging.info(f'Not deleting {file["name"]} from bucket')
                            logging.info(
                                f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                            )
                            logging.info(
                                f'{Fore.GREEN}Size of {files[0]["name"]} is {files[0]["size"]}{Style.RESET_ALL}'
                            )
                else:
                    # no need to delete any thing in store code
                    pass
        else:
            logging.info(f'Known Directory {file[0]["dir"]}')
            collection.insert_one(
                {
                    "file_name": file["name"],
                    "store_code": store_code,
                    "size": file["size"],
                    "date": datetime.now().strftime("%d-%b-%Y"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "status": "not deleted",
                }
            )

    return True


def delete_repeating(client, bucket_name, bucket_path):
    unique_store_code = get_unique_store_code(client, bucket_name, bucket_path)
    db = db_connection()
    collection = db["delete_logs"]
    same_date_files = {}
    processed_store_code = set()

    for store_code, files in unique_store_code.items():
        if store_code not in processed_store_code:
            processed_store_code.add(store_code)
            same_date_files[store_code] = {}
            for file in files:
                if file["date"] not in same_date_files[store_code]:
                    same_date_files[store_code][file["date"]] = []
                same_date_files[store_code][file["date"]].append(file)
    for store_code, files in same_date_files.items():
        for date, files in files.items():
            if len(files) > 1:
                for file in files[:-1]:
                    if file["size"] < files[-1]["size"]:
                        if file == files[-1]:
                            continue
                        logging.warn(
                            f'{Fore.RED}Deleting {file["name"]} from bucket{Style.RESET_ALL}'
                        )
                        logging.info(
                            f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                        )
                        logging.info(
                            f'{Fore.GREEN}Size of {files[-1]["name"]} is {files[-1]["size"]}{Style.RESET_ALL}'
                        )
                        # Delete file from the bucket
                        client.remove_object(bucket_name, file["path"])
                        collection.insert_one(
                            {
                                "file_name": file["name"],
                                "store_code": store_code,
                                "size": file["size"],
                                "date": datetime.now().strftime("%d-%b-%Y"),
                                "time": datetime.now().strftime("%H:%M:%S"),
                                "status": "deleted",
                            }
                        )
                        if file in files:
                            files.remove(file)
                    else:
                        if files[-1] == file:
                            continue
                        logging.warn(
                            f'{Fore.RED}Deleting {files[-1]["name"]} from bucket{Style.RESET_ALL}'
                        )
                        logging.info(
                            f'{Fore.GREEN}Size of {files[-1]["name"]} is {files[-1]["size"]}{Style.RESET_ALL}'
                        )
                        logging.info(
                            f'{Fore.GREEN}Size of {file["name"]} is {file["size"]}{Style.RESET_ALL}'
                        )
                        # Delete file from the bucket
                        client.remove_object(bucket_name, files[-1]["path"])
                        collection.insert_one(
                            {
                                "file_name": files[-1]["name"],
                                "store_code": store_code,
                                "size": files[-1]["size"],
                                "date": datetime.now().strftime("%d-%b-%Y"),
                                "time": datetime.now().strftime("%H:%M:%S"),
                                "status": "deleted",
                            }
                        )
                        if files[-1] in files:
                            files.remove(files[-1])
            else:
                pass
    return True


def get_unique_store_code(client, bucket_name, bucket_path):
    objects = client.list_objects(bucket_name, prefix=bucket_path, recursive=True)

    # to store all unique store codes for all files in the bucket
    unique_store_code = {}

    for obj in objects:
        store_code = obj.object_name.split("/")[-1].split("_")[0]

        if store_code not in unique_store_code:
            unique_store_code[store_code] = []

        unique_store_code[store_code].append(
            {
                "name": obj.object_name.split("/")[-1],
                "dir": obj.object_name.split("/")[-2],
                "date": obj.last_modified.strftime("%d_%b_%Y"),
                "time": obj.last_modified.strftime("%H_%M_%S"),
                "path": obj.object_name,
                "size": obj.size,
            }
        )

    # Sort each store_code by date
    for store_code in unique_store_code:
        unique_store_code[store_code] = sorted(
            unique_store_code[store_code],
            key=lambda k: parse_date(k["date"], k["name"]),
            reverse=True,
        )

    with open("unique_store_code.json", "w") as f:
        json.dump(unique_store_code, f, indent=4)
    return unique_store_code
