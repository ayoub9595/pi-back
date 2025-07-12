from flask import Blueprint
from flask_jwt_extended import create_access_token

authentication_bp = Blueprint('auth', __name__)

@authentication_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')

    if not email or not mot_de_passe:
        return jsonify({"msg": "Email et mot de passe requis"}), 400

    try:
        success, user = AuthentificationService.authentifier_utilisateur(email, mot_de_passe)
        if not success or not user:
            return jsonify({"msg": "Email ou mot de passe incorrect"}), 401

        access_token = create_access_token(identity={
            "id": user.id,
            "role": user.role.value,
            "email": user.email
        })
        return jsonify(access_token=access_token), 200

    except ValueError as e:
        return jsonify({"msg": str(e)}), 401

from flask import Blueprint, request, jsonify
from src.dao.utilisateur_dao import UtilisateurDAO
from src.services.authentification_service import AuthentificationService
from src.models.utilisateur import UserRole

auth_bp = Blueprint('auth', __name__)

@authentication_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    nom = data.get('nom')
    email = data.get('email')
    cin = data.get('cin')
    telephone = data.get('telephone')
    role = data.get('role', 'UTILISATEUR')
    mot_de_passe = data.get('mot_de_passe')

    if not all([nom, email, cin, telephone, mot_de_passe]):
        return jsonify({"msg": "Tous les champs sont obligatoires"}), 400

    # Vérifier doublons email ou cin
    if UtilisateurDAO.get_utilisateur_by_email(email) or UtilisateurDAO.get_utilisateur_by_cin(cin):
        return jsonify({"msg": "Email ou CIN déjà utilisé"}), 409

    try:
        # Créer l'utilisateur
        utilisateur = UtilisateurDAO.create_utilisateur(
            nom=nom,
            email=email,
            cin=cin,
            telephone=telephone,
            role=UserRole[role.upper()]
        )

        # Créer le compte d'authentification avec mot de passe hashé
        AuthentificationService.creer_compte(utilisateur.id, mot_de_passe)

        # Create access token similar to login endpoint
        access_token = create_access_token(identity={
            "id": utilisateur.id,
            "role": utilisateur.role.value,
            "email": utilisateur.email
        })

        return jsonify({
            "msg": "Utilisateur créé avec succès",
            "access_token": access_token
        }), 201

    except Exception as e:
        return jsonify({"msg": f"Erreur lors de la création : {str(e)}"}), 500

