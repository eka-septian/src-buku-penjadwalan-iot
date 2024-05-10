import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    initialize_extensions(app)
    register_blueprints(app)
    register_cli_commands(app)

    return app


def initialize_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from . import main

    app.register_blueprint(main.bp)


def register_cli_commands(app):
    @app.cli.command("init-db")
    def initialize_database():
        db.drop_all()
        db.create_all()
        print("Initialized the database!")
