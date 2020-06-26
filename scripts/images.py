#!/usr/bin/env python3
import sys

from json import dump
from typing import Sequence
from os import walk, path
from dataclasses import asdict

from impose.imagelist import ImageList, FILENAME


def is_image(filename: str) -> bool:
    return filename.endswith((".png", ".jpg", ".jpeg", ".gif"))


def find_images(filepath: str) -> Sequence[str]:
    files = []
    for (dirpath, dirnames, filenames) in walk(filepath):
        files.extend([
            path.join(dirpath, filename)
            for filename in filenames
            if is_image(filename)
        ])
    return files


def get_output_filename() -> str:
    if len(sys.argv) < 3:
        return FILENAME
    return sys.argv[2]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <directory> [output]")

    image_list = ImageList(index=0, images=find_images(sys.argv[1]))
    dump(asdict(image_list), open(get_output_filename(), "w+"))
