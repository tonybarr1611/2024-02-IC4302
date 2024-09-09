# Flask App for PostgreSQL
from flask import Flask
from os import getenv
import mariadb
import pandas as pd
import csv
from elasticsearch import Elasticsearch, helpers
import psycopg2
from psycopg2 import pool

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

app = Flask(__name__)

mariadb_connection = None
try:
  mariadb_connection = mariadb.ConnectionPool(
        pool_name="mariadb_pool",
        pool_size=5,
        host=MARIADB,
        user=MARIADB_USER,
        password=MARIADB_PASSWORD,
        database="f1_records"
    )
except Exception as e:
    print(f"Error connecting to MariaDB: {e}")
    exit(1)
    
postgres_connection = None
try:
    postgres_connection = psycopg2.pool.SimpleConnectionPool(
            minconn = 1,
            maxconn = 5,
            host = POSTGRES,
            user = POSTGRES_USER,
            password = POSTGRESQL_PASSWORD,
            dbname = 'f1_records'
        )
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    exit(1)
    
elastic_connection = None
try:
    elastic_connection =  Elasticsearch([ELASTIC], basic_auth=[ELASTIC_USER, ELASTIC_PASSWORD])
except:
    print("Error connecting to Elasticsearch")
    exit(1)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/drivers", methods=['GET'])
def get_drivers():
    query = "SELECT driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url FROM DRIVER ORDER BY driverId;"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/constructors", methods=['GET'])
def get_constructors():
    query = "SELECT constructorId, constructorRef, name, nationality, url FROM CONSTRUCTOR ORDER BY constructorId;"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/circuit/<int:id>/laps", methods=['GET'])
def get_laps(id):
    query = "SELECT   L.lapId, L.driverId, CONCAT(D.forename, ' ', D.surname) AS driverName, D.code AS driverCode, R.raceId, R.name AS raceName, R.year, R.date, L.lap, L.position, L.timeObtained, L.milliseconds FROM  LAP_TIME L LEFT JOIN RACE R on L.raceId = R.raceId LEFT JOIN CIRCUIT C on R.circuitId = C.circuitId LEFT JOIN DRIVER D on L.driverId = D.driverId WHERE C.circuitId = id"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/drivers/<int:id>/laps", methods=['GET'])
def get_laps_driver(id):
    query = "SELECT L.lapId, L.driverId, CONCAT(D.forename, ' ', D.surname) AS driverName, D.code AS driverCode, R.raceId, R.name AS raceName, R.year, R.date, L.lap, L.position, L.timeObtained, L.milliseconds FROM LAP_TIME L LEFT JOIN RACE R on L.raceId = R.raceId LEFT JOIN DRIVER D on L.driverId = D.driverId WHERE L.driverId = id"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/driver/<int:id>/total_races", methods=['GET'])
def get_total_races_driver(id):
    query = "SELECT D.driverId, D.forename, D.surname, D.code, COUNT(DISTINCT R.raceId) AS totalRaces FROM DRIVER D LEFT JOIN LAP_TIME L on D.driverId = L.driverId LEFT JOIN RACE R on L.raceId = R.raceId WHERE D.driverId = id GROUP BY D.driverId, D.forename, D.surname, D.code"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

@app.route("/driver/<int:id>/pitstops", methods=['GET'])
def get_pitstops_driver(id):
    query = "SELECT P.pitstopId, P.driverId, CONCAT(D.forename, ' ', D.surname) AS driverName, D.code AS driverCode, R.raceId, R.name AS raceName, R.year, R.date, P.lap, P.stop, P.time, P.duration, P.milliseconds FROM PITSTOP P LEFT JOIN DRIVER D on P.driverId = D.driverId LEFT JOIN RACE R on P.raceId = R.raceId WHERE P.driverId = id"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    conn_psql = postgres_connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    cursor_psql.execute(query)
    results_psql = cursor_psql.fetchall()
    cursor_psql.close()
    
    return f"<h1>MariaDB</h1><p>{result_mdb}</p><h1>PostgreSQL</h1><p>{results_psql}</p>"

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host='localhost', port=5000)
