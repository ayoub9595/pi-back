from datetime import datetime
from src.dao.registration_dao import RegistrationRequestDAO
from src.dao.utilisateur_dao import UtilisateurDAO
from werkzeug.security import generate_password_hash
from src.models.authentification import Authentification
from src.models.utilisateur import UserRole
from src.models.registration_request import RegistrationStatus
from src import db
import secrets
import string


class RegistrationService:

    @staticmethod
    def create_registration_request(data):

        email = data['email']
        cin = data['cin']

        if RegistrationRequestDAO.check_pending_request(email, cin):
            raise ValueError("Une demande d'inscription est déjà en attente pour cet email ou CIN")

        if UtilisateurDAO.get_utilisateur_by_email(email):
            raise ValueError("Email déjà utilisé")

        if UtilisateurDAO.get_utilisateur_by_cin(cin):
            raise ValueError("CIN déjà utilisé")

        role_str = data.get('role', 'UTILISATEUR').upper()
        if role_str not in UserRole.__members__:
            role_str = 'UTILISATEUR'

        request = RegistrationRequestDAO.create_request(
            nom=data['nom'],
            email=email,
            cin=cin,
            telephone=data['telephone'],
            role=UserRole[role_str],
        )

        return {
            "msg": "Demande d'inscription soumise avec succès. En attente de validation par l'administrateur. Verifiez votre email !",
            "request_id": request.id
        }

    @staticmethod
    def generate_random_password(length=12):

        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"

        password_chars = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(symbols)
        ]

        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(length - 4):
            password_chars.append(secrets.choice(all_chars))

        secrets.SystemRandom().shuffle(password_chars)

        return ''.join(password_chars)

    @staticmethod
    def update_registration_request(request_id, admin_id, update_data):

        request = RegistrationRequestDAO.get_request_by_id(request_id)

        if not request:
            raise ValueError("Demande d'inscription introuvable")

        new_status = update_data.get('status', '').upper()

        if new_status == 'APPROVED':
            if request.status == RegistrationStatus.APPROVED:
                raise ValueError("Cette demande est déjà approuvée")

            if UtilisateurDAO.get_utilisateur_by_email(request.email):
                raise ValueError("Un utilisateur avec cet email existe déjà")

            if UtilisateurDAO.get_utilisateur_by_cin(request.cin):
                raise ValueError("Un utilisateur avec ce CIN existe déjà")

            final_role = request.role
            if 'role' in update_data:
                role_str = update_data['role'].upper()
                if role_str in UserRole.__members__:
                    final_role = UserRole[role_str]

            plain_password = RegistrationService.generate_random_password()
            hashed_password = generate_password_hash(plain_password)

            temporary_plain_password = plain_password

            utilisateur = UtilisateurDAO.create_utilisateur(
                nom=request.nom,
                cin=request.cin,
                email=request.email,
                telephone=request.telephone,
                role=final_role
            )

            auth = Authentification(
                id_utilisateur=utilisateur.id,
                mot_de_passe_hash=hashed_password
            )
            db.session.add(auth)

            request.status = RegistrationStatus.APPROVED
            request.rejection_reason = None

            request.generated_password = temporary_plain_password

        elif new_status == 'REJECTED':
            if request.status == RegistrationStatus.REJECTED:
                raise ValueError("Cette demande est déjà rejetée")

            request.status = RegistrationStatus.REJECTED
            request.rejection_reason = update_data.get('rejection_reason', 'Raison non spécifiée')

        elif new_status == 'PENDING':
            request.status = RegistrationStatus.PENDING
            request.rejection_reason = None

        elif new_status == '':
            if 'nom' in update_data:
                request.nom = update_data['nom']
            if 'telephone' in update_data:
                request.telephone = update_data['telephone']
            if 'role' in update_data:
                role_str = update_data['role'].upper()
                if role_str in UserRole.__members__:
                    request.role = UserRole[role_str]

        elif new_status:
            raise ValueError(f"Statut invalide: {new_status}. Utilisez PENDING, APPROVED ou REJECTED")

        request.reviewed_by = admin_id
        request.updated_at = datetime.utcnow()

        db.session.commit()

        response_data = {
            "msg": "Demande mise à jour avec succès",
            "request_id": request.id,
            "status": request.status.value
        }

        if new_status == 'APPROVED' and hasattr(request, 'generated_password'):
            response_data["generated_password"] = request.generated_password
            response_data["note"] = "Ce mot de passe a été envoyé par email à l'utilisateur. Il est recommandé de le changer à la première connexion."

        return response_data

    @staticmethod
    def get_all_requests():
        """Get all registration requests"""
        return RegistrationRequestDAO.get_all_requests()

    @staticmethod
    def get_request_by_id(request_id):
        return RegistrationRequestDAO.get_request_by_id(request_id)

    @staticmethod
    def get_requests_by_status(status_str):
        try:
            status = RegistrationStatus[status_str.upper()]
            return RegistrationRequestDAO.get_requests_by_status(status)
        except KeyError:
            raise ValueError(f"Statut invalide: {status_str}")

    @staticmethod
    def delete_request(request_id):
        return RegistrationRequestDAO.delete_request(request_id)