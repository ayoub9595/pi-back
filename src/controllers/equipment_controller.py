from flask import Blueprint, request, jsonify
from src.services.equipment_service import EquipmentService

equipment_blueprint = Blueprint('equipment', __name__)

@equipment_blueprint.route('/', methods=['GET'])
def get_all_equipments():
    equipments = EquipmentService.get_all_equipments()
    return jsonify(equipments)

@equipment_blueprint.route('/<int:equipment_id>', methods=['GET'])
def get_equipment(equipment_id):
    equipment = EquipmentService.get_equipment_by_id(equipment_id)
    if equipment:
        return jsonify(equipment)
    return jsonify({'message': 'Equipment not found'}), 404

@equipment_blueprint.route('/', methods=['POST'])
def create_equipment():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    
    equipment = EquipmentService.create_equipment(data)
    return jsonify(equipment), 201

@equipment_blueprint.route('/', methods=['PUT'])
def update_equipment():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'message': 'No input data or ID provided'}), 400
    
    equipment_id = data.pop('id')
    equipment = EquipmentService.update_equipment(equipment_id, data)
    if equipment:
        return jsonify(equipment)
    return jsonify({'message': 'Equipment not found'}), 404


@equipment_blueprint.route('/<int:equipment_id>', methods=['DELETE'])
def delete_equipment(equipment_id):
    if EquipmentService.delete_equipment(equipment_id):
        return jsonify({'message': 'Equipment deleted'})
    return jsonify({'message': 'Equipment not found'}), 404