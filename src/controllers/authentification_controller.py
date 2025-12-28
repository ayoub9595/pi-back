from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    create_access_token,
    jwt_required
)
from src.services.authentification_service import AuthentificationService
from src.services.registration_service import RegistrationService
from src.services.email_service import EmailService
from src.services.utilisateur_service import UtilisateurService

authentication_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@authentication_bp.route('/signup', methods=['POST'])
def signup():

    data = request.json
    try:
        result = RegistrationService.create_registration_request(data)

        # Notify User
        EmailService.envoyer_email_confirmation_inscription_user(data)

        # Notify Admins
        admins = UtilisateurService.lister_administrateurs()
        admin_emails = [admin.email for admin in admins if admin.email]
        EmailService.envoyer_email_nouvelle_inscription_admins(data, admin_emails)

        return jsonify(result), 202
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Erreur lors de la création : {str(e)}"}), 500


@authentication_bp.route('/login', methods=['POST'])
def login():

    data = request.json
    try:
        result = AuthentificationService.login_utilisateur(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500


@authentication_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    claims = get_jwt()

    new_access_token = create_access_token(
        identity=identity,
        additional_claims={
            "role": claims.get("role"),
            "email": claims.get("email"),
            "nom": claims.get("nom"),
        }
    )
    return jsonify(access_token=new_access_token), 200


@authentication_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    data = request.json

    if not data.get('ancien_mot_de_passe') or not data.get('nouveau_mot_de_passe'):
        return jsonify({"msg": "Ancien et nouveau mot de passe requis"}), 400

    try:
        AuthentificationService.changer_mot_de_passe(
            id_utilisateur=int(current_user_id),
            ancien_mot_de_passe=data['ancien_mot_de_passe'],
            nouveau_mot_de_passe=data['nouveau_mot_de_passe']
        )
        return jsonify({"msg": "Mot de passe changé avec succès"}), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500
