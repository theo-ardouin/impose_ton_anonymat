#!/usr/bin/env python3
import sys

from impose.adapters.database import Database
from impose.entities import Permission


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <user_id> <scope...>")

    with Database().create_session() as session:
        try:
            session.permissions.update(int(sys.argv[1]), {
                Permission(permission) for permission in sys.argv[2:]
            })
        except Exception as err:
            print(err)
