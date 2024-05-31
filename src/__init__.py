from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
    )

    db.init_app(app)
    register_cli_commands(app)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app


def register_cli_commands(app):
    @app.cli.command("init-db")
    def initialize_database():
        db.drop_all()
        db.create_all()
        print("Initialized the database!")
