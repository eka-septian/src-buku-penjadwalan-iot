from flask import jsonify, render_template, request
from flask_login import login_required

from . import bp
from .services import Light
from project import leds


@bp.route("/")
@login_required
def home():
    return render_template("main/home.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html", leds=leds)


@bp.route("/led/switch", methods=["PATCH"])
def led_switch():
    action = bool(request.json.get("state"))
    pin = int(request.json.get("pin"))
    print(request.json)
    if action:
        print("On")
        Light.turn_on(pin)
    else:
        print("off")
        Light.turn_of(pin)
    return jsonify({"status": "success"}), 200
