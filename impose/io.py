import json
from typing import Any

from dataclasses import dataclass, asdict


class Reader:
    def __init__(self, class_: Any, filename: str) -> None:
        self.filename = filename
        self.class_ = class_

    def read(self) -> Any:
        return self.class_(**json.load(open(self.filename)))


class Writer:
    def __init__(self, class_: Any, filename: str) -> None:
        self.filename = filename
        self.class_ = class_

    def write(self) -> None:
        json.dump(asdict(self.class_), open(self.filename, "w+"))
