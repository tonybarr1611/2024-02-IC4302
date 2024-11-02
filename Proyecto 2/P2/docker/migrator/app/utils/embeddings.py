from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2')

# Generate embeddings for a given text
def generateEmbeddings(text):
    embedding = model.encode(text).tolist()
    return embedding