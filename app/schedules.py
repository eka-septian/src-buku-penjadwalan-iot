from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for

from . import db, leds
from .models import Schedule
from .services import schedule_light, turn_on_light, turn_off_light, delete_schedule

schedules_bp = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        schedules = Schedule.query.all()
        return render_template("schedule.html", leds=leds, schedules=schedules)

    hour = int(request.form["hour"])
    minute = int(request.form["minute"])
    second = int(request.form["second"])
    action = request.form["action"]
    pin = int(request.form["pin"])

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

    flash("Schedule created!")

    return redirect(url_for("schedules.index"))


@schedules_bp.route("/<id>/delete")
def delete(id):
    try:
        db.session.execute(db.delete(Schedule).filter_by(job_id=id))
        db.session.commit()
        delete_schedule(id)
    except Exception as e:
        print(e)

    return redirect(url_for("schedules.index"))
