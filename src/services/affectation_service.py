from datetime import datetime
from sqlalchemy.exc import IntegrityError
from src.models.equipment import Equipment
from src.models.utilisateur import Utilisateur
from src.dao.affectation_dao import AffectationDAO

class AffectationService:

    @staticmethod
    def lister_affectations():
      affectations = AffectationDAO.get_all()
      result = []
      for a in affectations:
        result.append({
            'id': a.id,
            'id_equipement': a.id_equipement,
            'nom_equipement': a.equipement.nom if a.equipement else None,
            'id_utilisateur': a.id_utilisateur,
            'nom_utilisateur': a.utilisateur.nom if a.utilisateur else None,
            'date_debut': a.date_debut.isoformat() if a.date_debut else None,
            'date_fin': a.date_fin.isoformat() if a.date_fin else None,
            'determine': a.determine
        })
      return result

    @staticmethod
    def recuperer_affectation(affectation_id):
        affectation = AffectationDAO.get_by_id(affectation_id)
        if not affectation:
            raise ValueError("Affectation introuvable")
        return affectation


    @staticmethod
    def creer_affectation(data):
        try:
            id_equipement = data['id_equipement']
            id_utilisateur = data['id_utilisateur']
            date_debut = datetime.fromisoformat(data['date_debut'])
            determine = data.get('determine', False)
            date_fin = None
            if determine:
                date_fin = datetime.fromisoformat(data['date_fin']) if data.get('date_fin') else None
        except KeyError as e:
            raise ValueError(f"Champ requis manquant : {e}")
        except (ValueError, TypeError):
            raise ValueError("Format de date invalide")

        if not Equipment.query.get(id_equipement):
            raise ValueError("Équipement inexistant")
        if not Utilisateur.query.get(id_utilisateur):
            raise ValueError("Utilisateur inexistant")

        try:
            affectation = AffectationDAO.create(
                id_equipement=id_equipement,
                id_utilisateur=id_utilisateur,
                date_debut=date_debut,
                date_fin=date_fin,
                determine=determine
            )
        except IntegrityError:
            raise ValueError("Erreur d'intégrité lors de la création")
        return affectation

    @staticmethod
    def mettre_a_jour_affectation(affectation_id, data):
        affectation = AffectationDAO.get_by_id(affectation_id)
        if not affectation:
            raise ValueError("Affectation introuvable")

        if 'id_equipement' in data:
            if not Equipment.query.get(data['id_equipement']):
                raise ValueError("Équipement inexistant")
        if 'id_utilisateur' in data:
            if not Utilisateur.query.get(data['id_utilisateur']):
                raise ValueError("Utilisateur inexistant")

        if 'date_debut' in data:
            try:
                data['date_debut'] = datetime.fromisoformat(data['date_debut'])
            except ValueError:
                raise ValueError("Format date_debut invalide")
        if 'date_fin' in data:
            try:
                data['date_fin'] = datetime.fromisoformat(data['date_fin']) if data['date_fin'] else None
            except ValueError:
                raise ValueError("Format date_fin invalide")

        try:
            updated = AffectationDAO.update(affectation_id, data)
        except IntegrityError:
            raise ValueError("Erreur d'intégrité lors de la mise à jour")

        return updated

    @staticmethod
    def supprimer_affectation(affectation_id):
        success = AffectationDAO.delete(affectation_id)
        if not success:
            raise ValueError("Affectation introuvable")
