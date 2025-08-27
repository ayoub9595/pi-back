from datetime import datetime
from sqlalchemy.exc import IntegrityError
import logging

from src.dao.affectation_dao import AffectationDAO
from src.dao.equipment_dao import EquipmentDAO
from src.dao.reclamation_dao import ReclamationDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from src.models.equipment import Equipment
from src.models.utilisateur import Utilisateur
from src.services.email_service import EmailService
from src.services.utilisateur_service import UtilisateurService


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

        # Notify admins about the new reclamation
        try:
            ReclamationService._notifier_admins_nouvelle_reclamation(reclamation)
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi des notifications email aux admins : {str(e)}")

        # Notify the user who submitted the reclamation
        try:
            ReclamationService._notifier_utilisateur_reclamation(reclamation, action="creation")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de la confirmation email à l'utilisateur : {str(e)}")

        return ReclamationService._format_reclamation(reclamation)

    @staticmethod
    def _notifier_admins_nouvelle_reclamation(reclamation):
        try:
            admins = UtilisateurService.lister_administrateurs()

            if not admins:
                logging.warning("Aucun administrateur trouvé pour l'envoi de notifications")
                return

            reclamation_data = ReclamationService._format_reclamation(reclamation)

            for admin in admins:
                if admin.email:
                    EmailService.envoyer_email_reclamation_pour_admins(
                        reclamation=reclamation_data,
                        recipient_email=admin.email,
                        action="creation"
                    )
                else:
                    logging.warning(f"Admin {admin.nom} (ID: {admin.id}) n'a pas d'adresse email")

        except Exception as e:
            logging.error(f"Erreur lors de la notification des admins : {str(e)}")
            raise

    @staticmethod
    def _notifier_utilisateur_reclamation(reclamation, action="creation"):
        try:
            # Get the user who submitted the reclamation
            utilisateur = UtilisateurService.recuperer_utilisateur(reclamation.id_utilisateur)

            if not utilisateur:
                logging.warning(f"Utilisateur avec ID {reclamation.id_utilisateur} introuvable")
                return

            if not utilisateur.email:
                logging.warning(f"Utilisateur {utilisateur.nom} (ID: {utilisateur.id}) n'a pas d'adresse email")
                return

            reclamation_data = ReclamationService._format_reclamation(reclamation)

            EmailService.envoyer_email_reclamation_pour_utilisateur(
                reclamation=reclamation_data,
                recipient_email=utilisateur.email,
                action=action
            )

        except Exception as e:
            logging.error(f"Erreur lors de la notification de l'utilisateur : {str(e)}")
            raise

    @staticmethod
    def mettre_a_jour_reclamation(reclamation_id, data):
        reclamation = ReclamationDAO.get_by_id(reclamation_id)
        if not reclamation:
            raise ValueError("Réclamation introuvable")

        old_state = reclamation.etat_reclamation

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

            # Notify user if the status changed
            if old_state != updated.etat_reclamation:
                try:
                    if updated.etat_reclamation.lower() == 'acceptée':
                        action = "accepted"
                    elif updated.etat_reclamation.lower() == 'rejetée':
                        action = "rejected"
                    elif updated.etat_reclamation.lower() == 'résolue':
                        action = "resolved"
                    else:
                        action = "update"

                    ReclamationService._notifier_utilisateur_reclamation(updated, action=action)
                except Exception as e:
                    logging.error(f"Erreur lors de la notification de mise à jour à l'utilisateur : {str(e)}")

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