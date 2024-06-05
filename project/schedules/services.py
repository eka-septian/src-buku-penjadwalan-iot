from typing import Callable
from project import bg_schedules


class ScheduleModel:
    """Class for parsing and manage sheduled job"""

    id: str
    hour: int
    minute: int
    second: int

    def __init__(self, func: Callable, pin: int, hour: int, minute: int, second: int):
        self.id = bg_schedules.add_job(func, "cron", hour=hour, second=second, minute=minute, args=[pin]).id
        self.hour = hour
        self.minute = minute
        self.second = second

    @staticmethod
    def reschedule(id: str, hour: int, minute: int, second: int):
        bg_schedules.reschedule_job(id, "cron", second="*")

    @staticmethod
    def delete(id: str):
        bg_schedules.remove_job(id)
