from datetime import datetime
from sqlalchemy.exc import IntegrityError

from src.dao.affectation_dao import AffectationDAO
from src.dao.equipment_dao import EquipmentDAO
from src.dao.reclamation_dao import ReclamationDAO
from src.models.equipment import Equipment
from src.models.utilisateur import Utilisateur

class ReclamationService:

    @staticmethod
    def _format_reclamation(r):
        return {
            'id': r.id,
            'id_utilisateur': r.id_utilisateur,
            'utilisateur': r.utilisateur.to_dict() if r.utilisateur else None,
            'id_equipement': r.id_equipement,
            'equipement': r.equipement.to_dict() if r.equipement else None,
            'description': r.description,
            'date_reclamation': r.date_reclamation.isoformat() if r.date_reclamation else None,
            'etat_reclamation': r.etat_reclamation,
            'commentaire': r.commentaire if r.commentaire else None,
        }

    @staticmethod
    def lister_reclamations():
        reclamations = ReclamationDAO.get_all()
        return [ReclamationService._format_reclamation(r) for r in reclamations]

    @staticmethod
    def recuperer_reclamation(reclamation_id):
        reclamation = ReclamationDAO.get_by_id(reclamation_id)
        if not reclamation:
            raise ValueError("Réclamation introuvable")
        return ReclamationService._format_reclamation(reclamation)

    @staticmethod
    def creer_reclamation(data):
        try:
            id_utilisateur = data['id_utilisateur']
            id_equipement = data['id_equipement']
            description = data['description']
        except KeyError as e:
            raise ValueError(f"Champ requis manquant : {e}")
        if not Utilisateur.query.get(id_utilisateur):
            raise ValueError("Utilisateur inexistant")
        if not Equipment.query.get(id_equipement):
            raise ValueError("Équipement inexistant")

        date_reclamation = datetime.utcnow()
        etat_reclamation = "Non traitée"

        try:
            reclamation = ReclamationDAO.create(
                id_utilisateur=id_utilisateur,
                id_equipement=id_equipement,
                description=description,
                date_reclamation=date_reclamation,
                etat_reclamation=etat_reclamation
            )
        except IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité de base de données: {str(e)}")

        return ReclamationService._format_reclamation(reclamation)

    @staticmethod
    def mettre_a_jour_reclamation(reclamation_id, data):
      reclamation = ReclamationDAO.get_by_id(reclamation_id)
      if not reclamation:
        raise ValueError("Réclamation introuvable")

      if 'id_utilisateur' in data:
        if not Utilisateur.query.get(data['id_utilisateur']):
            raise ValueError("Utilisateur inexistant")
      if 'id_equipement' in data:
        if not Equipment.query.get(data['id_equipement']):
            raise ValueError("Équipement inexistant")

      try:
        updated = ReclamationDAO.update(reclamation_id, data)
        if updated.etat_reclamation == 'Acceptée':
            EquipmentDAO.desactiver_equipement(updated.id_equipement)
            AffectationDAO.supprimer_par_utilisateur_et_equipement(updated.id_utilisateur, updated.id_equipement)
      except IntegrityError:
        raise ValueError("Erreur lors de la mise à jour")
      return ReclamationService._format_reclamation(updated)

    @staticmethod
    def supprimer_reclamation(reclamation_id):
        success = ReclamationDAO.delete(reclamation_id)
        if not success:
            raise ValueError("Réclamation introuvable")


    @staticmethod
    def lister_reclamations_par_utilisateur(utilisateur_id):
     reclamations = ReclamationDAO.get_by_utilisateur_id(utilisateur_id)
     return [ReclamationService._format_reclamation(r) for r in reclamations]

