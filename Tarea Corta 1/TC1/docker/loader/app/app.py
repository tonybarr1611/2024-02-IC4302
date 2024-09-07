import os
import mariadb
import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers

#Elasticsearch configuration

# CSV files to load
csv_file_names = ["status", "circuits", "seasons", "constructors", "drivers", "races", "constructor_results", 
                  "constructor_standings", "driver_standings", "lap_times", "pit_stops", "qualifying", "results"]

# Directory where the CSV files are located
CSV_DIR = "loader/data"

# Conection to Elasticsearch
try: 
    elasticsearch_connection = Elasticsearch("http://ic4302-es-http:9200")  # Cambia la URL si es necesario
    index_prefix = "f1_records"
except Exception as e:
    print(f"Error connecting to Elasticsearch: {e}")

def load_elasticsearch(csv_file_names, csv_dir, elasticsearch_connection, index_prefix):
    try:
        for csv_file in csv_file_names:
            file_path = os.path.join(csv_dir, f"{csv_file}.csv")
            
            if os.path.exists(file_path):
                # create the index name
                index_name = index_prefix + "_" + csv_file
            
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
                helpers.bulk(elasticsearch_connection, actions)
                print(f"Uploaded {len(records)} records to Elasticsearch index: {index_name}")
            else:
                print(f"El archivo {file_path} no existe.")
    except Exception as e:
        print(f"Error loading data into Elasticsearch: {e}")

# call the function to load data into Elasticsearch
load_elasticsearch(csv_file_names, CSV_DIR, elasticsearch_connection, index_prefix)

# MariaDB configuration

MARIADB = os.getenv("MARIADB")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")

print(f"MariaDB: {MARIADB}")
print(f"MariaDB User: {MARIADB_USER}")
print(f"MariaDB Password: {MARIADB_PASSWORD}")


# # Insert queries
# insert_queries = {
#     "status": "INSERT INTO STATUS (statusId, status) VALUES (%s, %s)",
#     "circuits": "INSERT INTO CIRCUIT (circuitId, circuitRef, name, location, country, lat, lng, alt, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     "seasons": "INSERT INTO SEASON (year, url) VALUES (%s, %s)",
#     "constructors": "INSERT INTO CONSTRUCTOR (constructorId, constructorRef, name, nationality, url) VALUES (%s, %s, %s, %s, %s)",
#     "drivers": "INSERT INTO DRIVER (driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     "races": "INSERT INTO RACE (raceId, year, round, circuitId, name, calendarDate, timeObtained, url, fp1_date, fp1_time, fp2_date, fp2_time, fp3_date, fp3_time, quali_date, quali_time, sprint_date, sprint_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     "constructor_results": "INSERT INTO CONSTRUCTOR_RESULT (constructorResultId, raceId, constructorId, points, status) VALUES (%s, %s, %s, %s, %s)",
#     "constructor_standings": "INSERT INTO CONSTRUCTOR_STANDING (constructorStandingsId, raceId, constructorId, points, position, positionText, wins) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#     "driver_standings": "INSERT INTO DRIVER_STANDING (driverStandingsId, raceId, driverId, points, position, positionText, wins) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#     "lap_times": "INSERT INTO LAP_TIME (raceId, driverId, lap, position, timeObtained, milliseconds) VALUES (%s, %s, %s, %s, %s, %s)",
#     "pit_stops": "INSERT INTO PIT_STOP (raceId, driverId, stop, lap, timeObtained, duration, milliseconds) VALUES (%s, %s, %s, %s, %s, %s, %s)",
#     "qualifying": "INSERT INTO QUALIFYING (qualifyId, raceId, driverId, constructorId, assignedNumber, position, q1, q2, q3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     "results": "INSERT INTO RESULT (resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, rank, fastestLapTime, fastestLapSpeed, statusId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#     "sprint_results": "INSERT INTO SPRINT_RESULT (resultId, raceId, driverId, constructorId, assignedNumber, grid, position, positionText, positionOrder, points, laps, timeObtained, milliseconds, fastestLap, fastestLapTime, statusId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
# }

# # Establish a connection pool to MariaDB
# def create_connection_pool():
#     return mariadb.ConnectionPool(
#         pool_name="mariadb_pool",
#         pool_size=5,
#         host=MARIADB,
#         user=MARIADB_USER,
#         password=MARIADB_PASSWORD,
#     )

# # Create the database 
# def create_database(pool: mariadb.ConnectionPool):
#     conn = None
#     try:
#         conn = pool.get_connection()
#         cursor = conn.cursor()
#         cursor.execute("CREATE DATABASE IF NOT EXISTS f1_records")
#         cursor.close()
#     except mariadb.Error as e:
#         print(f"Error creating database: {e}")
#         exit(1)
#     finally:
#         if conn:
#             conn.close()
            
# # Executes the SQL script called \loader\MariaDB.sql
# def execute_script(pool: mariadb.ConnectionPool):
#     conn = None
#     try:
#         conn = pool.get_connection()
#         cursor = conn.cursor()
#         cursor.execute("USE f1_records")
#         with open("loader/MariaDB.sql", "r") as file:
#             sql_script = file.read()
#         sql_statements = sql_script.split(';')
#         for statement in sql_statements:
#             if statement.strip():
#                 try:
#                     cursor.execute(statement)
#                     print(f"Executed statement: {statement}")
#                 except mariadb.Error as e:
#                     print(f"Error executing statement: {e}")
#                     print(f"Failed statement: {statement}")
#                     exit(1)
#         cursor.close()
#     except mariadb.Error as e:
#         print(f"Error executing script: {e}")
#         exit(1)
#     finally:
#         if conn:
#             conn.close()

# # Insert data into the database
# def insert_data(pool: mariadb.ConnectionPool):
#     conn = None
#     try:
#         conn = pool.get_connection()
#         cursor = conn.cursor()
#         cursor.execute("USE f1_records")
#         for query in insert_queries:
#             csv_data = open(f"loader/data/{query}.csv", "r")
#             # Ignore header row
#             header = True
#             for row in csv_data:
#                 if header:
#                     print(f"Header: {row}")
#                     header = False
#                 else:
#                     try:
#                         cursor.execute(insert_queries[query], row.split(","))
#                     except Exception as e:
#                         print(f"Failed to insert row: {row}")
#                         print(f"Error: {e}")
#             csv_data.close()
#             print(f"Inserted data for: {query}")
#         conn.commit()
#     except mariadb.Error as e:
#         print(f"Error executing script: {e}")
#         exit(1)
#     finally:
#         if conn:
#             conn.close()
    
# pool = create_connection_pool()
# print("Connection pool created")
# create_database(pool)
# print("Database created")
# execute_script(pool)
# print("Script executed")
# insert_data(pool)
# print("Data inserted")
# pool.close()
# print("Connection pool closed")

# exit(0)