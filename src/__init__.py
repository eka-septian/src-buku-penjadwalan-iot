from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler

db = SQLAlchemy()
scheduler = BackgroundScheduler()


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
    )

    db.init_app(app)
    register_cli_commands(app)

    with app.app_context():
        scheduler.start()

    from .services import schedule_light, turn_off_light, turn_on_light

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    @app.route("/schedule", methods=["POST"])
    def schedule():
        data = request.get_json()
        job_id = data.get("job_id")
        hour = data.get("hour")
        minute = data.get("minute")
        second = data.get("second")
        action = data.get("action")

        if action == "on":
            job = schedule_light(job_id, hour, minute, second, turn_on_light)
        elif action == "off":
            job = schedule_light(job_id, hour, minute, second, turn_off_light)
        else:
            return jsonify({"error": "Invalid action"}), 400

        return jsonify({"job_id": job.id, "next_run_time": job.next_run_time}), 201

    return app


def register_cli_commands(app):
    @app.cli.command("init-db")
    def initialize_database():
        db.drop_all()
        db.create_all()
        print("Initialized the database!")
