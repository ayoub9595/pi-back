from src import db
from src.models.registration_request import RegistrationRequest, RegistrationStatus
from datetime import datetime

class RegistrationRequestDAO:

    @staticmethod
    def create_request(nom, email, cin, telephone, role):
        request = RegistrationRequest(
            nom=nom,
            email=email,
            cin=cin,
            telephone=telephone,
            role=role
        )
        db.session.add(request)
        db.session.commit()
        return request

    @staticmethod
    def get_request_by_id(request_id):
        return RegistrationRequest.query.get(request_id)

    @staticmethod
    def get_all_requests():
        return RegistrationRequest.query.order_by(
            RegistrationRequest.created_at.desc()
        ).all()

    @staticmethod
    def get_requests_by_status(status):
        return RegistrationRequest.query.filter_by(status=status).order_by(
            RegistrationRequest.created_at.desc()
        ).all()

    @staticmethod
    def update_request(request_id, **kwargs):
        request = RegistrationRequest.query.get(request_id)
        if not request:
            return None

        for key, value in kwargs.items():
            if hasattr(request, key):
                setattr(request, key, value)

        request.updated_at = datetime.utcnow()
        db.session.commit()
        return request

    @staticmethod
    def delete_request(request_id):
        request = RegistrationRequest.query.get(request_id)
        if not request:
            return False

        db.session.delete(request)
        db.session.commit()
        return True

    @staticmethod
    def check_pending_request(email, cin):
        return RegistrationRequest.query.filter(
            RegistrationRequest.status == RegistrationStatus.PENDING,
            (RegistrationRequest.email == email) | (RegistrationRequest.cin == cin)
        ).first() is not None