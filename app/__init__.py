from flask import Flask

from .config import Config
from .extensions import db, migrate
from .routes.dashboard import dashboard_bp
from .extensions import db, migrate, jwt

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models
    from .routes.auth import auth_bp
    from .routes.inventory import inventory_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(dashboard_bp)
    return app