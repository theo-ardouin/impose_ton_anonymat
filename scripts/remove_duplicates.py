#!/usr/bin/env python3
import os
import hashlib
from pathlib import Path

from impose.adapters.database import Database
from impose.entities import Image, Cursor

ImageData = tuple[Image, Cursor]


def get_md5(file_path: str) -> str:
    with open(file_path, "rb") as file:
        return hashlib.md5(file.read()).hexdigest()


def generate_md5(
    parent_path: Path, images: list[ImageData]
) -> dict[str, list[ImageData]]:
    count = 0
    total = len(images)
    files: dict[str, list[ImageData]] = {}

    for image, id in images:
        if count % 1000 == 0:
            print(f"Generating MD5 for files ({count}/{total})")

        files.setdefault(get_md5(parent_path / image), []).append((image, id))
        count += 1

    print(f"Generating MD5 for files ({count}/{total})")
    return files


path = Path(os.environ["PARENT_PATH"])
with Database().create_session() as session:
    images = session.images.get_all_images()
    files = generate_md5(path, images)

    for md5, items in files.items():
        if len(items) > 1:
            cursors = [id for _, id in items[1:]]
            session.images.delete_images(cursors)
            print(f"Removing duplicate(s) for MD5 ({md5}): {', '.join(cursors)}")
