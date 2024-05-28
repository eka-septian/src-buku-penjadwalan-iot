from flask import jsonify, render_template, request
from flask_login import login_required

from . import bp
from .services import Light
from project import led_pin


@bp.route("/")
@login_required
def home():
    return render_template("main/home.html")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("main/dashboard.html")


@bp.route("/led/switch", methods=["PATCH"])
def led_switch():
    action = bool(request.json.get("state"))
    if action:
        print("turning on")
        Light.turn_on(led_pin)
    else:
        print("turning off")
        Light.turn_of(led_pin)
    return jsonify({"status": "success"}), 200
