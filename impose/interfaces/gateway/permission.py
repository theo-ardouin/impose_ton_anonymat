from abc import ABC, abstractmethod
from typing import Set

from impose.entities import Permission


class IPermissionGateway(ABC):
    @abstractmethod
    def update(self, user_id: int, permissions: Set[Permission]) -> None:
        pass

    @abstractmethod
    def get(self, user_id: int) -> Set[Permission]:
        pass
