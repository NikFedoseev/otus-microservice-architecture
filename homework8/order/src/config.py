from dotenv import load_dotenv
import os

load_dotenv()

RELOAD = os.environ.get('RELOAD') == 'True'
API_PORT = os.environ.get('API_PORT')
CONSUMER_PORT = os.environ.get('CONSUMER_PORT')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_MAX_CONNECTIONS = os.environ.get('DB_MAX_CONNECTIONS')
DC_POOL_RECYCLE = os.environ.get('DC_POOL_RECYCLE')
RABBITMQ_USER = os.environ.get('RABBITMQ_USER')
RABBITMQ_PASS = os.environ.get('RABBITMQ_PASS')
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT')
ORDER_CREATED_QUEUE = os.environ.get('ORDER_CREATED_QUEUE')
ORDER_STATE_CHANGED_QUEUE = os.environ.get('ORDER_STATE_CHANGED_QUEUE')
ORDER_CANCELLED_QUEUE = os.environ.get('ORDER_CANCELLED_QUEUE')