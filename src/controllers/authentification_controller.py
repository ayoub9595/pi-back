from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    get_jwt,
    create_access_token,
    jwt_required
)
from src.services.authentification_service import AuthentificationService

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