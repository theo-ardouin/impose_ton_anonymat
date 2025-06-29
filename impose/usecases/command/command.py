from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections.abc import Sequence

from impose.entities import Permission
from impose.interfaces.database import IDatabase
from impose.interfaces.discord import IDiscord
from impose.interfaces.scheduler import IScheduler


@dataclass(frozen=True)
class Context:
    discord: IDiscord
    database: IDatabase
    scheduler: IScheduler
    parent_path: str


class ICommand(ABC):
    @property
    @abstractmethod
    def permission(self) -> Permission:
        pass

    @abstractmethod
    async def execute(
        self, user_id: int, channel_id: int, args: Sequence[str]
    ) -> str | None:
        pass
