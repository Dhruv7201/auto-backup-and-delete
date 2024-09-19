from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from db import db_connection

router = APIRouter()


@router.get('/')
async def index():
    db = db_connection()
    collection = db['backup_logs']
    dl_collection = db['delete_logs']
    logs = collection.find({})
    delete_logs = dl_collection.find({})
    
    store_code_data = {}
    
    for log in logs:
        store_code = log['store_code']
        if store_code not in store_code_data:
            if store_code == 'RGJAHM9999':
                continue
            # logic for flag
            if log['status'] == 'uploaded':
                store_code_data[store_code] = {
                    'total_size': log['size'],
                    'total_bucket_files': 1,
                    'last_backup_date': log['date'],
                    'last_backup_time': log['time'],
                    'flag': 'success'
                }
            elif log['status'] in ['already exists', 'not deleted']:
                store_code_data[store_code] = {
                    'total_size': log['size'],
                    'total_bucket_files': 1,
                    'last_backup_date': log['date'],
                    'last_backup_time': log['time'],
                    'flag': 'warning'
                }
            else:
                store_code_data[store_code] = {
                    'total_size': log['size'],
                    'total_bucket_files': 1,
                    'last_backup_date': log['date'],
                    'last_backup_time': log['time'],
                    'flag': 'danger'
                }
        else:
            # logic for flag
            store_code_data[store_code]['total_size'] += log['size']
            store_code_data[store_code]['total_bucket_files'] += 1
            store_code_data[store_code]['last_backup_date'] = max(
                store_code_data[store_code]['last_backup_date'],
                log['date']
            )
            # get the time of max of last backup date
            if store_code_data[store_code]['last_backup_date'] == log['date']:
                store_code_data[store_code]['last_backup_time'] = log['time']
            if log['status'] == 'uploaded':
                continue
            elif log['status'] in ['already exists', 'not deleted']:
                if store_code_data[store_code]['flag'] != 'warning':
                    store_code_data[store_code]['flag'] = 'warning'
            else:
                if store_code_data[store_code]['flag'] != 'danger':
                    store_code_data[store_code]['flag'] = 'danger'
    for delete_log in delete_logs:
        store_code = delete_log['store_code']
        if store_code in store_code_data:
            store_code_data[store_code]['last_deleted_date'] = delete_log['date']
            if delete_log['status'] == 'deleted':
                store_code_data[store_code]['total_size'] -= delete_log['size']
                store_code_data[store_code]['total_bucket_files'] -= 1
                if store_code_data[store_code]['flag'] == 'success':
                    continue
            elif delete_log['status'] == 'not deleted':
                if store_code_data[store_code]['flag'] != 'warning':
                    store_code_data[store_code]['flag'] = 'warning'
            else:
                if store_code_data[store_code]['flag'] != 'danger':
                    print(delete_log)
                    store_code_data[store_code]['flag'] = 'danger'

    for store_code in store_code_data:
        if store_code_data[store_code]['total_size'] < 1024:
            store_code_data[store_code]['total_size'] = round(
                store_code_data[store_code]['total_size'] / 1024 / 1024, 2
            )
        else:
            store_code_data[store_code]['total_size'] = round(
                store_code_data[store_code]['total_size'] / 1024 / 1024 / 1024, 2
            )
    print(store_code_data)
    return JSONResponse(store_code_data)



@router.get('/store-code')
async def store_code_index(store_code: str = Query(...)):
    db = db_connection()
    bl_collection = db['backup_logs']
    dl_collection = db['delete_logs']
    backup_logs = bl_collection.find({'store_code': store_code})
    delete_logs = dl_collection.find({'store_code': store_code})
    store_code_data = []
    for log in backup_logs:
        store_code_data.append({
            'file_name': log['file_name'],
            'store_code': log['store_code'],
            'size': log['size'],
            'date': log['date'],
            'time': log['time'],
            'status': log['status']
        })

    for log in delete_logs:
        store_code_data.append({
            'file_name': log['file_name'],
            'store_code': log['store_code'],
            'size': log['size'],
            'date': log['date'],
            'time': log['time'],
            'status': log['status']
        })

    # convert size to MB
    for log in store_code_data:
        log['size'] = round(log['size'] / 1024 / 1024, 2)
        log['size'] = str(log['size']) + ' MB'
    return JSONResponse(content=store_code_data)
