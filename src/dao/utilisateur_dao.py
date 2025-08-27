from src import db
from src.models.utilisateur import Utilisateur

class UtilisateurDAO:

    @staticmethod
    def create_utilisateur(nom, cin,email, telephone, role):
        utilisateur = Utilisateur(
            nom=nom,
            cin=cin,
            email=email,
            telephone=telephone,
            role=role
        )
        db.session.add(utilisateur)
        db.session.commit()
        return utilisateur

    @staticmethod
    def get_all_utilisateurs():
        return Utilisateur.query.all()

    @staticmethod
    def get_utilisateur_by_id(utilisateur_id):
        return Utilisateur.query.get(utilisateur_id)

    @staticmethod
    def get_utilisateur_by_cin(cin):
        return Utilisateur.query.filter_by(cin=cin).first()
    @staticmethod
    def get_utilisateur_by_email(email):
        return Utilisateur.query.filter_by(email=email).first()

    @staticmethod
    def update_utilisateur(utilisateur_id, nom=None, cin=None, telephone=None, role=None):
        utilisateur = Utilisateur.query.get(utilisateur_id)
        if not utilisateur:
            return None

        if nom is not None:
            utilisateur.nom = nom
        if cin is not None:
            utilisateur.cin = cin
        if telephone is not None:
            utilisateur.telephone = telephone
        if role is not None:
            utilisateur.role = role

        db.session.commit()
        return utilisateur

    @staticmethod
    def delete_utilisateur(utilisateur_id):
        utilisateur = Utilisateur.query.get(utilisateur_id)
        if not utilisateur:
            return False

        db.session.delete(utilisateur)
        db.session.commit()
        return True
    @staticmethod
    def get_utilisateurs_by_role(role):
        return Utilisateur.query.filter_by(role=role).all()