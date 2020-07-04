import asyncio
import schedule
from dataclasses import dataclass
from typing import Any, Callable, Dict

from impose.entities import Task

from .context import Context
from .runner import TaskRunner


class Scheduler:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.tasks: Dict[int, Task] = {}

    def add(self, task: Task) -> None:
        self.tasks[task.channel_id] = task

    def remove(self, channel_id: int) -> None:
        del self.tasks[channel_id]

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
