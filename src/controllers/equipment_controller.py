import traceback
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError

from src.decorators.auth_decorators import admin_required
from src.services.equipment_service import EquipmentService

equipment_blueprint = Blueprint('equipment', __name__)


@equipment_blueprint.route('/', methods=['GET'])
@admin_required
def get_all_equipments():
    equipments = EquipmentService.get_all_equipments()
    return jsonify(equipments)

@equipment_blueprint.route('/<int:equipment_id>', methods=['GET'])
@admin_required
def get_equipment(equipment_id):
    equipment = EquipmentService.get_equipment_by_id(equipment_id)
    if equipment:
        return jsonify(equipment)
    return jsonify({'message': 'Equipment not found'}), 404

@equipment_blueprint.route('/', methods=['POST'])
@admin_required
def create_equipment():
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
@admin_required
def update_equipment(equipment_id):
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
@admin_required
def delete_equipment(equipment_id):
    if EquipmentService.delete_equipment(equipment_id):
        return jsonify({'message': 'Équipement supprimé'})
    return jsonify({'message': 'Équipment non trouvé'}), 404

@equipment_blueprint.route('/unassigned', methods=['GET'])
@admin_required
def get_unassigned_equipments():
    try:
        equipments = EquipmentService.get_unassigned_equipments()
        return jsonify(equipments), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500