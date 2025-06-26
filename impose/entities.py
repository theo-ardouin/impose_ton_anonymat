from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import NewType


class CommandType(Enum):
    start = "start"
    stop = "stop"
    image = "image"
    permission = "perm"
    test = "test"


class Permission(Enum):
    QUERY_IMAGE = "image.query"
    WRITE_SCHEDULE = "schedule.write"
    WRITE_PERMISSION = "permission.write"


@dataclass(frozen=True)
class Task:
    channel_id: int
    times: Sequence[str]


Cursor = NewType("Cursor", str)
Image = NewType("Image", str)
