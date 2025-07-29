from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.services.reclamation_service import ReclamationService

reclamation_bp = Blueprint('reclamation', __name__)

@reclamation_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    try:
        reclamations = ReclamationService.lister_reclamations()
        return jsonify(reclamations), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@reclamation_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_by_id(id):
    try:
        reclamation = ReclamationService.recuperer_reclamation(id)
        return jsonify(reclamation), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@reclamation_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    try:
        reclamation = ReclamationService.creer_reclamation(data)
        return jsonify(reclamation), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
