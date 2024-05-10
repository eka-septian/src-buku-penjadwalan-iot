import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    from . import main
    app.register_blueprint(main.bp)

    return app
