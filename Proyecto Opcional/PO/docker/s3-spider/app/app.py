import datetime as dt 
import time
import re
import os
import sys
import pika
import boto3
import mariadb 
import uuid

#Environment variables

DATA=os.getenv('DATAFROMK8S')
RABBIT_MQ=os.getenv('RABBITMQ')
RABBIT_MQ_PASSWORD=os.getenv('RABBITMQ_PASS')
QUEUE_NAME=os.getenv('RABBITMQ_QUEUE')
BUCKET = os.getenv('BUCKET')
ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
MARIADB_USER = os.getenv('MARIADB_USER')
MARIADB_PASS = os.getenv('MARIADB_PASS')
MARIADB = os.getenv('MARIADB')
MARIADB_DB = os.getenv('MARIADB_DB')
MARIADB_TABLE = os.getenv('MARIADB_TABLE')
PROCESSED_TABLE = os.getenv('PROCESSED_TABLE')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

# Set up S3 client
try :
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    print("S3 client configured")
except NameError:
    print("AWS credentials not configured")
    sys.exit(1)

# Set up MariaDB Connection 

def mariadb_connection():
    try:
        mariadb_conn = mariadb.connect(
            user=MARIADB_USER,
            password=MARIADB_PASS,
            host=MARIADB,
            port=3306,  # Change the port if necessary
            database=MARIADB_DB
        )
        cursor = mariadb_conn.cursor()
    except mariadb.Error as e:
        print(f"Error connecting to mariadb {e}")
        sys.exit(1)
    return mariadb_conn, cursor

# Funtions

# Check if an object has been processed
def is_object_processed(file_key):
    mariadb_conn, cursor = mariadb_connection()
    try:
        cursor.callproc('CheckIfObjectProcessed', [file_key])
        result = cursor.fetchone()[0]
    except mariadb.Error as e:
        print(f"Error calling stored procedure CheckIfObjectProcessed: {e}")
        result = 0
    cursor.close()
    mariadb_conn.close()
    return result > 0

# Mark an object as processed in the database
def mark_object_as_processed(file_key):
    mariadb_conn, cursor = mariadb_connection()
    try:
        cursor.callproc('MarkObjectAsProcessed', [file_key])
        mariadb_conn.commit()
    except mariadb.Error as e:
        print(f"Error calling stored procedure MarkObjectAsProcessed: {e}")
    finally:
        cursor.close()
        mariadb_conn.close()

# Extract the dois from the content of the object
def extract_dois(text):
    # Regex para identificar patrones de DOI válidos
    doi_pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b'
    
    # Search all DOIs in the text
    potential_dois = re.findall(doi_pattern, text, flags=re.IGNORECASE)
    
    # Filter the results to ensure they are valid DOIs
    valid_dois = [doi for doi in potential_dois if re.match(doi_pattern, doi)]

    valid_dois = list(set(valid_dois))

    return valid_dois

# Function to get the content of a file in S3
def get_file_content(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content

# Function to list the content of an object in a list with its Dois
def create_jobs(data, job_size):
    # Leave only the dois
    dois = extract_dois(data)
    
    # Create the jobs with the DOIs list
    jobs = [dois[i:i + job_size] for i in range(0, len(dois), job_size)]
    
    return jobs

# Function to list all the objects in a bucket
def list_all_objects(bucket):
    objects = []
    continuation_token = None
    while True:
        if continuation_token:
            response = s3_client.list_objects_v2(Bucket=bucket, ContinuationToken=continuation_token)
        else:
            response = s3_client.list_objects_v2(Bucket=bucket)
        
        if 'Contents' in response:
            objects.extend(response['Contents'])
        
        if response.get('IsTruncated'):  # If the response is truncated, there are more objects to get
            continuation_token = response.get('NextContinuationToken')
        else:
            break
    
    return objects

# Function to save job information to MariaDB
def insert_job_to_mariadb(job_id, dois):
    mariadb_conn, cursor = mariadb_connection()
    try:
        cursor.callproc('InsertJob', [job_id, 'pending', ','.join(dois), '', dt.datetime.now(), None])
        mariadb_conn.commit()
        print(f"Job ID {job_id} inserted into {MARIADB_TABLE} in {MARIADB_DB}")
        return True 
    except mariadb.Error as e:
        print(f"Error inserting job into MariaDB: {e}")
        return False
    finally:
        cursor.close()
        mariadb_conn.close()


# Main functionality

#Get the files in the bucket
files_to_read = list_all_objects(BUCKET)

# Get the objects in the  
for file in files_to_read:
    if not is_object_processed(file['Key']):
        content = get_file_content(BUCKET, file['Key'])
        jobs = create_jobs(content, job_size=10)  # Adjust job_size as needed

        for job in jobs:
            id = str(uuid.uuid4())
            insert = insert_job_to_mariadb(id, job)

            if insert :
                # Publish job ID to RabbitMQ
                msg = f"Job ID: {id}"
                channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg)
                # Mark the object as processed
                print(f"Published Job ID {id} to RabbitMQ")
            else :
                print(f"Error inserting job {id} to MariaDB")
        mark_object_as_processed(file['Key'])
    else:
        print(f"Object {file['Key']} already processed")
        

# Clean up
connection.close()
#exit aplication
print("Application finished")
sys.exit(0)

