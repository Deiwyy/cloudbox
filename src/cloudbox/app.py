from flask import Flask

from cloudbox.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(auth_bp)



    @app.route("/")
    def index():
        return "Hello from Cloudbox!"

    return app