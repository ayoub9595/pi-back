from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    create_access_token,
    create_refresh_token,
    jwt_required
)
from src.services.authentification_service import AuthentificationService
from src.services.email_service import EmailService


authentication_bp = Blueprint('auth', __name__)


@authentication_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        result = AuthentificationService.inscrire_utilisateur(data)
        return jsonify(result), 201
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
            "email": claims.get("email")
        }
    )
    return jsonify(access_token=new_access_token), 200
@authentication_bp.route('/test-email', methods=['GET'])
def test_email():
    try:
        EmailService.envoyer_email(
            subject="Test SMTP avec Flask",
            recipients=["badiamohamedaymane@gmail.com"],
            body="Bonjour,\n\nCeci est un test d'email depuis votre application Flask."
        )
        return jsonify({"msg": "Email envoyé avec succès"}), 200
    except Exception as e:
        return jsonify({"msg": f"Erreur lors de l'envoi : {str(e)}"}), 500
