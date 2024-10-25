from flask import Blueprint, request, jsonify
from databases import connect_to_postgres

apartments_bp = Blueprint('apartments', __name__)
es_client = connect_to_postgres() # Cambiar a elastic

@apartments_bp.route('/apartments/<apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apartment = es_client.get(index="apartments", id=apartment_id)
    
    if apartment:
        return jsonify(apartment['_source'])
    else:
        return jsonify({"error": "Apartamento no encontrado"}), 404
