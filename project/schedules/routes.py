from apscheduler.schedulers.base import JobLookupError
from flask import flash, render_template, request, abort
from flask_login.login_manager import redirect
from flask_login.utils import url_for

from project import bg_schedules, db
from project.models import Schedule
from project.schedules.services import ScheduleModel
from project.main.services import Light

from . import bp


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = Light.turn_on if request.form["action"] == "on" else Light.turn_of
        hour = int(request.form["hour"])
        minute = int(request.form["minute"])
        second = int(request.form["second"])

        print(action)

        schedule_data = ScheduleModel(action , hour, minute, second)
        new_schedule = Schedule(**schedule_data.__dict__)
        db.session.add(new_schedule)
        db.session.commit()

        flash("Schedule created!")

    schedules = db.session.query(Schedule).all()

    return render_template("schedule/index.html", schedules=schedules)


@bp.route("/<id>/delete")
def delete(id):
    query = db.select(Schedule).where(Schedule.job_id == id)
    schedule = db.session.execute(query).one_or_none()

    if schedule is None:
        abort(404, description="Schedule not found")  

    try:
        # TODO: teardown the table if the server stop
        ScheduleModel.delete(id)
    except JobLookupError:
        pass

    # This should be the one that being executed but somehow it's not work
    # db.session.delete(schedule)
    # db.session.commit()
    # so function call bellow it's a hacky solution

    db.session.execute(db.delete(Schedule).filter_by(job_id=id))
    db.session.commit()

    return redirect(url_for("schedules.index"))
