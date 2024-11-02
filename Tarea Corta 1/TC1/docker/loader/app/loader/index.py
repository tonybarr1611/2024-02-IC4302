import os
import psycopg2
import pandas as pd
# import mysql.connector
# from elasticsearch import Elasticsearch, helpers

CSV_DIR = './data'
MARIADB_FILE = './MariaDB.sql'
POSTGRESQL_FILE = 'C:/Users/barra/Escritorio/OneDrive - Estudiantes ITCR/TEC/2024 - II Semestre/IC4302 - Bases de Datos II/Grupal/Tarea Corta 1/TC1/docker/FlaskApp/app/loader/postgreSQL.sql'

# elasticsearch_connection = Elasticsearch("http://localhost:9200")  # TODO: Replace with your Elasticsearch URL
# index_prefix = "f1_records"

# def load_elasticsearch(csv_dir, elasticsearch_connection, index_prefix):
#     for csv_file in os.listdir(csv_dir):
#         if csv_file.endswith('.csv'):
#             index_name = index_prefix + os.path.splitext(csv_file)[0]
            
#             file_path = os.path.join(csv_dir, csv_file)
#             info = pd.read_csv(file_path)
            
#             records = info.to_dict(orient='records')
            
#             helpers.bulk(elasticsearch_connection, records, index=index_name)
#             print(f"Uploaded {len(records)} records to Elasticsearch index: {index_name}")

# load_elasticsearch(CSV_DIR, elasticsearch_connection, index_prefix)

# def execute_MariaDB_script(connection):
#     cursor = connection.cursor()

#     with open(MARIADB_FILE, 'r') as file:
#         sql_script = file.read()

#     for result in cursor.execute(sql_script, multi=True):
#         if result.with_rows:
#             print(f"Affected Rows: {result.rowcount}")
#         else:
#             print(f"Executed query: {result.statement}")

#     cursor.close()

# def load_MariaDB():
#     config = {
#         'user': 'your_username', #TODO
#         'password': 'your_password', #TODO
#         'host': 'your_host', #TODO
#         'database': 'f1_records'
#     }

#     connection = mysql.connector.connect(**config)

#     try:
#         execute_MariaDB_script(connection)

#     finally:
#         connection.close()

def execute_PostgreSQL_script(connection):
    cursor = connection.cursor()

    with open(POSTGRESQL_FILE, 'r') as file:
        sql_script = file.read()

    cursor.execute(sql_script)

    connection.commit()
    cursor.close()

def load_PostgreSQL():
    config = {
        'database': 'f1_records',  # TODO
        'user': 'postgres',  # TODO
        'password': 'IBZevT1fBr',  # TODO
        'host': 'localhost',  # TODO
        'port': '5432'  # TODO
    }

    connection = psycopg2.connect(**config)

    try:
        execute_PostgreSQL_script(connection)

    finally:
        connection.close()

load_PostgreSQL()