from utils.mongo import readDataMongo
from utils.elastic import indexCreation

# Main function, handles from reading the data to indexing it
def processDocuments():
    print("Creeating index")
    indexCreation()
    print("Index created")
    documentsN = readDataMongo("listingsAndReviews")
    print(f"Parsed {documentsN} documents")
    return documentsN