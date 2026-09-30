import argparse
import tomllib

from cloudbox.database import Database, Session, run_migrations
from cloudbox.app import create_app

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str)
    parser.add_argument("--debug", action="store_true")

    args = parser.parse_args()
    
    with open(args.config, "rb") as file:
        config = tomllib.load(file)

    app = create_app(config)

    app.run(
        host=config["flask"]["host"],
        port=config["flask"]["port"],
        load_dotenv=False,
        debug=args.debug
    )