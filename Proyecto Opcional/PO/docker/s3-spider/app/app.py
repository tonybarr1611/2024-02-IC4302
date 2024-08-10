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


while True:
    localtime = time.localtime()
    result = time.strftime("%I:%M:%S %p", localtime)
    msg = "{\"msg\": \""+result+"\"}"
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=msg)
    print(DATA+" - " +result)
    time.sleep(1)
    
connection.close()
