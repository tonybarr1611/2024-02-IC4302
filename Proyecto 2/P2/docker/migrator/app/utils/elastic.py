import json
import os
from elasticsearch import Elasticsearch

ELASTIC_URL = os.getenv("ELASTIC")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASS = os.getenv("ELASTIC_PASSWORD")
ELASTIC_INDEX_NAME = os.getenv("ELASTIC_INDEX_NAME")

# Ensures only one connection to Elasticsearch is made
class ElasticsearchSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                if ELASTIC_URL:
                    cls._instance = Elasticsearch(
                        [ELASTIC_URL],
                        basic_auth=(ELASTIC_USER, ELASTIC_PASS)
                    )
                else:
                    print("Elasticsearch URL not provided")
                    os._exit(1)
            except Exception as e:
                print(f"Error creating Elasticsearch connection: {e}")
                os._exit(1)
        return cls._instance

# Gives a connection to the Elasticsearch database
def getESConnection():
    return ElasticsearchSingleton()

# Initializes the index with the correct mapping
def indexCreation():
    es = getESConnection()
    mapping = {
        "mappings": {
            "properties": {
                "_id": {"type": "keyword"},
                "listing_url": {"type": "keyword"},
                "name": {"type": "text"},
                "summary": {"type": "text"},
                "interaction": {"type": "text"},
                "house_rules": {"type": "text"},
                "property_type": {"type": "keyword"},
                "room_type": {"type": "keyword"},
                "bed_type": {"type": "keyword"},
                "minimum_nights": {"type": "integer"},
                "maximum_nights": {"type": "integer"},
                "cancellation_policy": {"type": "keyword"},
                "last_scraped": {"type": "date"},
                "calendar_last_scraped": {"type": "date"},
                "first_review": {"type": "date"},
                "last_review": {"type": "date"},
                "accommodates": {"type": "integer"},
                "bedrooms": {"type": "integer"},
                "beds": {"type": "integer"},
                "number_of_reviews": {"type": "integer"},
                "bathrooms": {"type": "float"},
                "amenities": {"type": "keyword"},
                "price": {"type": "float"},
                "security_deposit": {"type": "float"},
                "cleaning_fee": {"type": "float"},
                "extra_people": {"type": "float"},
                "guests_included": {"type": "integer"},
                "images": {
                    "properties": {
                        "thumbnail_url": {"type": "keyword"},
                        "medium_url": {"type": "keyword"},
                        "picture_url": {"type": "keyword"},
                        "xl_picture_url": {"type": "keyword"},
                    }
                },
                "host": {
                    "properties": {
                        "host_id": {"type": "keyword"},
                        "host_url": {"type": "keyword"},
                        "host_name": {"type": "text"},
                        "host_location": {"type": "text"},
                        "host_about": {"type": "text"},
                        "host_response_time": {"type": "keyword"},
                        "host_thumbnail_url": {"type": "keyword"},
                        "host_picture_url": {"type": "keyword"},
                        "host_neighbourhood": {"type": "text"},
                        "host_response_rate": {"type": "integer"},
                        "host_is_superhost": {"type": "boolean"},
                        "host_has_profile_pic": {"type": "boolean"},
                        "host_identity_verified": {"type": "boolean"},
                        "host_listings_count": {"type": "integer"},
                        "host_total_listings_count": {"type": "integer"},
                        "host_verifications": {"type": "keyword"},
                    }
                },
                "address": {
                    "properties": {
                        "street": {"type": "text"},
                        "suburb": {"type": "text"},
                        "government_area": {"type": "text"},
                        "market": {"type": "text"},
                        "country": {"type": "keyword"},
                        "country_code": {"type": "keyword"},
                        "location": {
                            "properties": {
                                "type": {"type": "keyword"},
                                "coordinates": {"type": "geo_point"},
                                "is_location_exact": {"type": "boolean"},
                            }
                        },
                    }
                },
                "availability": {
                    "properties": {
                        "availability_30": {"type": "integer"},
                        "availability_60": {"type": "integer"},
                        "availability_90": {"type": "integer"},
                        "availability_365": {"type": "integer"},
                    }
                },
                "review_scores": {
                    "properties": {
                        "review_scores_accuracy": {"type": "integer"},
                        "review_scores_cleanliness": {"type": "integer"},
                        "review_scores_checkin": {"type": "integer"},
                        "review_scores_communication": {"type": "integer"},
                        "review_scores_location": {"type": "integer"},
                        "review_scores_value": {"type": "integer"},
                        "review_scores_rating": {"type": "integer"},
                    }
                },
                "reviews": {
                    "type": "nested",
                    "properties": {
                        "_id": {"type": "keyword"},
                        "date": {"type": "date"},
                        "listing_id": {"type": "keyword"},
                        "reviewer_id": {"type": "keyword"},
                        "reviewer_name": {"type": "text"},
                        "comments": {"type": "text"},
                    },
                },
                "name_embedding": {"type": "dense_vector", "dims": 768},
                "summary_embedding": {"type": "dense_vector", "dims": 768},
                "description_embedding": {"type": "dense_vector", "dims": 768},
                "reviews_embeddings": {
                    "type": "nested",
                    "properties": {
                        "embedding": {"type": "dense_vector", "dims": 768}
                    }
                }
            }
        }
    }

    if not es.indices.exists(index=ELASTIC_INDEX_NAME):
        es.indices.create(index=ELASTIC_INDEX_NAME, body=mapping)
    return

# Indexes a document in Elasticsearch
def indexDocument(doc: dict):
    es = getESConnection()
    # Change the _id field to id, as Elasticsearch does not accept _id
    doc["id"] = doc.pop("_id")
    # Parse the document to be a JSON
    doc = json.dumps(doc, default=str)
    response = es.index(index=ELASTIC_INDEX_NAME, body=doc)
    return response