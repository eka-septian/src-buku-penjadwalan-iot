from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

try:
    import RPi.GPIO as GPIO
except:
    import SimulRPi.GPIO as GPIO

io = GPIO
db = SQLAlchemy()
scheduler = BackgroundScheduler()

leds = [
    {"name": "Kamar 1", "pin": 17},
    {"name": "Dapur", "pin": 27},
    {"name": "Kamar 2", "pin": 22},
    {"name": "Kamar mandi", "pin": 23},
    {"name": "Ruang tamu", "pin": 24},
]

io.setmode(io.BCM)
for led in leds:
    io.setup(led["pin"], io.OUT)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.sqlite",
    )

    db.init_app(app)
    register_cli_commands(app)

    from .main import main_bp
    from .schedules import schedules_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(schedules_bp)

    with app.app_context():
        scheduler.start()

    return app


def register_cli_commands(app):
    @app.cli.command("init-db")
    def initialize_database():
        db.drop_all()
        db.create_all()
        print("Initialized the database!")
