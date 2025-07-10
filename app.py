from flask import Flask
from flask_migrate import Migrate
from src import db

def create_app():
    app = Flask(__name__)
    
    
    app.config.from_object('config.Config')

    
    db.init_app(app)
    migrate = Migrate(app, db)

   
    with app.app_context():
        from src.models.equipment import Equipment
        from src.models.caracteristique_equipement import CaracteristiqueEquipment
     

    
    from src.controllers.equipment_controller import equipment_blueprint

    app.register_blueprint(equipment_blueprint, url_prefix="/equipements")

    return app


app = create_app()
