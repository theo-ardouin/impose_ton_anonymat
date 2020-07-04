from abc import ABC, abstractmethod, abstractproperty


class IDiscord(ABC):
    @abstractproperty
    def user(self) -> str:
        pass

    @abstractmethod
    async def send(self, channel_id: int, message: str) -> None:
        pass

    @abstractmethod
    async def send_file(self, channel_id: int, filename: str) -> None:
        pass
