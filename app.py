import sys
if sys.version_info >= (3, 13):
    # Fix collections imports
    import collections
    import collections.abc
    collections.defaultdict = collections.defaultdict
    collections.MutableMapping = collections.abc.MutableMapping
    sys.modules['collections'] = collections
    
    # Fix typing imports
    import typing
    typing.TYPE_CHECKING = False

from flask import Flask
from config import Config
from src.models.equipment import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Import and register blueprints
    from src.controllers.equipment_controller import equipment_blueprint
    app.register_blueprint(equipment_blueprint, url_prefix='/api/equipment')
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)