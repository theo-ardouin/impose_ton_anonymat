import logging

from impose.entities import Task
from impose.interfaces.database import ISession

from .scheduler import Scheduler

LOGGER = logging.getLogger(__name__)


class TaskHandler:
    def __init__(self, session: ISession, scheduler: Scheduler) -> None:
        self.session = session
        self.scheduler = scheduler

    def register(self) -> None:
        for task in self.session.tasks.all():
            LOGGER.info(f"Register {task} from database")
            self.scheduler.add(task)
        self.scheduler.reload()

    def add(self, task: Task) -> None:
        self.session.tasks.add(task)
        if self.scheduler.has(task.channel_id):
            self.scheduler.remove(task.channel_id)
        self.scheduler.add(task)
        self.scheduler.reload()
        LOGGER.info(f"Register {task}")

    def remove(self, channel_id: int) -> None:
        self.session.tasks.remove(channel_id)
        self.scheduler.remove(channel_id)
        self.scheduler.reload()
        LOGGER.info(f"Unregister task for {channel_id}")
