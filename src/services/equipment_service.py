from typing import List, Optional, Dict
from src.dao.equipment_dao import EquipmentDAO
from src.models.equipment import Equipment
from src.services.caracteristique_service import CaracteristiqueEquipmentService

class EquipmentService:
    @staticmethod
    def get_all_equipments() -> List[Dict]:
        equipments = EquipmentDAO.get_all_equipments()
        return [equipment.to_dict() for equipment in equipments]
    
    @staticmethod
    def get_equipment_by_id(equipment_id: int) -> Optional[Dict]:
        equipment = EquipmentDAO.get_equipment_by_id(equipment_id)
        return equipment.to_dict() if equipment else None
    
    @staticmethod
    def create_equipment(equipment_data: Dict) -> Dict:
        caracteristiques_data = equipment_data.pop("caracteristiques", [])

    
        equipment = EquipmentDAO.create_equipment(equipment_data)

        
        for carac in caracteristiques_data:
            carac_data = {
                "caracteristique": carac["caracteristique"],
                "valeur": carac["valeur"],
                "id_equipement": equipment.id 
            }
            CaracteristiqueEquipmentService.create_caracteristique(carac_data)

        return equipment.to_dict()
    
    @staticmethod
    def update_equipment(equipment_id: int, equipment_data: Dict) -> Optional[Dict]:
        equipment = EquipmentDAO.update_equipment(equipment_id, equipment_data)
        return equipment.to_dict() if equipment else None
    
    @staticmethod
    def delete_equipment(equipment_id: int) -> bool:
        return EquipmentDAO.delete_equipment(equipment_id)