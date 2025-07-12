from src import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .equipment import Equipment

class CaracteristiqueEquipment(db.Model):
    __tablename__ = 'caracteristique_equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    id_equipement = db.Column(db.Integer, ForeignKey('equipment.id'), nullable=False)
    caracteristique = db.Column(db.String(255), nullable=False)
    valeur = db.Column(db.String(255))
    equipement = relationship(
        "Equipment", 
        back_populates="caracteristiques"
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_equipement': self.id_equipement,
            'caracteristique': self.caracteristique,
            'valeur': self.valeur
        }

    def __repr__(self):
        return f"<Caracteristique {self.caracteristique} (Valeur: {self.valeur}{self.unite_mesure})>"