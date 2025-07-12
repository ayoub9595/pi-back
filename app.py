from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS

from src import db

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    migrate = Migrate(app, db)


    jwt = JWTManager(app)


    CORS(app)

    with app.app_context():
        pass

    from src.controllers.equipment_controller import equipment_blueprint
    from src.controllers.utilisateur_controller import utilisateur_bp
    from src.controllers.authentification_controller import authentication_bp

    app.register_blueprint(equipment_blueprint, url_prefix="/equipements")
    app.register_blueprint(utilisateur_bp, url_prefix="/utilisateurs")
    app.register_blueprint(authentication_bp, url_prefix="/auth")

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
