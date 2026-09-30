import argparse
import logging
from flask import app

from cloudbox.server_utils.paths import app_paths

from cloudbox.app import create_app
from cloudbox.database import Database
from cloudbox.database.migrations import run_migrations
from cloudbox.config.settings import APP_NAME
from cloudbox.logger import configure_logging

from cloudbox.services import AuthService

logger = logging.getLogger(__name__)

def main():
    #  ARGS
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    #  APP CREATION
    app = create_app()
    
    #  PATHS CONFIG
    paths = app_paths(APP_NAME)
    app.config["APP_NAME"] = APP_NAME
    app.config["APP_DATA"] = paths["data"]
    app.config["APP_CONFIG"] = paths["config"]
    app.config["APP_LOG"] = paths["log"]

    #  LOGGING CONFIG
    configure_logging(
        log_file=paths["log"] / "cloudbox.log",
        level=app.config.get("LOG_LEVEL", "DEBUG" if args.debug else "INFO"),
    )

    #  DATABASE CONFIG AND INITIALIZATION  
    database = Database(app.config["APP_DATA"] / "database" / "cloudbox.db")
    database.initialize()
    run_migrations(database)

    #  AUTH SERVICE CONFIG
    auth_service = AuthService(database)

    #  EXTENSIONS CONFIG
    app.extensions["database"] = database
    app.extensions["auth_service"] = auth_service

    # RUN APP
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=args.debug,
    )