from __future__ import annotations

from impose.entities import CommandType
from impose.interfaces.database import IDatabase
from impose.interfaces.discord import IDiscord
from impose.usecases.task import Scheduler, TaskContext
from impose.usecases.command import (
    CommandImage,
    CommandStart,
    CommandStop,
    CommandTest,
    CommandContext,
    CommandPermission,
)


class Service:
    INSTANCE: Service | None = None

    def __init__(self, discord: IDiscord, db: IDatabase, parent_path: str) -> None:
        self.discord = discord
        self.db = db
        self.scheduler = Scheduler(TaskContext(discord, db, parent_path))
        ctxt = CommandContext(discord, db, self.scheduler, parent_path)
        self.commands = {
            CommandType.image: CommandImage(ctxt),
            CommandType.start: CommandStart(ctxt),
            CommandType.stop: CommandStop(ctxt),
            CommandType.permission: CommandPermission(ctxt),
            CommandType.test: CommandTest(ctxt),
        }

    @classmethod
    def get_instance(cls) -> Service:
        if cls.INSTANCE is None:
            raise ValueError("Server instance was never set")
        return cls.INSTANCE
