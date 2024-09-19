import os
import logging
from utils import initialize_minio_client
from backup_process import backup_files
from delete_process import delete_files



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    client = initialize_minio_client()
    if not client:
        logging.error('Failed to initialize Minio client')
        return
    logging.info('Starting backup process')
    
    backup_flag = backup_files(client)
    if backup_flag:
        logging.info('Backup process completed')
        logging.info('Starting delete process')

    delete_flag = delete_files(client)
    if delete_flag:
        logging.info('Delete process completed')
        

if __name__ == "__main__":
    main()
