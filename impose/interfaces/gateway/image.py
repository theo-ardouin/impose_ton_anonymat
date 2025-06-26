from abc import ABC, abstractmethod
from collections.abc import Sequence

from impose.entities import Image, Cursor


class IImageGateway(ABC):
    @abstractmethod
    def add(self, image: Image) -> None:
        pass

    @abstractmethod
    def add_multiple(self, images: Sequence[Image]) -> None:
        pass

    @abstractmethod
    def get_from_cursor(self, cursor: Cursor | None) -> tuple[Image, Cursor] | None:
        pass
