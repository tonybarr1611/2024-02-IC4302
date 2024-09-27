import os
import sys
import csv
import time
import pika
import boto3
import mariadb
import logging
import requests
import datetime
from io import StringIO
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from prometheus_client import Counter, Histogram, start_http_server

XPATH=os.getenv('XPATH')
DATA=os.getenv('DATAFROMK8S')

RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITMQ_PASS')
QUEUE_NAME=os.getenv('RABBITMQ_QUEUE')

MARIADB_USER = os.getenv('MARIADB_USER')
MARIADB_PASS = os.getenv('MARIADB_PASS')
MARIADB = os.getenv('MARIADB')
MARIADB_DB = os.getenv('MARIADB_DB')
MARIADB_TABLE = os.getenv('MARIADB_TABLE')

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY_PREFIX = os.getenv('S3_KEY_PREFIX')

ELASTIC_URL = os.getenv('ELASTIC')
ELASTIC_USER = os.getenv('ELASTIC_USER')
ELASTIC_PASS = os.getenv('ELASTIC_PASS')
ELASTIC_INDEX_NAME = os.getenv('ELASTIC_INDEX_NAME')

HUGGING_FACE_API = os.getenv('HUGGING_FACE_API')



object_processing_time = Histogram('object_processing_time_seconds', 'Time taken to process an object', buckets=[0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 5, 10, 30, 60, 120, 300])

row_processing_time = Histogram('row_processing_time_seconds', 'Time taken to process a row', buckets=[0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 5, 10, 30, 60, 120, 300])


objects_processed = Counter('objects_processed', 'Cantidad de objetos procesados')
rows_processed = Counter('rows_processed', 'Cantidad de filas procesados')
rows_error = Counter('rows_error', 'Cantidad de filas con error')

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("application.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# S3 client
def create_s3_client():
    try:
        if AWS_ACCESS_KEY and AWS_SECRET_ACCESS_KEY:
            client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
            logger.info("S3 client configured")
            return client
        else:
            logger.error("AWS credentials not provided")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error creating S3 client: {e}")
        sys.exit(1)

s3_client = create_s3_client()

def find_object(bucket_name, file_name, prefix=''):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith(file_name):
                    logger.info(f"File {file_name} found in bucket {bucket_name}")
                    logger.info(f"Key: {obj['Key']}")
                    return obj['Key']
        logger.warning('File not found')
        return None
    except Exception as e:
        logger.error(f"Error finding object: {e}")
        sys.exit(1)

def read_csv_from_s3(bucket_name, file_key):
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        csv_content = response['Body'].read().decode('utf-8')
        csv_reader = csv.reader(StringIO(csv_content))

        return [row for row in csv_reader]
    except Exception as e:
        logger.error(f"Error reading CSV from S3: {e}")
        sys.exit(1)

# CSV 

def process_csv_file(bucket_name, file_name, prefix=''):
    try:
        file_key = find_object(bucket_name, file_name, prefix)
        logger.info(f"Processing file {file_name} from bucket {bucket_name} with key {file_key}")
        if file_key:
            csv_data = read_csv_from_s3(bucket_name, file_key)
            return csv_data
        else:
            logger.error(f"File {file_name} not found in bucket {bucket_name} with prefix {prefix}.")
            return []
    except Exception as e:
        logger.error(f"Error reading CSV from S3: {e}")
        return []
    
# MariaDB

def create_connection_pool():
    pool = mariadb.ConnectionPool(
        host=MARIADB,
        port=3306,
        user=MARIADB_USER,
        password=MARIADB_PASS,
        database=MARIADB_DB,
        pool_name="job_pool",
        pool_size=10  
    )
    return pool

pool = create_connection_pool()

def execute_query(query, params=None):
    conn = None
    try:
        conn = pool.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            conn.commit()
    except mariadb.Error as e:
        logger.error(f"Error executing query: {e}")
    finally:
        if conn:
            conn.close()

def object_processed(key):
    query = "SELECT object_key FROM processed_objects WHERE object_key = %s"
    results = execute_query(query, [key])

    if results: return True 
    else: return False

def mark_object_processed(key):
    query = "INSERT INTO processed_objects (object_key, processed_at) VALUES (%s, %s) "
    execute_query(query, [key, datetime.datetime.now()])

# Embeddings
    
def get_embeddings(text):
    try:
        response = requests.post(f"{HUGGING_FACE_API}encode", json={'text': text})
        if response.status_code == 200:
            return response.json()['embedding']
    except Exception as e:
        logger.error(f"Error getting embeddings: {e}")
        return None
    
# Elasticsearch

elastic_client = None
try:
    elastic_client = Elasticsearch(
        [ELASTIC_URL], 
        basic_auth=(ELASTIC_USER, ELASTIC_PASS)  
    )
except Exception as e:
    logger.error(f"Error connecting to Elasticsearch: {e}")
    exit(1)

def create_index_if_not_exists():
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "text"},
                "title": {"type": "text"},
                "artist": {"type": "text"},
                "lyrics": {"type": "text"},
                "embeddings": {
                    "type": "dense_vector",
                    "dims": 768
                }
            }
        }
    }
    if not elastic_client.indices.exists(index=ELASTIC_INDEX_NAME):
        elastic_client.indices.create(index=ELASTIC_INDEX_NAME, body=mapping)
        logger.info(f"Index '{ELASTIC_INDEX_NAME}' created successfully.")
    else:
        logger.warning(f"Index '{ELASTIC_INDEX_NAME}' already exists.")

create_index_if_not_exists()

def store_embedding(id, title, artist, lyrics, embeddings):
    document = {
        "id": id,
        "title": title,
        "artist": artist,
        "lyrics": lyrics,
        "embeddings": embeddings
    }
    response = elastic_client.index(index=ELASTIC_INDEX_NAME, document=document)
    
    return response

def callback(ch, method, properties, body):
    key = body.decode('utf-8')
    logger.info(f"Received job {key}")
    
    if not object_processed(key):
        with object_processing_time.time():
            songsList = process_csv_file(S3_BUCKET, key, S3_KEY_PREFIX)

        for song in songsList[1:]:
            with row_processing_time.time():
                embedding = get_embeddings(song[16])
                logger.info(f"Song id: {song[0]} read.")
                store_embedding(song[0], song[1], song[3], song[16], embedding)
                rows_processed.inc()

        mark_object_processed(key)
        objects_processed.inc()
        logger.info(f"{key} processed")
    else:
        logger.info(f"{key} already processed")


start_http_server(8000)
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body='part-00075-77fbec1f-53bd-48e0-9790-c733ee82f211-c000.csv')
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()