import psycopg2
from os import getenv
from psycopg2 import pool
from contextlib import contextmanager

POSTGRES = getenv("POSTGRES")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRESQL_PASSWORD = getenv("POSTGRES_PASSWORD")

postgres_connection_pool = None

def generatePostgresConnection():
    global postgres_connection_pool
    try:
        if postgres_connection_pool is None:
            postgres_connection_pool = pool.SimpleConnectionPool(
                minconn=1,
                maxconn=5,
                host=POSTGRES,
                user=POSTGRES_USER,
                password=POSTGRESQL_PASSWORD,
                dbname=POSTGRES_DB
            )
        return postgres_connection_pool
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        exit(1)

@contextmanager
def get_connection():
    if postgres_connection_pool is None:
        generatePostgresConnection()
    connection = postgres_connection_pool.getconn()
    try:
        yield connection
    finally:
        postgres_connection_pool.putconn(connection)
    
def insertDataPostgres(table, columns, data):
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            for row in data:
                cursor.execute(query, row)
                conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Error inserting data: {e}")
        finally:
            cursor.close()

def initDB():
    try:
        # Create the database if it doesn't exist
        with psycopg2.connect(
            host=POSTGRES,
            user=POSTGRES_USER,
            password=POSTGRESQL_PASSWORD
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
                if not cursor.fetchone():
                    print("Creating PostgreSQL Database")
                    cursor.execute(f"CREATE DATABASE {POSTGRES_DB}")

        # Connect to the new database and create tables if they don’t exist
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Artist (
                    Name VARCHAR(255),
                    Genres VARCHAR(255),
                    Songs VARCHAR(255),
                    Popularity VARCHAR(255),
                    Link VARCHAR(255)
                )"""
            )
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Song (
                    ArtistLink VARCHAR(255),
                    Name VARCHAR(255),
                    Link VARCHAR(255),
                    Lyric TEXT,
                    Language VARCHAR(255)
                )"""
            )
            cursor.execute("DELETE FROM Artist")
            cursor.execute("DELETE FROM Song")            
            conn.commit()
            print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating database or tables: {e}")

def get(connection):
    conn_psql = None
    cursor_psql = None
    try:
        conn_psql = connection.getconn()
        cursor_psql = conn_psql.cursor()

        # Query to get all table names in the current database
        cursor_psql.execute("""
            SELECT * 
            FROM Artist;
        """)
        
        # Fetch all table names
        tables = cursor_psql.fetchall()
        
        # Extract table names from tuples
        table_names = [table[0] for table in tables]
        
        return table_names
    
    except Exception as e:
        print(f"Error retrieving table names: {e}")
        return []
    
    finally:
        if cursor_psql:
            cursor_psql.close()
        if conn_psql:
            conn_psql.close()