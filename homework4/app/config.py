from dotenv import load_dotenv
import os

load_dotenv()

RELOAD = os.environ.get('RELOAD') == 'True'

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_MAX_CONNECTIONS = os.environ.get('DB_MAX_CONNECTIONS')
DC_POOL_RECYCLE = os.environ.get('DC_POOL_RECYCLE')
