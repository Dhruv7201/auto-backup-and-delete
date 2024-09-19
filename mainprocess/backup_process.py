import os
import logging
from datetime import datetime, timedelta
import minio
import time
from db import db_connection



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def backup_files(client):
    bucket_name = os.getenv("BUCKET_NAME")
    bucket_path = os.getenv("BUCKET_PATH")
    local_path = os.getenv("BACKUP_DIR")
    local_path = os.path.abspath(local_path)

    objects = client.list_objects(bucket_name, prefix=bucket_path, recursive=True)
    db = db_connection()
    collection = db['backup_logs']

    bucket_files = {}
    files = {}
    for obj in objects:
        bucket_files[obj.object_name] = {
            'name': obj.object_name.split('/')[-1],
            'dir': obj.object_name.split('/')[-2],
            'path': obj.object_name,
            'size': obj.size,
        }
    # get local files names from folder local_path/folders/files
    for r, dir, f in os.walk(local_path):
        # ignore __pycache__ folder
        if '__pycache__' in dir:
            dir.remove('__pycache__')
        for d in dir:
            for file in os.listdir(f'{r}/{d}'):
                # take list of files that are any time before two hours if file size is more than 1gb
                if datetime.now() - timedelta(hours=2) >= datetime.fromtimestamp(os.path.getmtime(f'{r}/{d}/{file}')) and os.path.getsize(f'{r}/{d}/{file}') > 1073741824:
                    files[file] = {
                        'path': f'{r}/{d}/{file}',
                        'dir': d,
                        'name': file,
                        'size': os.path.getsize(f'{r}/{d}/{file}'),
                    }
                # take list of files that are any time before one hours if file size is less than 1gb
                elif datetime.now() - timedelta(hours=1) >= datetime.fromtimestamp(os.path.getmtime(f'{r}/{d}/{file}')) and os.path.getsize(f'{r}/{d}/{file}') < 1073741824:
                    files[file] = {
                        'path': f'{r}/{d}/{file}',
                        'dir': d,
                        'name': file,
                        'size': os.path.getsize(f'{r}/{d}/{file}'),
                    }
                else:
                    logging.info(f'{file} is not old enough to backup')
    # compare local files with bucket files
    for file in files:
        if bucket_files:
            # if file exist
            if os.path.exists(files[file]['path']):
                # if file is not in bucket
                if not any(files[file]['name'] == bucket_file['name'] for bucket_file in bucket_files.values()):
                    logging.info(f'Uploading {files[file]["name"]} to bucket')
                    client.fput_object(bucket_name, f'{bucket_path}/{files[file]["dir"]}/{files[file]["name"]}', files[file]['path'])
                    time.sleep(1)
                    collection.insert_one({
                        'file_name': files[file]['name'],
                        'store_code': files[file]['name'].split('_')[0],
                        'size': files[file]['size'],
                        'date': datetime.now().strftime('%d-%b-%Y'),
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'status': 'uploaded'
                    })
                    try:
                        os.remove(files[file]['path'])
                    except Exception as e:
                        logging.error(f'Error deleting file {files[file]["name"]}: {e}')
                else:
                    logging.info(f'{files[file]["name"]} already exists in bucket')
                    collection.insert_one({
                        'file_name': files[file]['name'],
                        'store_code': files[file]['name'].split('_')[0],
                        'size': files[file]['size'],
                        'date': datetime.now().strftime('%d-%b-%Y'),
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'status': 'already exists'
                    })
                    try:
                        os.remove(files[file]['path'])
                    except Exception as e:
                        logging.error(f'Error deleting file {files[file]["name"]}: {e}')
            else:
                logging.info(f'{files[file]["name"]} does not exist')
        else:
            logging.info(f'Uploading {files[file]["name"]} to bucket')
            client.fput_object(bucket_name, f'{bucket_path}/{files[file]["dir"]}/{files[file]["name"]}', files[file]['path'])
            collection.insert_one({
                'file_name': files[file]['name'],
                'store_code': files[file]['name'].split('_')[0],
                'size': files[file]['size'],
                'date': datetime.now().strftime('%d-%b-%Y'),
                'time': datetime.now().strftime('%H:%M:%S'),
                'status': 'uploaded'
            })
            os.remove(files[file]['path'])
    return True
