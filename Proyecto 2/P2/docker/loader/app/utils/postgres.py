import psycopg2
from os import getenv
from psycopg2 import pool

POSTGRES = getenv("POSTGRES")
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRESQL_PASSWORD = getenv("POSTGRES_PASSWORD")

def generatePostgresConnection():
    try:
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
    
def insertDataPostgres(connection, table, columns, data):
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"

    conn_psql = connection.getconn()
    cursor_psql = conn_psql.cursor()
    
    try:
        for row in data:
            cursor_psql.execute(query, row)
        conn_psql.commit()
    except Exception as e:
        conn_psql.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cursor_psql.close()
        conn_psql.close()

def initDB(connection):
    conn_psql = None
    cursor_psql = None
    try:
        conn_psql = psycopg2.connect(
            host=POSTGRES,
            user=POSTGRES_USER,
            password=POSTGRESQL_PASSWORD
        )
        conn_psql.autocommit = True
        cursor_psql = conn_psql.cursor()

        cursor_psql.execute(f"SELECT 1 FROM pg_database WHERE datname = '{POSTGRES_DB}'")
        if not cursor_psql.fetchone():
            print("Creating PostgreSQL Database")
            cursor_psql.execute(f"CREATE DATABASE {POSTGRES_DB}")

        conn_psql = connection.getconn()
        cursor_psql = conn_psql.cursor()

        cursor_psql.execute("""
            CREATE TABLE IF NOT EXISTS Artist (
                Name VARCHAR(255),
                Genres VARCHAR(255),
                Songs VARCHAR(255),
                Popularity VARCHAR(255),
                Link VARCHAR(255)
            )"""
        )
        print(f"4. Table 'Artist' created successfully.")

        cursor_psql.execute("""
            CREATE TABLE IF NOT EXISTS Song (
                ArtistLink VARCHAR(255),
                Name VARCHAR(255),
                Link VARCHAR(255),
                Lyric TEXT,
                Language VARCHAR(255)
            )"""
        )
        conn_psql.commit()
    except Exception as e:
        print(f"Error creating database or tables: {e}")
    finally:
        if cursor_psql:
            cursor_psql.close()
        if conn_psql:
            conn_psql.close()

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