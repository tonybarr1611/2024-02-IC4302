import time
import os
import sys
import pika
from datetime import datetime
import json
import hashlib
import json
import mariadb


hostname = os.getenv('HOSTNAME')
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

print("DATA: ", DATA)
print("RABBIT_MQ: ", RABBIT_MQ)
print("RABBIT_MQ_PASSWORD: ", RABBIT_MQ_PASSWORD)
print("QUEUE_NAME: ", QUEUE_NAME)

print("MARIADB_USER: ", MARIADB_USER)
print("MARIADB_PASS: ", MARIADB_PASS)
print("MARIADB: ", MARIADB)
print("MARIADB_DB: ", MARIADB_DB)
print("MARIADB_TABLE: ", MARIADB_TABLE)

# Conectar a MariaDB
def create_connection_pool():
    print("Creando pool de conexiones")
    pool = mariadb.ConnectionPool(
        host=MARIADB,
        port=3306,
        user=MARIADB_USER,
        password=MARIADB_PASS,
        database=MARIADB_DB, # my_database es el nombre de la base de datos con la cual nos funciono
        pool_name="job_pool",
        pool_size=10  
    )
    print ("Pool de conexiones creado")
    return pool


# Inicializar el pool de conexiones
pool = create_connection_pool()
print("Pool de conexiones inicializado")

# Obtener una conexión del pool
def get_connection():
    try:
        print("Obteniendo conexión")
        return pool.get_connection()
    except mariadb.PoolError as e:
        print(f"Error obtaining connection from pool: {e}")
        return None

# Devolver una conexión al pool
print("Devolviendo conexión")
get_connection()
print ("Conexión devuelta")

def callback(ch, method, properties, body):
    json_object = json.loads(body)
    with open(XPATH+'/'+hashlib.md5(body).hexdigest()+'.json', 'w') as f:
        json.dump(json_object, f)
    print(" [x] Received %r" % body)


credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()


