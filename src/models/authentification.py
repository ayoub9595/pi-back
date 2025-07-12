from src import db
from sqlalchemy.orm import relationship

class Authentification(db.Model):
    __tablename__ = 'authentifications'
    id = db.Column(db.Integer, primary_key=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False, unique=True)
    mot_de_passe_hash = db.Column(db.String(256), nullable=False)
    utilisateur = db.relationship("Utilisateur", backref=db.backref("authentification", uselist=False))
