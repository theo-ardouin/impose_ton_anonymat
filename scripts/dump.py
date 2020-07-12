#!/usr/bin/env python3
import sys

from typing import Sequence
from os import walk, path

from impose.adapters import Database


def is_image(filename: str) -> bool:
    return filename.endswith((".png", ".jpg", ".jpeg", ".gif"))


def find_images(filepath: str) -> Sequence[str]:
    files = []
    for (dirpath, dirnames, filenames) in walk(filepath):
        files.extend([
            path.realpath(path.join(dirpath, filename))
            for filename in filenames
            if is_image(filename)
        ])
    return files


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <directory>")

    with Database().create_session() as session:
        try:
            session.images.add_multiple(find_images(sys.argv[1]))
        except Exception as err:
            print(err)
