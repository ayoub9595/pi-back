from src import db
from src.models.authentification  import Authentification
from src.dao.utilisateur_dao import UtilisateurDAO
from werkzeug.security import generate_password_hash, check_password_hash

class AuthentificationService:

    @staticmethod
    def creer_compte(id_utilisateur, mot_de_passe):
        # Vérifier si l'utilisateur existe
        user = UtilisateurDAO.get_utilisateur_by_id(id_utilisateur)
        if not user:
            raise ValueError("Utilisateur introuvable")


        auth = Authentification.query.filter_by(id_utilisateur=id_utilisateur).first()
        if auth:
            raise ValueError("Compte d'authentification déjà existant pour cet utilisateur")

        # Créer compte avec mot de passe hashé
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        auth = Authentification(id_utilisateur=id_utilisateur, mot_de_passe_hash=mot_de_passe_hash)
        db.session.add(auth)
        db.session.commit()
        return auth

    @staticmethod
    def authentifier_utilisateur(email, mot_de_passe):
        user = UtilisateurDAO.get_utilisateur_by_email(email)
        if not user:
          return False, None
        auth = Authentification.query.filter_by(id_utilisateur=user.id).first()
        if not auth:
          return False, None
        if not check_password_hash(auth.mot_de_passe_hash, mot_de_passe):
          return False, None
        return True, user


    @staticmethod
    def changer_mot_de_passe(id_utilisateur, ancien_mot_de_passe, nouveau_mot_de_passe):
        auth = Authentification.query.filter_by(id_utilisateur=id_utilisateur).first()
        if not auth:
            raise ValueError("Compte d'authentification introuvable")

        if not check_password_hash(auth.mot_de_passe_hash, ancien_mot_de_passe):
            raise ValueError("Ancien mot de passe incorrect")

        auth.mot_de_passe_hash = generate_password_hash(nouveau_mot_de_passe)
        db.session.commit()
        return auth
