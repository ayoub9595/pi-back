from flask import Flask
from flask_migrate import Migrate
from src import db  # Import de db uniquement

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialisation des extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Import des modèles DANS le contexte d'application
    with app.app_context():
        from src.models.equipment import Equipment
        from src.models.caracteristique_equipement import CaracteristiqueEquipment
    
    # Enregistrement des blueprints
    from src.controllers.equipment_controller import equipment_blueprint
    app.register_blueprint(equipment_blueprint)
    
    return app

app = create_app()