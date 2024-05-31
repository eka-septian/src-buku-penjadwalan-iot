from . import scheduler
from datetime import datetime


def turn_on_light():
    print(f"Light turned on at {datetime.now()}")


def turn_off_light():
    print(f"Light turned off at {datetime.now()}")


def schedule_light(job_id, hour, minute, second, action):
    job = scheduler.add_job(
        action, "cron", hour=hour, minute=minute, second=second, id=job_id
    )
    return job
