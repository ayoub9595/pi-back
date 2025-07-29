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

@reclamation_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        reclamation = ReclamationService.mettre_a_jour_reclamation(id, data)
        return jsonify(reclamation), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@reclamation_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
def get_reclamations_par_utilisateur(utilisateur_id):
    try:
        reclamations = ReclamationService.lister_reclamations_par_utilisateur(utilisateur_id)
        return jsonify(reclamations), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500