import argparse
from flask import app

from server_utils import app_paths

#  APP
from cloudbox.app import create_app

#  DATABASE
from cloudbox.database import Database

#  CONFIGS
from cloudbox.config.settings import APP_NAME


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

    #  DATABASE CONFIG AND INITIALIZATION  
    database = Database(app.config["APP_DATA"] / "database" / "cloudbox.db")
    database.initialize()

    app.extensions["database"] = database

    # RUN APP
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=args.debug,
    )