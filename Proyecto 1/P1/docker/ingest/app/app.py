import os
import sys
import csv
import pika
import boto3
import mariadb
import requests
import logging
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

ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
SECRET_KEY = os.getenv('AWS_SECRET_KEY')
BUCKET = os.getenv('BUCKET')
S3_BUCKET_NAME = '2024-02-ic4302-gr1'
S3_OBJECT_PATH = 'spotify/'

ELASTIC_URL = os.getenv('ELASTIC_URL')
ELASTIC_USER = os.getenv('ELASTIC_USER')
ELASTIC_PASS = os.getenv('ELASTIC_PASS')
index_name = 'songs'
doc_type = '_doc'

HUGGINGFACE_API = ""

REQUEST_COUNT = Counter('app_requests_count', 'Número de requests totales')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latencia de requests')

maximum_object = Counter('maximum_processing_time_object', 'Tiempo máximo de procesamiento de un objeto')
minimum_object = Counter('minimum_processing_time_object', 'Tiempo mínimo de procesamiento de un objeto')

maximum_row = Counter('maximum_processing_time_row', 'Tiempo máximo de procesamiento de una fila')
minimum_row = Counter('minimum_processing_time_row', 'Tiempo mínimo de procesamiento de una fila')

objects_processed = Counter('objects_processed', 'Cantidad de objetos procesados')
rows_processed = Counter('rows_processed', 'Cantidad de filas procesados')
rows_error = Counter('rows_error', 'Cantidad de filas con error')

# Logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato del mensaje
    handlers=[
        logging.FileHandler("application.log"),  # Guardar los logs en un archivo llamado application.log
        logging.StreamHandler(sys.stdout)  # show logs in console
    ]
)

logger = logging.getLogger(__name__)

# S3 client
def create_s3_client():
    try:
        if ACCESS_KEY and SECRET_KEY:
            client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
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
        print("File not found")
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
    file_key = find_object(bucket_name, file_name, prefix)
    logger.info(f"Processing file {file_name} from bucket {bucket_name} with key {file_key}")
    if file_key:
        csv_data = read_csv_from_s3(bucket_name, file_key)
        return csv_data
    else:
        logger.error(f"File {file_name} not found in bucket {bucket_name} with prefix {prefix}.")
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

def mark_as_processed(job_id):
    query = "UPDATE objects SET processed = 1 WHERE ID = %s"
    execute_query(query, [job_id])

# Embeddings
    
def get_embeddings(text):
    try:
        response = requests.post(HUGGINGFACE_API, json={'text': text})
        if response.status_code == 200:
            return response.json()['embeddings']
    except Exception as e:
        logger.error(f"Error getting embeddings: {e}")
        return None
    
# Elasticsearch

if ELASTIC_USER and ELASTIC_PASS:
    es = Elasticsearch(
        ELASTIC_URL,
        http_auth=(ELASTIC_USER, ELASTIC_PASS),
        verify_certs=False
    )
else: es = Elasticsearch(ELASTIC_URL, verify_certs=False)

def format_data_for_indexing(data):
    for doc in data:
        yield {
            "_index": index_name,
            "_type": doc_type,
            "_id": doc['song_id'],
            "_source": doc
        }

bulk(es, format_data_for_indexing(data))
    
"""
def mark_object_as_processed(job_id):
    mariadb_conn, cursor = mariadb_connection()
    try:
        cursor.callproc('MarkObjectAsProcessed', [job_id])
        mariadb_conn.commit()
    except mariadb.Error as e:
        print(f"Error calling stored procedure MarkObjectAsProcessed: {e}")
    finally:
        cursor.close()
        mariadb_conn.close()
"""


"""def index_in_elasticsearch(data):
    for doc in data:
        es.index(index='songs', body=doc)"""


def callback(ch, method, properties, body):
    job_key = body.decode('utf-8')
    logger.info(f"Received job {job_key}")
    
    # Query to check if the job has already been processed (commented out for now)
    """
    query = "SELECT processed, s3_key FROM objects WHERE ID = %s"
    result = execute_query(query, [job_id])

    if result and result[0][0] == 1:
        print(f"Job {job_id} already processed. Skipping.")
        return

    s3_key = result[0][1]
    """

    s3_key = job_id  # Using job_id as the s3_key directly for now
    s3_data = download_from_s3(S3_BUCKET, s3_key)

    if s3_data:
        processed_data = process_csv(s3_data)
        # Uncomment this line to index the processed data into Elasticsearch
        # index_in_elasticsearch(processed_data)
        mark_as_processed(job_id)
        logger.info(f"Job {job_id} processed successfully.")
    else:
        logger.error(f"Error processing job {job_id}")


start_http_server(8000)
credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print("RABBIT_MQ: " + RABBIT_MQ)
print("RABBIT_MQ_PASSWORD: " + RABBIT_MQ_PASSWORD)
print("QUEUE_NAME: " + QUEUE_NAME)

print("MARIADB_USER: " + MARIADB_USER)
print("MARIADB_PASS: " + MARIADB_PASS)
print("MARIADB: " + MARIADB)
print("MARIADB_DB: " + MARIADB_DB)
print("MARIADB_TABLE: " + MARIADB_TABLE)

print("ACCESS_KEY: " + ACCESS_KEY)
print("SECRET_KEY: " + SECRET_KEY)
print("BUCKET: " + BUCKET)

print("ELASTIC_URL: " + ELASTIC_URL)
print("ELASTIC_USER: " + ELASTIC_USER)
print("ELASTIC_USER: " + ELASTIC_USER)


print(' [*] Waiting for messages. To exit press CTRL+C')


channel.start_consuming()