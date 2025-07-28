from flask import Blueprint, request, jsonify
from src.services.equipment_service import EquipmentService
from src.decorators.auth_decorators import admin_required
from src.decorators.error_handlers import handle_integrity_error

equipment_blueprint = Blueprint('equipment', __name__)

def get_request_json_or_400():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Aucune donnée reçue'}), 400
    return data

@equipment_blueprint.route('/', methods=['GET'])
@admin_required
def get_all_equipments():
    return jsonify(EquipmentService.get_all_equipments()), 200

@equipment_blueprint.route('/<int:equipment_id>', methods=['GET'])
@admin_required
def get_equipment(equipment_id):
    equipment = EquipmentService.get_equipment_by_id(equipment_id)
    if equipment:
        return jsonify(equipment), 200
    return jsonify({'message': 'Equipment not found'}), 404

@equipment_blueprint.route('/', methods=['POST'])
@admin_required
@handle_integrity_error
def create_equipment():
    data = get_request_json_or_400()
    return jsonify(EquipmentService.create_equipment(data)), 201

@equipment_blueprint.route('/<int:equipment_id>', methods=['PUT'])
@admin_required
@handle_integrity_error
def update_equipment(equipment_id):
    data = get_request_json_or_400()
    updated = EquipmentService.update_equipment(equipment_id, data)
    if updated:
        return jsonify(updated), 200
    return jsonify({'message': "Équipement non trouvé"}), 404

@equipment_blueprint.route('/<int:equipment_id>', methods=['DELETE'])
@admin_required
def delete_equipment(equipment_id):
    if EquipmentService.delete_equipment(equipment_id):
        return jsonify({'message': 'Équipement supprimé'}), 200
    return jsonify({'message': 'Équipement non trouvé'}), 404

@equipment_blueprint.route('/unassigned', methods=['GET'])
@admin_required
def get_unassigned_equipments():
    return jsonify(EquipmentService.get_unassigned_equipments()), 200