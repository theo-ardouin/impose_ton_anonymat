import json
from sqlite3 import Connection
from typing import Any
from collections.abc import Sequence

from impose.entities import Task, Cursor
from impose.interfaces.gateway import ITaskGateway


class TaskGateway(ITaskGateway):
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def add(self, task: Task) -> None:
        row = (
            self.connection.cursor()
            .execute("SELECT * FROM tasks WHERE channel_id = ?", (task.channel_id,))
            .fetchone()
        )
        if row is None:
            self.connection.execute(
                "INSERT INTO tasks (channel_id, time) VALUES (?, ?)",
                (task.channel_id, json.dumps(task.times)),
            )
        else:
            self.connection.execute(
                "UPDATE tasks SET time = ? WHERE channel_id = ?",
                (json.dumps(task.times), task.channel_id),
            )

    def get(self, channel_id: int) -> Task | None:
        row = (
            self.connection.cursor()
            .execute(
                "SELECT * FROM tasks WHERE channel_id = ? AND time NOT NULL",
                (channel_id,),
            )
            .fetchone()
        )
        return self._deserialize(row) if row else None

    def all(self) -> Sequence[Task]:
        cursor = self.connection.cursor()
        return [
            self._deserialize(row)
            for row in cursor.execute("SELECT * FROM tasks WHERE time NOT NULL")
        ]

    def remove(self, channel_id: int) -> None:
        self.connection.execute(
            "UPDATE tasks SET time = NULL WHERE channel_id = ?", (channel_id,)
        )

    def get_cursor(self, channel_id: int) -> Cursor | None:
        row = (
            self.connection.cursor()
            .execute(
                "SELECT cursor FROM tasks WHERE channel_id = ? AND time NOT NULL",
                (channel_id,),
            )
            .fetchone()
        )
        return Cursor(row[0]) if row else None

    def set_cursor(self, channel_id: int, cursor: Cursor | None) -> None:
        self.connection.execute(
            "UPDATE tasks SET cursor = ? WHERE channel_id = ?",
            (
                cursor,
                channel_id,
            ),
        )

    @staticmethod
    def _deserialize(row: Sequence[Any]) -> Task:
        return Task(channel_id=row[0], times=json.loads(row[1]))
