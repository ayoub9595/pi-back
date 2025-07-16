from src.dao.utilisateur_dao import UtilisateurDAO

class UtilisateurService:

    @staticmethod
    def creer_utilisateur(data):
        required_fields = ['nom', 'cin', 'role']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Le champ '{field}' est requis.")

        if UtilisateurDAO.get_utilisateur_by_cin(data['cin']):
            raise ValueError("Un utilisateur avec ce CIN existe déjà.")

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
        utilisateur = UtilisateurDAO.update_utilisateur(
            utilisateur_id,
            nom=data.get('nom'),
            cin=data.get('cin'),
            telephone=data.get('telephone'),
            role=data.get('role')
        )
        if not utilisateur:
            raise ValueError("Utilisateur introuvable pour mise à jour.")
        return utilisateur

    @staticmethod
    def supprimer_utilisateur(utilisateur_id):
        success = UtilisateurDAO.delete_utilisateur(utilisateur_id)
        if not success:
            raise ValueError("Utilisateur introuvable pour suppression.")
        return success
