import os

import sqlalchemy as sa
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
csrf = CSRFProtect()
login = LoginManager()
login.login_view = "auth.login"

bg_schedules = BackgroundScheduler()
bg_schedules.start()


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

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database!")
    else:
        app.logger.info("Database already contains the users table.")

    return app


def initialize_extensions(app):
    db.init_app(app)
    csrf.init_app(app)
    login.init_app(app)

    from .models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()


def register_blueprints(app):
    from . import auth, main, schedules

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(schedules.bp)


def register_cli_commands(app):
    @app.cli.command("init-db")
    def initialize_database():
        db.drop_all()
        db.create_all()
        print("Initialized the database!")
