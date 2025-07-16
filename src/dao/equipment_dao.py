from typing import List, Optional
from src.models.equipment import Equipment
from .. import db

class EquipmentDAO:
    @staticmethod
    def get_all_equipments() -> List[Equipment]:
        return Equipment.query.all()
    
    @staticmethod
    def get_equipment_by_id(equipment_id: int) -> Optional[Equipment]:
        return Equipment.query.get(equipment_id)
    
    @staticmethod
    def create_equipment(equipment_data: dict) -> Equipment:
        equipment = Equipment(**equipment_data)
        db.session.add(equipment)
        db.session.flush()
        db.session.commit()
        return equipment
    
    @staticmethod
    def update_equipment(equipment_id: int, equipment_data: dict) -> Optional[Equipment]:
        equipment = Equipment.query.get(equipment_id)
        if equipment:
          for key, value in equipment_data.items():
            if key != "caracteristiques":
              setattr(equipment, key, value)
          db.session.commit()
        return equipment

    @staticmethod
    def delete_equipment(equipment_id: int) -> bool:
        equipment = Equipment.query.get(equipment_id)
        if equipment:
            db.session.delete(equipment)
            db.session.commit()
            return True
        return False