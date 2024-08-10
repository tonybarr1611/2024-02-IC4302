import time
import os
import sys
import pika
import boto3

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
 
hostname = os.getenv('HOSTNAME')

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

# Set up S3 client
try :
    s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
except NameError:
    print("No se ha configurado las credenciales de AWS")
    sys.exit(1)

# TODO Set up MariaDB Connection 

# Funtions

# Extract the dois from the content of the object
def extract_dois(text):
    # Regex para identificar patrones de DOI válidos
    doi_pattern = r'\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b'
    
    # Buscar todos los DOI en el texto
    potential_dois = re.findall(doi_pattern, text, flags=re.IGNORECASE)
    
    # Filtrar los resultados para asegurar que sean DOIs válidos
    valid_dois = [doi for doi in potential_dois if re.match(doi_pattern, doi)]

    return valid_dois

# Function to get the content of a file in S3
def get_file_content(bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content

# Function to list the content of an object in a list with its Dois
# TODO Por alguna razon crea dois nuevos cuando se compara con el contenido original esto se da en la funcion extract_dois 
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
        
        if response.get('IsTruncated'):  # Si la respuesta está truncada, hay más objetos que obtener
            continuation_token = response.get('NextContinuationToken')
        else:
            break
    
    return objects

# Funcionality 

# Get the objects to read 
files_to_read = list_all_objects(BUCKET)


while True:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    msg = "{\"msg\": \""+result+"\"}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg)
    print(DATA+" - " +result)
    time.sleep(1)
    
connection.close()
