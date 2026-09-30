from pathlib import Path

from flask import Flask

from cloudbox.database import Database, Session, run_migrations
from cloudbox.utils import app_paths
from cloudbox.services.auth import AuthService

from cloudbox.routes.auth import auth_bp
from cloudbox.routes.explorer import explorer_bp


def create_app(config):
    app = Flask(__name__)

    # Load configuration etc
    paths = app_paths(config["app"]["name"])
    
    data_dir: Path = paths["data"]


    # Initialize the database
    db = Database(data_dir / "database" / config["database"]["filename"])
    db.initialize()
    run_migrations(db)

    # Auth
    auth = AuthService(db)

    # Setup extensions
    app.extensions["db"] = db
    app.extensions["auth"] = auth

    # App configuration
    app.config["SECRET_KEY"] = config["flask"]["secret_key"]

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(explorer_bp)

    return app