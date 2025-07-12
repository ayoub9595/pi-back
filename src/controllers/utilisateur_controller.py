from flask import Blueprint, request, jsonify
from src.services.utilisateur_service import UtilisateurService

utilisateur_bp = Blueprint('utilisateur', __name__)

@utilisateur_bp.route('/', methods=['GET'])
def lister_utilisateurs():
    utilisateurs = UtilisateurService.lister_utilisateurs()
    return jsonify([u.to_dict() for u in utilisateurs]), 200


@utilisateur_bp.route('/<int:utilisateur_id>', methods=['GET'])
def recuperer_utilisateur(utilisateur_id):
    try:
        utilisateur = UtilisateurService.recuperer_utilisateur(utilisateur_id)
        return jsonify(utilisateur.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@utilisateur_bp.route('/', methods=['POST'])
def creer_utilisateur():
    data = request.json
    try:
        utilisateur = UtilisateurService.creer_utilisateur(data)
        return jsonify(utilisateur.to_dict()), 201
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400


@utilisateur_bp.route('/', methods=['PUT'])
def mettre_a_jour_utilisateur(utilisateur_id):
    data = request.json
    try:
        utilisateur = UtilisateurService.mettre_a_jour_utilisateur(utilisateur_id, data)
        return jsonify(utilisateur.to_dict()), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404


@utilisateur_bp.route('/<int:utilisateur_id>', methods=['DELETE'])
def supprimer_utilisateur(utilisateur_id):
    try:
        UtilisateurService.supprimer_utilisateur(utilisateur_id)
        return jsonify({"msg": "Utilisateur supprimé"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 404
