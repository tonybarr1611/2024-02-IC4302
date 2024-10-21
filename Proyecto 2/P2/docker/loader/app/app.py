import csv
from google.cloud import storage

SERVICE_ACCOUNT_CREDENTIALS = "./service_account.json"

BUCKET_NAME = "ic4302-202402"

def readCSVFile(blob):
    content = blob.download_as_text()
    return csv.reader(content.splitlines())

def processArtist(file):
    print('Processing Artist')

def processLyric(file):
    print('Processing Lyric')

def readGoogleCloudBucket():
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_CREDENTIALS)
    blobs = client.list_blobs(BUCKET_NAME)
    return blobs

def processBlobs(blobs):
    print(f"Files in bucket '{BUCKET_NAME}':")
    for blob in blobs:
        if blob.name.endswith(".csv"):
            print(f"Processing CSV file: {blob.name}")
            file = readCSVFile(blob)
            if blob.name == 'artists-data.csv':
                processArtist(file)
            else:
                processLyric(file)

if __name__ == "__main__":
    blobs = readGoogleCloudBucket()
    processBlobs(blobs)