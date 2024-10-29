from flask import Blueprint, request, jsonify
from databases import elasticsearch_connection

apartments_bp = Blueprint('apartments', __name__)
es_client = elasticsearch_connection

@apartments_bp.route('/apartments/<apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apartment = es_client.get(index="listingsAndReviews", id=apartment_id)
    
    if apartment:
        return jsonify(apartment['_source'])
    else:
        return jsonify({"error": "Apartamento no encontrado"}), 404
