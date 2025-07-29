from src.models.reclamation import Reclamation
from src import db

class ReclamationDAO:

    @staticmethod
    def get_all():
        return Reclamation.query.all()

    @staticmethod
    def get_by_id(reclamation_id):
        return Reclamation.query.get(reclamation_id)

    @staticmethod
    def create(id_utilisateur, id_equipement, description, date_reclamation=None,etat_reclamation="en attente"):
        reclamation = Reclamation(
            id_utilisateur=id_utilisateur,
            id_equipement=id_equipement,
            description=description,
            date_reclamation=date_reclamation,
            etat_reclamation=etat_reclamation
        )
        db.session.add(reclamation)
        db.session.commit()
        return reclamation

    @staticmethod
    def update(reclamation_id, data):
        reclamation = Reclamation.query.get(reclamation_id)
        if not reclamation:
            return None

        reclamation.id_utilisateur = data.get('id_utilisateur', reclamation.id_utilisateur)
        reclamation.id_equipement = data.get('id_equipement', reclamation.id_equipement)
        reclamation.description = data.get('description', reclamation.description)
        reclamation.date_reclamation = data.get('date_reclamation', reclamation.date_reclamation)
        reclamation.etat_reclamation = data.get('etat_reclamation', reclamation.etat_reclamation)

        db.session.commit()
        return reclamation

    @staticmethod
    def delete(reclamation_id):
        reclamation = Reclamation.query.get(reclamation_id)
        if not reclamation:
            return False

        db.session.delete(reclamation)
        db.session.commit()
        return True

    @staticmethod
    def get_by_utilisateur_id(utilisateur_id):
        return Reclamation.query.filter_by(id_utilisateur=utilisateur_id).all()

    @staticmethod
    def get_by_equipement_id(equipement_id):
        return Reclamation.query.filter_by(id_equipement=equipement_id).all()
