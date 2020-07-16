from __future__ import annotations

from typing import Optional

from impose.entities import CommandType
from impose.interfaces import IDatabase, IDiscord
from impose.usecases.task import Scheduler, TaskContext
from impose.usecases.command import (
    CommandImage,
    CommandStart,
    CommandStop,
    CommandContext,
)


class Service:
    INSTANCE: Optional[Service] = None

    def __init__(self, discord: IDiscord, db: IDatabase) -> None:
        self.discord = discord
        self.db = db
        self.scheduler = Scheduler(TaskContext(discord, db))
        ctxt = CommandContext(discord, db, self.scheduler)
        self.commands = {
            CommandType.image: CommandImage(ctxt),
            CommandType.start: CommandStart(ctxt),
            CommandType.stop: CommandStop(ctxt),
        }

    @classmethod
    def get_instance(cls) -> Service:
        if cls.INSTANCE is None:
            raise ValueError("Server instance was never set")
        return cls.INSTANCE
