import logging
from dataclasses import dataclass
from collections.abc import Sequence

from impose.entities import CommandType

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class Command:
    type: CommandType
    args: Sequence[str]


def parse(message: str) -> Command | None:
    try:
        args = message.split(" ")
        if args[0] != "!impose":
            return None
        return Command(type=CommandType(args[1]), args=args[2:])
    except (ValueError, IndexError):
        LOGGER.warning("Invalid command: %s", message)
        return None
