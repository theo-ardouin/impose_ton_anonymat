from typing import Sequence

from impose.entities import Permission
from impose.usecases.task import TaskHandler

from .command import Context, ICommand, Permission


class CommandStop(ICommand):
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def permission(self) -> Permission:
        return Permission.WRITE_SCHEDULE

    async def execute(
        self, _user_id: int, channel_id: int, _args: Sequence[str]
    ) -> None:
        with self.context.database.create_session() as session:
            TaskHandler(session, self.context.scheduler).remove(channel_id)

        await self.context.discord.send(channel_id, "Unregistered")
