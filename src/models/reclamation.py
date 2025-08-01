from datetime import datetime
from src import db
from sqlalchemy.orm import relationship

class Reclamation(db.Model):
    __tablename__ = 'reclamations'

    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    id_equipement = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_reclamation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    etat_reclamation = db.Column(db.Text, nullable=False)
    commentaire = db.Column(db.Text, nullable=True)
    utilisateur = relationship("Utilisateur", back_populates="reclamations")
    equipement = relationship("Equipment", back_populates="reclamations")

    def to_dict(self):
        return {
            'id': self.id,
            'id_utilisateur': self.id_utilisateur,
            'id_equipement': self.id_equipement,
            'description': self.description,
            'date_reclamation': self.date_reclamation.isoformat(),
            'etat_reclamation': self.etat_reclamation,
            'commentaire': self.commentaire,
            'utilisateur': {
                'id': self.utilisateur.id if self.utilisateur else None,
                'nom': self.utilisateur.nom if self.utilisateur else "—"
            },
            'equipement': {
                'id': self.equipement.id if self.equipement else None,
                'nom': self.equipement.nom if self.equipement else "—"
            }
        }

    def __repr__(self):
        return f"<Reclamation {self.id} - Utilisateur {self.id_utilisateur} - Equipement {self.id_equipement}>"
