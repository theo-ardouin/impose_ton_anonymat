from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Task:
    channel_id: int
    times: Sequence[str]
