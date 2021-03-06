from abc import ABC, abstractmethod, abstractproperty
from contextlib import contextmanager
from typing import Iterator

from .gateway import ITaskGateway, IImageGateway, IPermissionGateway


class ISession(ABC):
    @abstractproperty
    def tasks(self) -> ITaskGateway:
        pass

    @abstractproperty
    def images(self) -> IImageGateway:
        pass

    @abstractproperty
    def permissions(self) -> IPermissionGateway:
        pass


class IDatabase(ABC):
    @abstractmethod
    def create_session(self) -> Iterator[ISession]:
        pass
