from flask import render_template
from flask_login import login_required

from . import bp


@bp.route("/")
@login_required
def home():
    return render_template("home.html")

@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@bp.route('/fungsi')
def pushbtn_state():
       return "Mantap"
