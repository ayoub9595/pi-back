from typing import List, Optional, Dict
from src.dao.equipment_dao import EquipmentDAO
from src.services.caracteristique_service import CaracteristiqueEquipmentService
from src.dao.caracteristique_equipment_dao import CaracteristiqueEquipmentDAO 

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
    def update_equipment(equipment_id: int, data: Dict) -> Optional[Dict]:

        equipment = EquipmentDAO.update_equipment(equipment_id, data)
        if not equipment:
            return None
        if "caracteristiques" in data:
            CaracteristiqueEquipmentDAO.delete_by_equipement_id(equipment_id)
            for carac in data["caracteristiques"]:
                CaracteristiqueEquipmentDAO.create_caracteristique({
                    "id_equipement" : equipment_id,
                    "caracteristique" : carac["caracteristique"],
                    "valeur" : carac["valeur"]
                })
        return equipment.to_dict()
    
    @staticmethod
    def delete_equipment(equipment_id: int) -> bool:
        return EquipmentDAO.delete_equipment(equipment_id)