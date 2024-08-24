import os
import pika
import json
import mariadb
import hashlib
import requests
import datetime

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
API = 'https://api.crossref.org/works/'


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

def get_doi_information(doi_id):
    try:
        response = requests.get(API + doi_id)
        if response.status_code == 200:
            res = response.json()
            return res
        else:
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def save_json(name, data):
    md5_doi = hashlib.md5(name.encode()).hexdigest()
    filename = f"MD5({md5_doi}).json"
    filepath = os.path.join(XPATH, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)
    return True

def update_info(job_id, doi):
    doi_info = get_doi_information(doi)

    if doi_info:
        save_json(doi, doi_info)
        print(f'DOI {doi} saved')
    else:
        query = "SELECT omitido FROM objects WHERE ID = %s"
        results = execute_query(query, [job_id])

        if results:
            for row in results:
                omitted = row[0]
                omitted = omitted + f'{doi};'
                print(f'DOI {doi} ommited')

        query = "UPDATE objects SET omitido = %s WHERE ID = %s"
        results = execute_query(query, [doi, job_id])
        print('omitted saved')

def callback(ch, method, properties, body):
    # Get Job ID from RabbitMQ
    job_id = body.decode('utf-8')
    print('------------------')
    print(f"Received message: {job_id}")

    # Update Job state in MariaDB
    query ="UPDATE objects SET Estado = 'in-progress' WHERE ID = %s"
    execute_query(query, [job_id])

    # Get JOB
    query = "SELECT ID, Estado, DOIs, omitido FROM objects WHERE ID = %s"
    results = execute_query(query, [job_id])

    if results:
        for row in results:
            separated_dois = row[2].split(",")
            for doi in separated_dois:
                update_info(job_id, doi)
        
    # Update Job state in MariaDB
    query = "UPDATE objects SET Estado = 'done', fecha_fin = %s WHERE ID = %s"
    results = execute_query(query, [datetime.datetime.now(), job_id])

credentials = pika.PlainCredentials('user', RABBIT_MQ_PASSWORD)
parameters = pika.ConnectionParameters(host=RABBIT_MQ, credentials=credentials) 
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)
channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()