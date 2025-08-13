from datetime import datetime
from sqlalchemy.exc import IntegrityError
from src.models.equipment import Equipment
from src.models.utilisateur import Utilisateur
from src.dao.affectation_dao import AffectationDAO
from src.services.caracteristique_service import CaracteristiqueEquipmentService
from src.services.email_service import EmailService


class AffectationService:

    @staticmethod
    def _format_affectation(a):
        return {
            'id': a.id,
            'id_equipement': a.id_equipement,
            'equipement': a.equipement.to_dict() if a.equipement else None,
            'id_utilisateur': a.id_utilisateur,
            'utilisateur': a.utilisateur.to_dict() if a.utilisateur else None,
            'date_debut': a.date_debut.isoformat() if a.date_debut else None,
            'date_fin': a.date_fin.isoformat() if a.date_fin else None,
            'determine': a.determine
        }

    @staticmethod
    def lister_affectations():
        affectations = AffectationDAO.get_all()
        return [AffectationService._format_affectation(a) for a in affectations]

    @staticmethod
    def recuperer_affectation(affectation_id):
        affectation = AffectationDAO.get_by_id(affectation_id)
        if not affectation:
            raise ValueError("Affectation introuvable")
        return AffectationService._format_affectation(affectation)

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

        equipement = Equipment.query.get(id_equipement)
        if not equipement:
            raise ValueError("Équipement inexistant")

        utilisateur = Utilisateur.query.get(id_utilisateur)
        if not utilisateur:
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

        caracteristiques = CaracteristiqueEquipmentService.get_by_equipment_id(equipement.id)


        affectation_dict = {
            "id": affectation.id,
            "date_debut": affectation.date_debut.isoformat() if affectation.date_debut else None,
            "date_fin": affectation.date_fin.isoformat() if affectation.date_fin else None,
            "determine": affectation.determine,
            "utilisateur": utilisateur.to_dict(),
            "equipement": equipement.to_dict()
        }

        affectation_dict["equipement"]["caracteristiques"] = caracteristiques

        EmailService.envoyer_email_affectation(
            affectation=affectation_dict,
            recipient_email=utilisateur.email,
            action="creation"
        )

        return AffectationService._format_affectation(affectation)

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


        equipement = updated.equipement
        utilisateur = updated.utilisateur
        caracteristiques = CaracteristiqueEquipmentService.get_by_equipment_id(equipement.id) if equipement else []

        affectation_dict = {
            "id": updated.id,
            "date_debut": updated.date_debut.isoformat() if updated.date_debut else None,
            "date_fin": updated.date_fin.isoformat() if updated.date_fin else None,
            "determine": updated.determine,
            "utilisateur": utilisateur.to_dict() if utilisateur else None,
            "equipement": equipement.to_dict() if equipement else None
        }
        if affectation_dict.get("equipement"):
            affectation_dict["equipement"]["caracteristiques"] = caracteristiques


        EmailService.envoyer_email_affectation(
            affectation=affectation_dict,
            recipient_email=utilisateur.email if utilisateur else None,
            action="modification"
        )

        return AffectationService._format_affectation(updated)
    @staticmethod
    def supprimer_affectation(affectation_id):
        affectation = AffectationDAO.get_by_id(affectation_id)
        if not affectation:
            raise ValueError("Affectation introuvable")

        affectation_dict = AffectationService._format_affectation(affectation)

        if affectation_dict.get("equipement"):
            equip_id = affectation_dict["equipement"]["id"]
            affectation_dict["equipement"]["caracteristiques"] = CaracteristiqueEquipmentService.get_by_equipment_id(equip_id)

        success = AffectationDAO.delete(affectation_id)
        if not success:
            raise ValueError("Erreur lors de la suppression de l'affectation")
        EmailService.envoyer_email_affectation(
            affectation=affectation_dict,
            recipient_email=affectation_dict["utilisateur"]["email"],
            action="suppression"
        )

    @staticmethod
    def lister_affectations_par_utilisateur(utilisateur_id):
        affectations = AffectationDAO.get_by_utilisateur_id(utilisateur_id)
        return [AffectationService._format_affectation(a) for a in affectations]
