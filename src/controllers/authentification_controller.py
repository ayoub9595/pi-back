from flask import Blueprint, request, jsonify
from src.services.authentification_service import AuthentificationService

authentication_bp = Blueprint('auth', __name__)

@authentication_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    try:
        access_token = AuthentificationService.login_utilisateur(data)
        return jsonify(access_token=access_token), 200

    except ValueError as e:
        return jsonify({"msg": str(e)}), 401
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500





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

