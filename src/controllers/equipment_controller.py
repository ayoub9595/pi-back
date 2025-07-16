import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError

from src.services.equipment_service import EquipmentService

equipment_blueprint = Blueprint('equipment', __name__)
def is_admin():
    claims = get_jwt()
    return claims.get("role", "").upper() == "ADMIN"

@equipment_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_all_equipments():
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    equipments = EquipmentService.get_all_equipments()
    return jsonify(equipments)

@equipment_blueprint.route('/<int:equipment_id>', methods=['GET'])
@jwt_required()
def get_equipment(equipment_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    equipment = EquipmentService.get_equipment_by_id(equipment_id)
    if equipment:
        return jsonify(equipment)
    return jsonify({'message': 'Equipment not found'}), 404

@equipment_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_equipment():
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400
    try:
        equipment = EquipmentService.create_equipment(data)
        return jsonify(equipment), 201
    except IntegrityError:
        return jsonify({'error': 'Le numéro de série existe déjà.'}), 400
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@equipment_blueprint.route('/<int:equipment_id>', methods=['PUT'])
@jwt_required()
def update_equipment(equipment_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400
    try:
        equipment = EquipmentService.update_equipment(equipment_id, data)
        if equipment:
            return jsonify(equipment)
        return jsonify({'message': 'Équipement non trouvé'}), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@equipment_blueprint.route('/<int:equipment_id>', methods=['DELETE'])
@jwt_required()
def delete_equipment(equipment_id):
    if not is_admin():
        return jsonify({"msg": "Accès refusé : réservé aux administrateurs"}), 403
    if EquipmentService.delete_equipment(equipment_id):
        return jsonify({'message': 'Équipement supprimé'})
    return jsonify({'message': 'Équipement non trouvé'}), 404
