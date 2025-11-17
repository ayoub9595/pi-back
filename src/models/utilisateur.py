from enum import Enum
from sqlalchemy.orm import relationship
from src import db
from sqlalchemy import Enum as SqlEnum

class UserRole(Enum):
    ADMIN = "admin"
    UTILISATEUR = "utilisateur"

class Utilisateur(db.Model):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    cin = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    role = db.Column(SqlEnum(UserRole), nullable=False, default=UserRole.UTILISATEUR)
    affectations = relationship("Affectation", back_populates="utilisateur", cascade="all, delete-orphan")
    reclamations = relationship("Reclamation", back_populates="utilisateur", cascade="all, delete-orphan")


    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'cin': self.cin,
            'email': self.email,
            'telephone': self.telephone,
            'role': self.role.value.upper(),
        }

    def __repr__(self):
        return f"<Utilisateur {self.nom} - CIN: {self.cin} - Role: {self.role.value}>"
