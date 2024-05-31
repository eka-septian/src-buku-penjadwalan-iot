from . import db


class Schedule(db.Model):
    __tablename__ = "schedules"

    job_id = db.Column(db.String, primary_key=True)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    second = db.Column(db.Integer, nullable=False)

    def __init__(self, job_id, hour, minute, second):
        self.job_id = job_id
        self.hour = hour
        self.minute = minute
        self.second = second
