from abc import ABC, abstractmethod
from collections.abc import Sequence

from impose.entities import Cursor, Task


class ITaskGateway(ABC):
    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def get(self, channel_id: int) -> Task | None:
        pass

    @abstractmethod
    def all(self) -> Sequence[Task]:
        pass

    @abstractmethod
    def remove(self, channel_id: int) -> None:
        pass

    @abstractmethod
    def get_cursor(self, channel_id: int) -> Cursor | None:
        pass

    @abstractmethod
    def set_cursor(self, channel_id: int, cursor: Cursor | None) -> None:
        pass
