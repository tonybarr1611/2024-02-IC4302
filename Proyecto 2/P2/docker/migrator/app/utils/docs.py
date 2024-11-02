from utils.embeddings import generateEmbeddings
from datetime import datetime

# Generates embeddings for the documents where needed
def generateDocumentEmbeddings(doc: dict):
    print("Generating embeddings for document")
    name_embedding = generateEmbeddings(doc.get("name") or "")
    summary_embedding = generateEmbeddings(doc.get("summary") or "")
    description_embedding = generateEmbeddings(doc.get("description") or "")

    reviews = doc.get("reviews")
    reviews_embeddings = []
    if reviews:
        for review in reviews:
            review_embedding = generateEmbeddings(review.get("comments") or "")
            reviews_embeddings.append({'embedding': review_embedding})

    doc["name_embedding"] = name_embedding
    doc["summary_embedding"] = summary_embedding
    doc["description_embedding"] = description_embedding
    doc["reviews_embeddings"] = reviews_embeddings

    return doc

# Makes the document serializable
def serializableDoc(doc: dict):
    serializable = doc.copy()
    for key, value in serializable.items():
        if isinstance(value, datetime):
            serializable[key] = value.isoformat()
    return serializable