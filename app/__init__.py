import os

from flask import Flask, abort, send_from_directory

from .config import Config
from .extensions import db, migrate, jwt

def create_app(config_class=Config):
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
    app = Flask(__name__, static_folder=frontend_dir, static_url_path="")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from . import models
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.inventory import inventory_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(dashboard_bp)

    @app.get("/api/health")
    def health_check():
        return {"status": "ok"}, 200

    @app.get("/")
    @app.get("/<path:path>")
    def serve_frontend(path="index.html"):
        """Serve the bundled frontend while leaving all /api routes to Flask."""
        if path.startswith("api/"):
            abort(404)

        file_path = os.path.join(frontend_dir, path)
        if path != "index.html" and os.path.isfile(file_path):
            return send_from_directory(frontend_dir, path)
        return send_from_directory(frontend_dir, "index.html")

    return app
