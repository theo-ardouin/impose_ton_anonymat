from abc import ABC, abstractmethod

from impose.entities import Task


class IScheduler(ABC):
    @abstractmethod
    def add(self, task: Task) -> None:
        pass

    @abstractmethod
    def has(self, channel_id: int) -> bool:
        pass

    @abstractmethod
    def remove(self, channel_id: int) -> None:
        pass

    @abstractmethod
    def reload(self) -> None:
        pass
