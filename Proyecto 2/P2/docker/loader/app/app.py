import csv
from os import getenv
from google.cloud import storage
from utils.postgres import generatePostgresConnection, initDB, insertDataPostgres, get
from utils.mongo import generateMongoConnection, insertDataMongo

BUCKET_NAME = getenv('GCS_BUCKET')
SERVICE_ACCOUNT_CREDENTIALS = "./service_account.json"

def readCSVFile(blob):
    content = blob.download_as_text()
    reader = csv.reader(content.splitlines())
    data = [row for row in reader if row][1:]
    return data

def processArtist(postgresConnection, mongoConnection, data):
    header = ['Name', 'Genres', 'Songs', 'Popularity', 'Link']
    insertDataPostgres(
        postgresConnection,
        'Artist',
        header,
        data
    )
    insertDataMongo(
        mongoConnection,
        'Artist',
        header,
        data
    )

def processSong(postgresConnection, mongoConnection, data):
    header = ['ArtistLink', 'Name', 'Link', 'Lyric','Language']
    insertDataPostgres(
        postgresConnection,
        'Song',
        header,
        data
    )
    insertDataMongo(
        mongoConnection,
        'Song',
        header,
        data
    )

def readGoogleCloudBucket():
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS)
    blobs = client.list_blobs(BUCKET_NAME)
    return blobs

def processBlobs(postgresConnection, mongoConnection, blobs):
    print(f"Files in bucket '{BUCKET_NAME}':")
    for blob in blobs:
        if blob.name.endswith(".csv"):
            print(f"Processing CSV file: {blob.name}")
            file = readCSVFile(blob)
            if blob.name == 'artists-data.csv':
                processArtist(postgresConnection, mongoConnection, file)
            else:
                processSong(postgresConnection, mongoConnection, file)

if __name__ == "__main__":
    # PostgreSQL
    postgresPool = generatePostgresConnection()
    initDB(postgresPool)

    # Mongo
    mongoPool = generateMongoConnection()

    # Execution
    blobs = readGoogleCloudBucket()
    processBlobs(postgresPool, mongoPool, blobs)