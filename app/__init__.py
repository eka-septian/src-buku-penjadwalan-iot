from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

import SimulRPi.GPIO as GPIO

io = GPIO
scheduler = BackgroundScheduler()

leds = [
    {"name": "LED1", "pin": 23},
    {"name": "LED2", "pin": 27},
]

io.setmode(io.BCM)
for led in leds:
    io.setup(led["pin"], io.OUT)


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    from .main import main_bp
    from .schedules import schedules_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(schedules_bp)

    with app.app_context():
        scheduler.start()

    return app
