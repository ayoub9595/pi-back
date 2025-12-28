from src import db
from sqlalchemy import Enum as SqlEnum
from enum import Enum
from datetime import datetime

from src.models.utilisateur import UserRole


class RegistrationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class RegistrationRequest(db.Model):
    __tablename__ = 'registration_requests'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    cin = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20), nullable=True)
    role = db.Column(SqlEnum(UserRole), nullable=False, default=UserRole.UTILISATEUR)
    status = db.Column(SqlEnum(RegistrationStatus), nullable=False, default=RegistrationStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    rejection_reason = db.Column(db.Text, nullable=True)

    reviewer = db.relationship('Utilisateur', foreign_keys=[reviewed_by])

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'cin': self.cin,
            'email': self.email,
            'telephone': self.telephone,
            'role': self.role.value,
            'status': self.status.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'reviewed_by': self.reviewed_by,
            'rejection_reason': self.rejection_reason
        }