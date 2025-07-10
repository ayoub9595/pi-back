from typing import List, Optional, Dict
from src.dao.caracteristique_equipment_dao import CaracteristiqueEquipmentDAO
from src.models.caracteristique_equipement import CaracteristiqueEquipment

class CaracteristiqueEquipmentService:
    @staticmethod
    def get_all_caracteristiques() -> List[Dict]:
        caracteristiques = CaracteristiqueEquipmentDAO.get_all_caracteristiques()
        return [carac.to_dict() for carac in caracteristiques]
    
    @staticmethod
    def get_caracteristique_by_id(caracteristique_id: int) -> Optional[Dict]:
        carac = CaracteristiqueEquipmentDAO.get_caracteristique_by_id(caracteristique_id)
        return carac.to_dict() if carac else None
    @staticmethod
    def create_caracteristique(caracteristique_data: Dict) -> Dict:
        carac = CaracteristiqueEquipmentDAO.create_caracteristique(caracteristique_data)
        return carac.to_dict()
    
    @staticmethod
    def update_caracteristique(caracteristique_id: int, caracteristique_data: Dict) -> Optional[Dict]:
        carac = CaracteristiqueEquipmentDAO.update_caracteristique(caracteristique_id, caracteristique_data)
        return carac.to_dict() if carac else None

    @staticmethod
    def delete_caracteristique(caracteristique_id: int) -> bool:
        return CaracteristiqueEquipmentDAO.delete_caracteristique(caracteristique_id)
