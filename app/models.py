from . import db


class Schedule(db.Model):
    __tablename__ = "schedules"

    job_id = db.Column(db.String, primary_key=True)
    led_name = db.Column(db.String, nullable=False)
    action = db.Column(db.Boolean, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    second = db.Column(db.Integer, nullable=False)

    def __init__(self, job_id, led_name, action, hour, minute, second):
        self.job_id = job_id
        self.led_name = led_name
        self.action = action
        self.hour = hour
        self.minute = minute
        self.second = second
