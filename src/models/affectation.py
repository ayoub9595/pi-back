from datetime import datetime
from src import db
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint

class Affectation(db.Model):
    __tablename__ = 'affectations'

    id = db.Column(db.Integer, primary_key=True)
    id_equipement = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_fin = db.Column(db.DateTime, nullable=True)
    determine = db.Column(db.Boolean, default=False, nullable=False)  # <== Nouveau champ

    equipement = relationship("Equipment", back_populates="affectations")
    utilisateur = relationship("Utilisateur", back_populates="affectations")

    @property
    def duree(self):
        if self.date_debut and self.date_fin:
            return (self.date_fin - self.date_debut).days
        return None

    @property
    def est_active(self):
        return self.date_fin is None

    def set_date_fin(self, date):
        if not self.determine:
            raise ValueError("Impossible d'ajouter une date de fin car cette affectation n'est pas déterminée.")
        self.date_fin = date

    def to_dict(self):
        return {
            'id': self.id,
            'id_equipement': self.id_equipement,
            'id_utilisateur': self.id_utilisateur,
            'date_debut': self.date_debut.isoformat() if self.date_debut else None,
            'date_fin': self.date_fin.isoformat() if self.date_fin else None,
            'determine': self.determine,
        }

    def __repr__(self):
        return f"<Affectation Equipement {self.id_equipement} à Utilisateur {self.id_utilisateur}>"
