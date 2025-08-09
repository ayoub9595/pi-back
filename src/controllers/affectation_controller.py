from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from src.services.affectation_service import AffectationService
from src.decorators.auth_decorators import admin_required, admin_or_self_required
from src.decorators.error_handlers import handle_value_error
from src.services.email_service import EmailService
from src.services.caracteristique_service import CaracteristiqueEquipmentService

affectation_bp = Blueprint('affectation', __name__)

@affectation_bp.route('/', methods=['GET'])
@admin_required
def lister_affectations():
    return jsonify(AffectationService.lister_affectations()), 200

@affectation_bp.route('/<int:affectation_id>', methods=['GET'])
@admin_required
@handle_value_error
def recuperer_affectation(affectation_id):
    return jsonify(AffectationService.recuperer_affectation(affectation_id)), 200

@affectation_bp.route('/', methods=['POST'])
@admin_required
@handle_value_error
def creer_affectation():
    data = request.json or {}
    return jsonify(AffectationService.creer_affectation(data)), 201

@affectation_bp.route('/<int:affectation_id>', methods=['PUT'])
@admin_required
@handle_value_error
def mettre_a_jour_affectation(affectation_id):
    return jsonify(AffectationService.mettre_a_jour_affectation(affectation_id, request.json)), 200

@affectation_bp.route('/<int:affectation_id>', methods=['DELETE'])
@admin_required
@handle_value_error
def supprimer_affectation(affectation_id):
    AffectationService.supprimer_affectation(affectation_id)
    return jsonify({"msg": "Affectation supprimée"}), 200

@affectation_bp.route('/utilisateur/<int:utilisateur_id>', methods=['GET'])
@jwt_required()
@admin_or_self_required()
def get_affectations_utilisateur(utilisateur_id):
    affectations = AffectationService.lister_affectations_par_utilisateur(utilisateur_id)
    return jsonify(affectations), 200
