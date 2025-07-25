from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from src.decorators.auth_decorators import admin_required
from src.services.affectation_service import AffectationService

affectation_bp = Blueprint('affectation', __name__)


@affectation_bp.route('/', methods=['GET'])
@admin_required
def lister_affectations():
    affectations = AffectationService.lister_affectations()
    return jsonify(affectations), 200

@affectation_bp.route('/<int:affectation_id>', methods=['GET'])
@admin_required
def recuperer_affectation(affectation_id):
    try:
        affectation = AffectationService.recuperer_affectation(affectation_id)
        return jsonify(affectation), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@affectation_bp.route('/', methods=['POST'])
@admin_required
def creer_affectation():
    data = request.json
    data['determine'] = data.get('determine', False)
    try:
        affectation = AffectationService.creer_affectation(data)
        return jsonify(affectation), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@affectation_bp.route('/<int:affectation_id>', methods=['PUT'])
@admin_required
def mettre_a_jour_affectation(affectation_id):
    data = request.json
    try:
        affectation = AffectationService.mettre_a_jour_affectation(affectation_id, data)
        return jsonify(affectation), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@affectation_bp.route('/<int:affectation_id>', methods=['DELETE'])
@admin_required
def supprimer_affectation(affectation_id):
    try:
        AffectationService.supprimer_affectation(affectation_id)
        return jsonify({"msg": "Affectation supprimée"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@affectation_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
def get_affectations_utilisateur(utilisateur_id):
    jwt_data = get_jwt()
    role = jwt_data.get('role')
    sub = jwt_data.get('sub')
    if role != "ADMIN" and sub != str(utilisateur_id):
        return jsonify({"msg": "Accès refusé"}), 403
    affectations = AffectationService.lister_affectations_par_utilisateur(utilisateur_id)
    return jsonify(affectations), 200