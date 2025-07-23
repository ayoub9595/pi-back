from flask import Blueprint, request, jsonify
from src.services.affectation_service import AffectationService
from flask_jwt_extended import jwt_required, get_jwt

affectation_bp = Blueprint('affectation', __name__)
def is_admin():
    claims = get_jwt()
    return claims.get("role", "").upper() == "ADMIN"

@affectation_bp.route('/', methods=['GET'])
@jwt_required()
def lister_affectations():
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    affectations = AffectationService.lister_affectations()
    return jsonify(affectations), 200

@affectation_bp.route('/<int:affectation_id>', methods=['GET'])
@jwt_required()
def recuperer_affectation(affectation_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    try:
        affectation = AffectationService.recuperer_affectation(affectation_id)
        return jsonify(affectation.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@affectation_bp.route('/', methods=['POST'])
@jwt_required()
def creer_affectation():
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    data = request.json
    data['determine'] = data.get('determine', False)
    try:
        affectation = AffectationService.creer_affectation(data)
        return jsonify(affectation.to_dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@affectation_bp.route('/<int:affectation_id>', methods=['PUT'])
@jwt_required()
def mettre_a_jour_affectation(affectation_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    data = request.json
    try:
        affectation = AffectationService.mettre_a_jour_affectation(affectation_id, data)
        return jsonify(affectation.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@affectation_bp.route('/<int:affectation_id>', methods=['DELETE'])
@jwt_required()
def supprimer_affectation(affectation_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    try:
        AffectationService.supprimer_affectation(affectation_id)
        return jsonify({"msg": "Affectation supprimée"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
