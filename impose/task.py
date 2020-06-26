from abc import ABC, abstractmethod, abstractproperty


class ITask(ABC):
    @abstractproperty
    def time_of_day(self) -> str:
        pass

    @abstractmethod
    async def execute(self) -> None:
        pass
