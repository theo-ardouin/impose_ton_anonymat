from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Sequence

from impose.entities import Permission
from impose.interfaces import IDatabase, IDiscord
from impose.usecases.task import Scheduler


@dataclass(frozen=True)
class Context:
    discord: IDiscord
    database: IDatabase
    scheduler: Scheduler


class ICommand(ABC):
    @abstractproperty
    def permission(self) -> Permission:
        pass

    @abstractmethod
    async def execute(self, user_id: int, channel_id: int, args: Sequence[str]) -> None:
        pass
