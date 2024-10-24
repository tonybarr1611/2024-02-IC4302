from metrics import total_requests
from flask import Blueprint, request, jsonify
from utils import executeQuery, errResult, measure_processing_time

sample_bp = Blueprint('sample', __name__)

#############################################################
# Route localhost:31000/register: Used to register a new user
#############################################################
@sample_bp.route('/posgres/sample', methods=['GET'])
@measure_processing_time
def sample_route():
    return jsonify({'result': '200'})