from __future__ import annotations

from typing import Optional

from impose.interfaces import IDatabase, IDiscord
from impose.usecases import Scheduler, Context


class Service:
    INSTANCE: Optional[Service] = None

    def __init__(self, discord: IDiscord, db: IDatabase) -> None:
        self.discord = discord
        self.db = db
        self.scheduler = Scheduler(Context(discord, db))

    @classmethod
    def get_instance(cls) -> Service:
        if cls.INSTANCE is None:
            raise ValueError("Server instance was never set")
        return cls.INSTANCE
