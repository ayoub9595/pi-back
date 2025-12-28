from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.decorators.auth_decorators import admin_required
from src.services.registration_service import RegistrationService

registration_bp = Blueprint('registration', __name__, url_prefix='/api/registrations')

@registration_bp.route('', methods=['GET'])
@jwt_required()
@admin_required
def get_all_requests():

    status = request.args.get('status')

    try:
        requests = (RegistrationService.get_requests_by_status(status)
                    if status
                    else RegistrationService.get_all_requests())

        return jsonify([req.to_dict() for req in requests]), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500


@registration_bp.route('/<int:request_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_request_by_id(request_id):
    try:
        reg_request = RegistrationService.get_request_by_id(request_id)
        if not reg_request:
            return jsonify({"msg": "Demande d'inscription introuvable"}), 404

        return jsonify(reg_request.to_dict()), 200
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500


@registration_bp.route('/<int:request_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_request(request_id):

    data = request.get_json()

    if not data:
        return jsonify({"msg": "Données de mise à jour requises"}), 400

    try:
        current_user_id = get_jwt_identity()
        updated_request = RegistrationService.update_registration_request(
            request_id=request_id,
            admin_id=current_user_id,
            update_data=data
        )

        return jsonify({
            "msg": "Demande mise à jour avec succès",
            "request": updated_request
        }), 200
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500


@registration_bp.route('/<int:request_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_request(request_id):
    """Delete a registration request"""
    try:
        success = RegistrationService.delete_request(request_id)
        if not success:
            return jsonify({"msg": "Demande introuvable"}), 404

        return jsonify({"msg": "Demande supprimée avec succès"}), 200
    except Exception as e:
        return jsonify({"msg": f"Erreur serveur : {str(e)}"}), 500