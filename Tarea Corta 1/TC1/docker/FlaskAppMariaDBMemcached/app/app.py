# Flask App for PostgreSQL
from flask import Flask
from os import getenv
import mariadb
from pymemcache.client import base

MARIADB = getenv("MARIADB")
MARIADB_USER = getenv("MARIADB_USER")
MARIADB_PASSWORD = getenv("MARIADB_PASSWORD")

print(f"MariaDB: {MARIADB}")
print(f"MariaDB User: {MARIADB_USER}")
print(f"MariaDB Password: {MARIADB_PASSWORD}")

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
    
memcached_connection = None
try:
    memcached_connection = base.Client(('localhost', 11211))
except Exception as e:
    print(f"Error connecting to MemCached: {e}")
    exit(1)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/drivers", methods=['GET'])
def get_drivers():
    query = "SELECT driverId, driverRef, assignedNumber, code, forename, surname, dob, nationality, url FROM DRIVER ORDER BY driverId;"
    cache_value = memcached_connection.get("drivers")
    if cache_value is None:
        return f"<h1>MariaDBCached</h1><p>{cache_value}</p>"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    memcached_connection.set("drivers", result_mdb)
    return f"<h1>MariaDB</h1><p>{result_mdb}</p>"

@app.route("/constructors", methods=['GET'])
def get_constructors():
    query = "SELECT * FROM CONSTRUCTOR ORDER BY constructorId;"
    cache_value = memcached_connection.get("constructors")
    if cache_value is None:
        return f"<h1>MariaDBCached</h1><p>{cache_value}</p>"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    memcached_connection.set("constructors", result_mdb)
    return f"<h1>MariaDB</h1><p>{result_mdb}</p>"

@app.route("/circuits", methods=['GET'])
def get_laps():
    query = "SELECT * FROM CIRCUIT ORDER BY circuitId"
    cache_value = memcached_connection.get("circuits")
    if cache_value is None:
        return f"<h1>MariaDBCached</h1><p>{cache_value}</p>"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    memcached_connection.set("circuits", result_mdb)
    return f"<h1>MariaDB</h1><p>{result_mdb}</p>"

@app.route("/races", methods=['GET'])
def get_laps_driver():
    query = "SELECT * FROM RACE ORDER BY raceId"
    cache_value = memcached_connection.get("races")
    if cache_value is None:
        return f"<h1>MariaDBCached</h1><p>{cache_value}</p>"
    
    conn_mdb = mariadb_connection.get_connection()
    cursor_mdb = conn_mdb.cursor()
    
    cursor_mdb.execute(query)
    result_mdb = cursor_mdb.fetchall()
    cursor_mdb.close()
    
    memcached_connection.set("races", result_mdb)
    return f"<h1>MariaDB</h1><p>{result_mdb}</p>"

if __name__ == "__main__":
    # Run on localhost:5000
    app.run(host='localhost', port=5000)
