from typing import List, Optional
from src.models.caracteristique_equipment import CaracteristiqueEquipment
from src import db

class CaracteristiqueEquipmentDAO:
    @staticmethod
    def get_all_caracteristiques() -> List[CaracteristiqueEquipment]:
        return CaracteristiqueEquipment.query.all()

    @staticmethod
    def get_caracteristique_by_id(caracteristique_id: int) -> Optional[CaracteristiqueEquipment]:
        return CaracteristiqueEquipment.query.get(caracteristique_id)

    @staticmethod
    def create_caracteristique(caracteristique_data: dict) -> CaracteristiqueEquipment:
        carac = CaracteristiqueEquipment(**caracteristique_data)
        db.session.add(carac)
        db.session.commit()
        return carac

    @staticmethod
    def update_caracteristique(caracteristique_id: int, caracteristique_data: dict) -> Optional[CaracteristiqueEquipment]:
        carac = CaracteristiqueEquipment.query.get(caracteristique_id)
        if carac:
            for key, value in caracteristique_data.items():
                setattr(carac, key, value)
            db.session.commit()
        return carac

    @staticmethod
    def delete_caracteristique(caracteristique_id: int) -> bool:
        carac = CaracteristiqueEquipment.query.get(caracteristique_id)
        if carac:
            db.session.delete(carac)
            db.session.commit()
            return True
        return False
