from abc import ABC, abstractmethod

from impose.entities import Permission


class IPermissionGateway(ABC):
    @abstractmethod
    def update(self, user_id: int, permissions: set[Permission]) -> None:
        pass

    @abstractmethod
    def get(self, user_id: int) -> set[Permission]:
        pass
