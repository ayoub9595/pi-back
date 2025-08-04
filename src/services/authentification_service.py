from src import db
from src.models.authentification import Authentification
from src.dao.utilisateur_dao import UtilisateurDAO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from src.models.utilisateur import UserRole

class AuthentificationService:

    @staticmethod
    def inscrire_utilisateur(data):
        AuthentificationService.valider_champs_inscription(data)

        email = data['email']
        cin = data['cin']

        if AuthentificationService.verifier_email_existant(email):
            raise ValueError("Email déjà utilisé")

        if AuthentificationService.verifier_cin_existant(cin):
            raise ValueError("CIN déjà utilisé")

        role_str = data.get('role', 'UTILISATEUR').upper()
        if not role_str or role_str not in UserRole.__members__:
            role_str = 'UTILISATEUR'

        try:
            utilisateur = UtilisateurDAO.create_utilisateur(
                nom=data['nom'],
                email=email,
                cin=cin,
                telephone=data['telephone'],
                role=UserRole[role_str]
            )
        except Exception as e:
            raise ValueError(f"Erreur lors de la création de l'utilisateur : {str(e)}")

        AuthentificationService.creer_compte(utilisateur.id, data['mot_de_passe'])

        access_token = create_access_token(
            identity=str(utilisateur.id),
            additional_claims={
                "role": utilisateur.role.value.upper(),
                "email": utilisateur.email
            }
        )
        refresh_token = create_refresh_token(identity=str(utilisateur.id))

        return {
            "msg": "Utilisateur créé avec succès",
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    def creer_compte(id_utilisateur, mot_de_passe):
        user = UtilisateurDAO.get_utilisateur_by_id(id_utilisateur)
        if not user:
            raise ValueError("Utilisateur introuvable")
        auth = Authentification.query.filter_by(id_utilisateur=id_utilisateur).first()
        if auth:
            raise ValueError("Compte d'authentification déjà existant pour cet utilisateur")
        mot_de_passe_hash = generate_password_hash(mot_de_passe)
        auth = Authentification(id_utilisateur=id_utilisateur, mot_de_passe_hash=mot_de_passe_hash)
        db.session.add(auth)
        db.session.commit()
        return auth

    @staticmethod
    def login_utilisateur(data):
        email = data.get('email')
        mot_de_passe = data.get('mot_de_passe')

        if not email or not mot_de_passe:
            raise ValueError("Email et mot de passe requis")

        success, user = AuthentificationService.authentifier_utilisateur(email, mot_de_passe)

        if not success or not user:
            raise ValueError("Email ou mot de passe incorrect")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role.value.upper(),
                "email": user.email
            }
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role.value.upper(),
                "email": user.email
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

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
    def valider_champs_inscription(data):
        required_fields = ['nom', 'email', 'cin', 'telephone', 'mot_de_passe']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValueError(f"Champs manquants : {', '.join(missing_fields)}")

    @staticmethod
    def verifier_email_existant(email):
        return UtilisateurDAO.get_utilisateur_by_email(email) is not None

    @staticmethod
    def verifier_cin_existant(cin):
        return UtilisateurDAO.get_utilisateur_by_cin(cin) is not None

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
