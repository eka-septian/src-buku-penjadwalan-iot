from datetime import datetime

from . import io


def turn_on_light(pin):
    io.output(pin, io.HIGH)
    print(f"Light turned on at {datetime.now()}")


def turn_off_light(pin):
    io.output(pin, io.LOW)
    print(f"Light turned off at {datetime.now()}")
