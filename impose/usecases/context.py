from dataclasses import dataclass
from typing import Type

from impose.interfaces import IDatabase, IDiscord


@dataclass(frozen=True)
class Context:
    discord: IDiscord
    database: IDatabase
