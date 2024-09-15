import os
import sys
import pika
import mariadb
import boto3
import csv
import requests



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
S3_BUCKET = os.getenv('S3_BUCKET')
HUGGINGFACE_API = "https://api-inference.huggingface.co/models/sentence-transformers/all-mpnet-base-v2"




def S3_BUCKET():
    try:
        if ACCESS_KEY and SECRET_KEY:
            s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
            print("S3 client configured")
        else:
            print("AWS credentials not configured")
            sys.exit(1)
    except Exception as e:
        print(f"Error configuring S3 client: {e}")
        sys.exit(1)

s3_client = S3_BUCKET()


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
        print(f"Error executing query: {e}")
    finally:
        if conn:
            conn.close()

def download_from_s3(bucket,s3_key):
    try:
        response = s3_client.get_object(Bucket=bucket, Key=s3_key)
        content= response['Body'].read().decode('utf-8')
        return content
    except Exception as e:
        print(f"Error downloading from S3: {e}")
        return None
    
def get_embeddings(text):
    try:
        response = requests.post(HUGGINGFACE_API, json={'text': text})
        if response.status_code == 200:
            return response.json()['embeddings']
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return None

def process_csv(s3_data):
    rows = []
    csv_reader = csv.DictReader(s3_data.splitlines())
    for row in csv_reader:
        embedding = get_embeddings(row['lyrics'])
        if embedding:
            row['embeddings'] = embedding
            rows.append(row)
    return rows

def mark_as_processed(job_id):
    query = "UPDATE objects SET processed = 1 WHERE ID = %s"
    execute_query(query, [job_id])
    
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
    job_id = body.decode('utf-8')
    print(f"Received message: {job_id}")
    
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
        print(f"Job {job_id} processed and indexed.")
    else:
        print(f"Job {job_id} failed to download data from S3.")


credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()