import argparse

from cloudbox.app import create_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app = create_app()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=args.debug,
    )