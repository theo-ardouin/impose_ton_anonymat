from sqlite3 import Connection
from collections.abc import Sequence

from impose.entities import Image, Cursor
from impose.interfaces.gateway import IImageGateway


class ImageGateway(IImageGateway):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, image: Image) -> None:
        self.connection.execute(
            "INSERT OR IGNORE INTO images (image) VALUES (?)", (image,)
        )
        self.connection.commit()

    def add_multiple(self, images: Sequence[Image]) -> None:
        self.connection.executemany(
            "INSERT OR IGNORE INTO images (image) VALUES (?)",
            [(image,) for image in images],
        )
        self.connection.commit()

    def get_from_cursor(self, cursor: Cursor | None) -> tuple[Image, Cursor] | None:
        if cursor is None:
            row = (
                self.connection.cursor()
                .execute("SELECT image, id FROM images ORDER BY id")
                .fetchone()
            )
            if row is None:
                return None
            return Image(row[0]), Cursor(str(row[1]))
        row = (
            self.connection.cursor()
            .execute("SELECT image, id FROM images WHERE id > ? ORDER BY id", (cursor,))
            .fetchone()
        )
        if row is None:
            return None
        return Image(row[0]), Cursor(str(row[1]))
