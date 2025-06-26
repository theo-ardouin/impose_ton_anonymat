from dataclasses import dataclass

from impose.interfaces.database import IDatabase
from impose.interfaces.discord import IDiscord


@dataclass(frozen=True)
class Context:
    discord: IDiscord
    database: IDatabase
    parent_path: str
