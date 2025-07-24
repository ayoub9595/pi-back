from functools import wraps
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.services.affectation_service import AffectationService

affectation_bp = Blueprint('affectation', __name__)

def admin_required(f):
    """Decorator that combines JWT authentication and admin role checking"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role", "").upper() != "ADMIN":
            return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
        return f(*args, **kwargs)
    return decorated_function

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
        return jsonify(affectation.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404

@affectation_bp.route('/', methods=['POST'])
@admin_required
def creer_affectation():
    data = request.json
    data['determine'] = data.get('determine', False)
    try:
        affectation = AffectationService.creer_affectation(data)
        return jsonify(affectation.to_dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400

@affectation_bp.route('/<int:affectation_id>', methods=['PUT'])
@admin_required
def mettre_a_jour_affectation(affectation_id):
    data = request.json
    try:
        affectation = AffectationService.mettre_a_jour_affectation(affectation_id, data)
        return jsonify(affectation.to_dict()), 200
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