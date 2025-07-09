from src import db
from sqlalchemy.orm import relationship

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    numero_serie = db.Column(db.String(50), unique=True)
    date_acquisition = db.Column(db.Date)
    maintenance_prevue = db.Column(db.Date)
    est_actif = db.Column(db.Boolean, default=True)

    caracteristiques = relationship(
        "CaracteristiqueEquipment", 
        back_populates="equipement",
        cascade="all, delete-orphan"
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'description': self.description,
            'numero_serie': self.numero_serie,
            'date_acquisition': self.date_acquisition.isoformat() if self.date_acquisition else None,
            'maintenance_prevue': self.maintenance_prevue.isoformat() if self.maintenance_prevue else None,
            'est_actif': self.est_actif,
            'caracteristiques': [c.to_dict() for c in self.caracteristiques]
        }

    def __repr__(self):
        return f'<Equipement {self.nom} (NS: {self.numero_serie})>'
