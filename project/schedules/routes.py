from os import abort
from typing import Callable

from apscheduler.schedulers.base import JobLookupError
from flask import flash, render_template, request
from flask_login.login_manager import redirect
from flask_login.utils import url_for

from project import bg_schedules, db
from project.models import Schedule

from . import bp


class ScheduleModel:
    """Class for parsing and manage sheduled job"""

    id: str
    hour: int
    minute: int
    second: int

    def __init__(self, func: Callable, hour: int, minute: int, second: int):
        self.id = bg_schedules.add_job(func, "cron", second="*").id
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def reschedule(id: str, hour: int, minute: int, second: int):
        bg_schedules.reschedule_job(id, "cron", second="*")

    @staticmethod
    def delete(id: str):
        bg_schedules.remove_job(id)


def test_job():
    print("job executed!")


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        hour = request.form["hour"]
        minute = request.form["minute"]
        second = request.form["second"]

        schedule_data = ScheduleModel(test_job, hour, minute, second)
        new_schedule = Schedule(**schedule_data.__dict__)
        db.session.add(new_schedule)
        db.session.commit()

        flash("Schedule created!")

    schedules = db.session.query(Schedule).all()

    return render_template("index.html", schedules=schedules)


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
