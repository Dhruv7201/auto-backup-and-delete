from minio import Minio
import os
import logging
from dotenv import load_dotenv
from colorama import init, Fore, Style
import urllib3


load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Initialize colorama
init(autoreset=True)




def initialize_minio_client():
    endpoint = os.getenv("MINIO_ENDPOINT")
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    bucket_name = os.getenv("BUCKET_NAME")
    bucket_path = os.getenv("BUCKET_PATH")

    # Initialize Minio client
    client = Minio(
        endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=True,

    )
    pool_manager = urllib3.PoolManager(timeout=1800,maxsize=10)
    client._http = pool_manager


        
    return client
