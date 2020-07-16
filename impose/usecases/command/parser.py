from dataclasses import dataclass
from typing import Optional, Sequence

from impose.entities import CommandType
from impose.logger import LOGGER


@dataclass(frozen=True)
class Command:
    type: CommandType
    args: Sequence[str]


def parse(message: str) -> Optional[Command]:
    try:
        args = message.split(" ")
        if args[0] != "!impose":
            return None
        return Command(type=CommandType(args[1]), args=args[2:])
    except ValueError:
        LOGGER.warn("Invalid command: %s", message)
        return None
