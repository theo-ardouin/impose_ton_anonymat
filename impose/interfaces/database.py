from abc import ABC, abstractmethod
from contextlib import contextmanager
from collections.abc import Iterator

from .gateway import ITaskGateway, IImageGateway, IPermissionGateway


class ISession(ABC):
    @property
    @abstractmethod
    def tasks(self) -> ITaskGateway:
        pass

    @property
    @abstractmethod
    def images(self) -> IImageGateway:
        pass

    @property
    @abstractmethod
    def permissions(self) -> IPermissionGateway:
        pass


class IDatabase(ABC):
    @abstractmethod
    @contextmanager
    def create_session(self) -> Iterator[ISession]:
        pass
