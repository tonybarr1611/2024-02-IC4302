from os import getenv, path
import mariadb
import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
import psycopg2
from psycopg2 import pool

#Elasticsearch configuration

# CSV files to load
csv_file_names = ["status", "circuits", "seasons", "constructors", "drivers", "races", "constructor_results", 
                  "constructor_standings", "driver_standings", "lap_times", "pit_stops", "qualifying", "results"]

# Insert queries
insert_queries = {
    # "status": "INSERT INTO STATUS (statusId, status) VALUES (%s, %s)",
    "circuits": "INSERT INTO CIRCUIT (circuitId, circuitRef, name, location, country, lat, lng, alt, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    # "seasons": "INSERT INTO SEASON (year, url) VALUES (%s, %s)",
    "constructors": "INSERT INTO CONSTRUCTOR (constructorId, constructorRef, name, nationality, url) VALUES (%s, %s, %s, %s, %s)",
    "drivers": "INSERT INTO DRIVER (driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "races": "INSERT INTO RACE (raceId, year, round, circuitId, name, calendarDate, timeObtained, url, fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time, quali_date, quali_time, sprint_date, sprint_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    # "results": "INSERT INTO RESULT (resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    # "constructor_results": "INSERT INTO CONSTRUCTOR_RESULT (constructorResultId, raceId, constructorId, points, status) VALUES (%s, %s, %s, %s, %s)",
    # "constructor_standings": "INSERT INTO CONSTRUCTOR_STANDING (constructorStandingsId, raceId, constructorId, points, position, positionText, wins) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    # "driver_standings": "INSERT INTO DRIVER_STANDING (driverStandingsId, raceId, driverId, points, position, positionText, wins) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    "lap_times": "INSERT INTO LAP_TIME (raceId, driverId, lap, position, timeObtained, milliseconds) VALUES (%s, %s, %s, %s, %s, %s)",
    # "pit_stops": "INSERT INTO PIT_STOP (raceId, driverId, stop, lap, timeObtained, duration, milliseconds) VALUES (%s, %s, %s, %s, %s, %s, %s)",
    # "qualifying": "INSERT INTO QUALIFYING (qualifyId, raceId, driverId, constructorId, assignedNumber, position, q1, q2, q3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    # "sprint_results": "INSERT INTO SPRINT_RESULT (resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, fastestLapTime, statusId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
}

insert_queries_postgres = {
    "circuits": "INSERT INTO circuit (circuitId, circuitRef, name, location, country, lat, lng, alt, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "constructors": "INSERT INTO constructor (constructorId, constructorRef, name, nationality, url) VALUES (%s, %s, %s, %s, %s)",
    "drivers": "INSERT INTO driver (driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "races": "INSERT INTO race (raceId, year, round, circuitId, name, calendarDate, timeObtained, url, fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time, quali_date, quali_time, sprint_date, sprint_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
    "lap_times": "INSERT INTO LAP_TIME (raceId, driverId, lap, position, timeObtained, milliseconds) VALUES (%s, %s, %s, %s, %s, %s)",
}

# Directory where the CSV files are located
CSV_DIR = "loader/data"


# MariaDB configuration

MARIADB = getenv("MARIADB")
MARIADB_USER = getenv("MARIADB_USER")
MARIADB_PASSWORD = getenv("MARIADB_PASSWORD")

POSTGRES = getenv("POSTGRES")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRESQL_PASSWORD = getenv("POSTGRES_PASSWORD")

ELASTIC = getenv("ELASTIC")
ELASTIC_USER = getenv("ELASTIC_USER")
ELASTIC_PASSWORD = getenv("ELASTIC_PASSWORD")

print(f"MariaDB: {MARIADB}")
print(f"MariaDB User: {MARIADB_USER}")
print(f"MariaDB Password: {MARIADB_PASSWORD}")

print(f"PostgreSQL: {POSTGRES}")
print(f"PostgreSQL User: {POSTGRES_USER}")
print(f"PostgreSQL Password: {POSTGRESQL_PASSWORD}")

print(f"Elasticsearch: {ELASTIC}")
print(f"Elasticsearch User: {ELASTIC_USER}")
print(f"Elasticsearch Password: {ELASTIC_PASSWORD}")

# Conection to Elasticsearch

def create_elasticsearch_connection():
    try:
        elasticsearch_connection = Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
        return elasticsearch_connection
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        exit(1)
        return None

def load_elasticsearch(elasticsearch_connection):
    try:
        for csv_file in insert_queries:
            file_path = f"{CSV_DIR}/{csv_file}.csv"
            
            if path.exists(file_path):
                # create the index name
                index_name = f"f1_records_{csv_file}"
            
                # read the CSV file
                info = pd.read_csv(file_path)
            
                # convert to dictionary
                records = info.to_dict(orient='records')
            
                # tranformation to the format required by Elasticsearch
                actions = [
                    {
                        "_index": index_name,
                        "_source": record
                    }
                    for record in records
                ]
                
                # upload data to Elasticsearch
                for action in actions:
                    elasticsearch_connection.index(index=action["_index"], body=action["_source"])
                print(f"Uploaded {len(records)} records to Elasticsearch index: {index_name}")
            else:
                print(f"El archivo {file_path} no existe.")
                exit(1)
    except Exception as e:
        print(f"Error loading data into Elasticsearch: {e}")
        exit(1)

# Establish a connection pool to MariaDB
def create_connection_pool():
    return mariadb.ConnectionPool(
        pool_name="mariadb_pool",
        pool_size=5,
        host=MARIADB,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
    )

# Create the database 
def create_database(pool: mariadb.ConnectionPool):
    conn = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS f1_records")
        cursor.close()
    except mariadb.Error as e:
        print(f"Error creating database: {e}")
        exit(1)
    finally:
        if conn:
            conn.close()
            
# Executes the SQL script called \loader\MariaDB.sql
def execute_script(pool: mariadb.ConnectionPool):
    conn = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("USE f1_records")
        with open("loader/MariaDB.sql", "r") as file:
            sql_script = file.read()
        sql_statements = sql_script.split(';')
        for statement in sql_statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed statement: {statement}")
                except mariadb.Error as e:
                    print(f"Error executing statement: {e}")
                    print(f"Failed statement: {statement}")
                    exit(1)
        cursor.close()
    except mariadb.Error as e:
        print(f"Error executing script: {e}")
        exit(1)
    finally:
        if conn:
            conn.close()

# Insert data into the database
def insert_data(pool: mariadb.ConnectionPool):
    conn = None
    try:
        conn = pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("USE f1_records")
        for query in insert_queries:
            csv_data = open(f"{CSV_DIR}/{query}.csv", "r")
            # Ignore header row
            header = True
            for row in csv_data:
                if header:
                    print(f"Header: {row}")
                    header = False
                else:
                    try:
                        cursor.execute(insert_queries[query], row.split(","))
                    except Exception as e:
                        print(f"Failed to insert row: {row}")
                        print(f"Error: {e}")
            csv_data.close()
            print(f"Inserted data for: {query}")
        conn.commit()
    except mariadb.Error as e:
        print(f"Error executing script: {e}")
        exit(1)
    finally:
        if conn:
            conn.close()

def create_postgres_connection_pool(dbname=False):
    if dbname:
        return psycopg2.pool.SimpleConnectionPool(
            minconn = 1,
            maxconn = 5,
            host = POSTGRES,
            user = POSTGRES_USER,
            password = POSTGRESQL_PASSWORD,
            dbname = 'f1_records'
        )
    else:
        return psycopg2.pool.SimpleConnectionPool(
            minconn = 1,
            maxconn = 5,
            host = POSTGRES,
            user = POSTGRES_USER,
            password = POSTGRESQL_PASSWORD
        )

# Create the database
def create_postgres_database(connection_pool):
    conn = None
    try:
        conn = connection_pool.getconn()
        conn.autocommit = True  # Enable autocommit mode
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'f1_records'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE f1_records")
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        exit(1)
    finally:
        if conn:
            connection_pool.putconn(conn)

# Executes the SQL script for PostgreSQL
def execute_postgresql_script(pool: psycopg2.pool.SimpleConnectionPool):
    conn = None
    try:
        conn = pool.getconn()
        cursor = conn.cursor()
        with open("loader/postgreSQL.sql", "r") as file:
            sql_script = file.read()
        sql_statements = sql_script.split(';')
        for statement in sql_statements:
            if statement.strip():
                try:
                    cursor.execute(statement)
                    print(f"Executed statement: {statement}")
                except psycopg2.Error as e:
                    print(f"Error executing statement: {e}")
                    print(f"Failed statement: {statement}")
                    exit(1)
        cursor.close()
        conn.commit()  # Ensure all statements are committed
    except psycopg2.Error as e:
        print(f"Error executing script: {e}")
        exit(1)
    finally:
        if conn:
            pool.putconn(conn)

# Insert data into the PostgreSQL database
def insert_data_postgresql(pool: psycopg2.pool.SimpleConnectionPool):
    conn = None
    try:
        conn = pool.getconn()
        cursor = conn.cursor()
        #cursor.execute("SET search_path TO f1_records")  # Set schema if necessary
        for query in insert_queries_postgres:
            csv_data = open(f"{CSV_DIR}/{query}.csv", "r")
            # Ignore header row
            header = True
            for row in csv_data:
                if header:
                    print(f"Header: {row}")
                    header = False
                else:
                    try:
                        cursor.execute(insert_queries_postgres[query], row.strip().split(","))

                    except Exception as e:
                        print(f"Failed to insert row: {row}")
                        print(f"Error: {e}")
            csv_data.close()
            print(f"Inserted data for: {query}")
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error executing script: {e}")
        exit(1)
    finally:
        if conn:
            pool.putconn(conn)

def execute_mariadb():
    pool = create_connection_pool()
    print("Connection pool created")
    create_database(pool)
    print("Database created")
    execute_script(pool)
    print("Script executed")
    insert_data(pool)
    print("Data inserted")
    pool.close()
    print("Connection pool closed")


def execute_postgres():
    pool = create_postgres_connection_pool()
    print('--------- connection created ---------')
    create_postgres_database(pool)
    pool = create_postgres_connection_pool(True)
    print('--------- database created ---------')
    execute_postgresql_script(pool)
    print('--------- script executed ---------')
    insert_data_postgresql(pool)
    print('--------- data inserted ---------')
    
def execute_elasticsearch():
    elasticsearch_connection = create_elasticsearch_connection()
    print("Connection to Elasticsearch established")
    load_elasticsearch(elasticsearch_connection)
    print("Data loaded into Elasticsearch")

def testConnection():
    create_connection_pool()
    create_postgres_connection_pool()
    create_elasticsearch_connection()

if __name__ == "__main__":
    testConnection()
    execute_mariadb()
    execute_postgres()
    execute_elasticsearch()
    exit(0)