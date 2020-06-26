from __future__ import annotations

from typing import Sequence
from dataclasses import dataclass

from .io import Reader, Writer

FILENAME = "impose.json"


@dataclass(frozen=True)
class Config:
    token: str
    channel: int
    time_of_day: str

    @staticmethod
    def load() -> Config:
        return Reader(Config, FILENAME).read()
