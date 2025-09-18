from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from src import db, mail
from src.controllers.reclamation_controller import reclamation_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    JWTManager(app)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    from src.controllers.equipment_controller import equipment_blueprint
    from src.controllers.utilisateur_controller import utilisateur_bp
    from src.controllers.authentification_controller import authentication_bp
    from src.controllers.affectation_controller import affectation_bp

    app.register_blueprint(equipment_blueprint, url_prefix="/equipements")
    app.register_blueprint(utilisateur_bp, url_prefix="/utilisateurs")
    app.register_blueprint(authentication_bp, url_prefix="/auth")
    app.register_blueprint(affectation_bp, url_prefix="/affectations")
    app.register_blueprint(reclamation_bp, url_prefix="/reclamations")

    with app.app_context():
        init_admin_user()

    return app

def init_admin_user():
    try:
        from src.models.utilisateur import UserRole
        from src.dao.utilisateur_dao import UtilisateurDAO
        from src.services.authentification_service import AuthentificationService

        admin_users = UtilisateurDAO.get_utilisateurs_by_role('ADMIN')

        if admin_users:
            print(f"Admin user found: {admin_users[0].email}")
            return

        print("No admin user found. Creating default admin user...")

        admin_data = {
            'nom': 'Ayoub Badia',
            'email': 'ayoub.badia95@gmail.com',
            'cin': 'ADMIN001',
            'telephone': '0000000000',
            'role': 'ADMIN',
            'mot_de_passe': '123456'
        }

        AuthentificationService.inscrire_utilisateur(admin_data)


    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        db.session.rollback()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0', port=5000)