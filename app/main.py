from flask import Blueprint, jsonify, request, render_template

from . import leds
from .services import turn_off_light, turn_on_light

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def dashboard():
    return render_template("dashboard.html", leds=leds)


@main_bp.route("/led/switch", methods=["POST"])
def led_switch():
    data = request.get_json()
    action = bool(data.get("action"))
    pin = data.get("pin")

    if action:
        turn_on_light(pin)
    else:
        turn_off_light(pin)

    return jsonify({"status": "success"}), 200
