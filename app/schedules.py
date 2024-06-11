from flask import Blueprint, request, jsonify

from . import db, leds
from .models import Schedule
from .services import schedule_light, turn_on_light, turn_off_light

schedules_bp = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules_bp.route("/", methods=["POST"])
def schedule():
    data = request.get_json()
    hour = data.get("hour")
    minute = data.get("minute")
    second = data.get("second")
    action = data.get("action")
    pin = data.get("pin")

    if action == "on":
        job = schedule_light(lambda: turn_on_light(pin), hour, minute, second)
    elif action == "off":
        job = schedule_light(lambda: turn_off_light(pin), hour, minute, second)
    else:
        return jsonify({"error": "Invalid action"}), 400

    led_name = next(led["name"] for led in leds if led["pin"] == pin)
    action = action == "on"
    new_schedule = Schedule(
        job_id=job.id,
        led_name=led_name,
        action=action,
        hour=hour,
        minute=minute,
        second=second,
    )

    db.session.add(new_schedule)
    db.session.commit()

    return (
        jsonify({"success": "Schedule created!", "next_run_time": job.next_run_time}),
        201,
    )
