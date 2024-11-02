import pandas as pd
from io import StringIO
from os import getenv
from google.cloud import storage
from utils.postgres import initDB, insertDataPostgres
from utils.mongo import initDB as initDBMongo, insertDataMongo

BUCKET_NAME = getenv('GCS_BUCKET')
SERVICE_ACCOUNT_CREDENTIALS = "./service_account.json"

def readCSVFile(blob):
    try:
        content = blob.download_as_text()
        df = pd.read_csv(StringIO(content), keep_default_na=False, on_bad_lines="skip") # Skip bad lines to avoid errors
        if (blob.name != 'artists-data.csv'):
            # Ensure that the 'Lyric' column is a string with \n characters
            df['Lyric'] = df['Lyric'].replace(r'\n',' ', regex=False)
        
        data = df.values.tolist()
        # Delete rows like [['Tudo novo', 'o que era antigo já passou:', '', '', ''] because of the empty strings
        data = [row for row in data if not any([cell == '' for cell in row])]
        return data
    except Exception as e:
        print(f"Skipping file {blob.name} due to error: {e}")
        return []

def processArtist(data):
    header = ['Name', 'Genres', 'Songs', 'Popularity', 'Link']
    insertDataPostgres(
        'Artist',
        header,
        data
    )
    insertDataMongo(
        'Artist',
        header,
        data
    )

def processSong(data):
    header = ['ArtistLink', 'Name', 'Link', 'Lyric','Language']
    insertDataPostgres(
        'Song',
        header,
        data
    )
    insertDataMongo(
        'Song',
        header,
        data
    )

def readGoogleCloudBucket():
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS)
    blobs = client.list_blobs(BUCKET_NAME)
    return blobs

def processBlobs(blobs):
    print(f"Files in bucket '{BUCKET_NAME}':")
    for blob in blobs:
        if blob.name.endswith(".csv"):
            file = readCSVFile(blob)
            if blob.name == 'artists-data.csv':
                processArtist(file)
                print("Artists processed")
            else:
                processSong(file)
                print(f"Songs on {blob.name} processed")

if __name__ == "__main__":
    # PostgreSQL
    initDB()

    # Mongo
    initDBMongo()

    # Execution
    blobs = readGoogleCloudBucket()
    processBlobs(blobs)