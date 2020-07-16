import json
from sqlite3 import Connection
from typing import Any, Set, Sequence

from impose.entities import Permission
from impose.interfaces import IPermissionGateway


class PermissionGateway(IPermissionGateway):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def update(self, user_id: int, permissions: Set[Permission]) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO permissions (user_id, scopes) VALUES (?, ?)",
            (user_id, json.dumps(list(permissions))),
        )
        self.connection.commit()

    def get(self, user_id: int) -> Set[Permission]:
        row = (
            self.connection.cursor()
            .execute("SELECT scopes FROM permissions WHERE user_id = ?", (user_id,))
            .fetchone()
        )
        if row is None:
            return set()
        return {Permission(permission) for permission in json.loads(row[0])}
