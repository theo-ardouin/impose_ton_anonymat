import json
from sqlite3 import Connection

from impose.entities import Permission
from impose.interfaces.gateway import IPermissionGateway


class PermissionGateway(IPermissionGateway):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def update(self, user_id: int, permissions: set[Permission]) -> None:
        self.connection.execute(
            "INSERT OR REPLACE INTO permissions (user_id, scopes) VALUES (?, ?)",
            (user_id, json.dumps([permission.value for permission in permissions])),
        )

    def get(self, user_id: int) -> set[Permission]:
        row = (
            self.connection.cursor()
            .execute("SELECT scopes FROM permissions WHERE user_id = ?", (user_id,))
            .fetchone()
        )
        if row is None:
            return set()
        return {Permission(permission) for permission in json.loads(row[0])}
