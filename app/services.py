from datetime import datetime
from . import io, scheduler


def turn_on_light(pin):
    io.output(pin, io.HIGH)
    print(f"Light turned on at {datetime.now()}")


def turn_off_light(pin):
    io.output(pin, io.LOW)
    print(f"Light turned off at {datetime.now()}")


def schedule_light(action, hour, minute, second):
    job = scheduler.add_job(
        action, "cron", hour=hour, minute=minute, second=second
    )
    return job
