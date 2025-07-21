from src.models.affectation import Affectation
from src import db

class AffectationDAO:

    @staticmethod
    def get_all():
        return Affectation.query.all()

    @staticmethod
    def get_by_id(affectation_id):
        return Affectation.query.get(affectation_id)

    @staticmethod
    def create(id_equipement, id_utilisateur, date_debut, determine=False, date_fin=None):
      if not determine:
        date_fin = None

      affectation = Affectation(
        id_equipement=id_equipement,
        id_utilisateur=id_utilisateur,
        date_debut=date_debut,
        date_fin=date_fin,
        determine=determine
      )

      db.session.add(affectation)
      db.session.commit()
      return affectation


    @staticmethod
    def update(affectation_id, data):
      affectation = Affectation.query.get(affectation_id)
      if not affectation:
        return None

      affectation.id_equipement = data.get('id_equipement', affectation.id_equipement)
      affectation.id_utilisateur = data.get('id_utilisateur', affectation.id_utilisateur)
      affectation.date_debut = data.get('date_debut', affectation.date_debut)
      affectation.determine = data.get('determine', affectation.determine)


      if affectation.determine:
        affectation.date_fin = data.get('date_fin', affectation.date_fin)
      else:
        affectation.date_fin = None

      db.session.commit()
      return affectation

    @staticmethod
    def delete(affectation_id):
        affectation = Affectation.query.get(affectation_id)
        if not affectation:
            return False
        db.session.delete(affectation)
        db.session.commit()
        return True


