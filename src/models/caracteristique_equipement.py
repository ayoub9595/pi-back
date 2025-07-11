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
    unite_mesure = db.Column(db.String(20))
    est_important = db.Column(db.Boolean, default=False)
    equipement = relationship(
        "Equipment", 
        back_populates="caracteristiques"
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_equipement': self.id_equipement,
            'caracteristique': self.caracteristique,
            'valeur': self.valeur,
            'unite_mesure': self.unite_mesure,
            'est_important': self.est_important
        }

    def __repr__(self):
        return f"<Caracteristique {self.caracteristique} (Valeur: {self.valeur}{self.unite_mesure})>"