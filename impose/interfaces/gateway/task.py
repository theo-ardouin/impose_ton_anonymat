from abc import ABC, abstractmethod
from typing import Any, Mapping, Optional, Sequence

from impose.entities import Cursor, Task


class ITaskGateway(ABC):
    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def get(self, channel_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def all(self) -> Sequence[Task]:
        pass

    @abstractmethod
    def remove(self, channel_id: int) -> None:
        pass

    @abstractmethod
    def get_cursor(self, channel_id: int) -> Optional[Cursor]:
        pass

    @abstractmethod
    def set_cursor(self, channel_id: int, cursor: Optional[Cursor]) -> None:
        pass
