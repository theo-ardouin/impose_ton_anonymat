import asyncio
import schedule
from typing import Any
from collections.abc import Callable

from impose.entities import Task
from impose.interfaces.scheduler import IScheduler
from impose.usecases.task.context import Context
from impose.usecases.task.runner import TaskRunner


class Scheduler(IScheduler):
    def __init__(self, context: Context) -> None:
        self.context = context
        self.tasks: dict[int, Task] = {}

    def add(self, task: Task) -> None:
        self.tasks[task.channel_id] = task

    def remove(self, channel_id: int) -> None:
        del self.tasks[channel_id]

    def has(self, channel_id: int) -> bool:
        return channel_id in self.tasks

    def reload(self) -> None:
        schedule.clear()
        for task in self.tasks.values():
            self._schedule(task)

    def _schedule(self, task: Task) -> None:
        task_runner = TaskRunner(self.context, task)
        for time in task.times:
            schedule.every().day.at(time).do(self.runner, task_runner.execute)

    @staticmethod
    def runner(coroutine: Callable, *args: Any, **kwargs: Any) -> None:
        async def wrapper(coroutine: Callable, *args: Any, **kwargs: Any) -> Any:
            await coroutine(*args, **kwargs)

        asyncio.create_task(wrapper(coroutine, *args, **kwargs))
