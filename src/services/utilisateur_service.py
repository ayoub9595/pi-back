import logging

from src.dao.utilisateur_dao import UtilisateurDAO
from src.decorators.error_handlers import ConflictError
from src.services.email_service import EmailService


class UtilisateurService:

    @staticmethod
    def creer_utilisateur(data):
        required_fields = ['nom', 'cin', 'role']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Le champ '{field}' est requis.")

        if UtilisateurDAO.get_utilisateur_by_cin(data['cin']):
            raise ConflictError("Un utilisateur avec ce CIN existe déjà.")

        return UtilisateurDAO.create_utilisateur(
            nom=data['nom'],
            cin=data['cin'],
            telephone=data.get('telephone'),
            role=data['role']
        )

    @staticmethod
    def lister_utilisateurs():
        return UtilisateurDAO.get_all_utilisateurs()

    @staticmethod
    def recuperer_utilisateur(utilisateur_id):
        utilisateur = UtilisateurDAO.get_utilisateur_by_id(utilisateur_id)
        if not utilisateur:
            raise ValueError("Utilisateur introuvable.")
        return utilisateur

    @staticmethod
    def mettre_a_jour_utilisateur(utilisateur_id, data):

        utilisateur_actuel = UtilisateurDAO.get_utilisateur_by_id(utilisateur_id)

        if not utilisateur_actuel:
            raise ValueError("Utilisateur introuvable pour mise à jour.")

        if 'email' in data and data['email']:
            utilisateur_avec_email = UtilisateurDAO.get_utilisateur_by_email(data['email'])
            if utilisateur_avec_email and utilisateur_avec_email.id != utilisateur_id:
                raise ConflictError("Cet email est déjà utilisé par un autre utilisateur.")

        if 'cin' in data and data['cin']:
            utilisateur_avec_cin = UtilisateurDAO.get_utilisateur_by_cin(data['cin'])
            if utilisateur_avec_cin and utilisateur_avec_cin.id != utilisateur_id:
                raise ConflictError("Ce CIN est déjà utilisé par un autre utilisateur.")

        utilisateur = UtilisateurDAO.update_utilisateur(
            utilisateur_id,
            nom=data.get('nom'),
            email=data.get('email'),
            cin=data.get('cin'),
            telephone=data.get('telephone'),
            role=data.get('role')
            )
        if not utilisateur:
            raise ValueError("Erreur lors de la mise à jour de l'utilisateur.")

        try:
            # utilisateur_dict = {
            #     'nom': utilisateur.nom,
            #     'email': utilisateur.email,
            #     'cin': utilisateur.cin,
            #     'telephone': utilisateur.telephone,
            #     'role': utilisateur.role
            #         }
            EmailService.envoyer_email_modification_utilisateur(utilisateur.to_dict())
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de modification : {str(e)}")

        return utilisateur

    @staticmethod
    def supprimer_utilisateur(utilisateur_id):
        success = UtilisateurDAO.delete_utilisateur(utilisateur_id)
        if not success:
            raise ValueError("Utilisateur introuvable pour suppression.")
        return success

    @staticmethod
    def lister_administrateurs():
        return UtilisateurDAO.get_utilisateurs_by_role('ADMIN')