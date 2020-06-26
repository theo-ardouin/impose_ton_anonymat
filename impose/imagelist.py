from __future__ import annotations

from typing import List
from random import randint
from dataclasses import dataclass

from .io import Reader, Writer
from .tools import loop

FILENAME = "images.json"


@dataclass
class ImageList:
    index: int
    images: List[str]

    def add(self, filename: str) -> None:
        self.images.insert(self.index + 1, filename)

    @property
    def current(self) -> str:
        return self.images[self.index]

    def next(self) -> str:
        self.index = loop(self.index + 1, 0, len(self.images))
        return self.current

    @staticmethod
    def load() -> ImageList:
        return Reader(ImageList, FILENAME).read()

    @staticmethod
    def save(images: ImageList) -> None:
        Writer(images, FILENAME).write()
