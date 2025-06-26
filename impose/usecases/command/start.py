from collections.abc import Sequence
from impose.entities import Task, Permission
from impose.usecases.task import TaskHandler

from .command import Context, ICommand, Permission


class CommandStart(ICommand):
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def permission(self) -> Permission:
        return Permission.WRITE_SCHEDULE

    async def execute(
        self, _user_id: int, channel_id: int, args: Sequence[str]
    ) -> str | None:
        with self.context.database.create_session() as session:
            TaskHandler(session, self.context.scheduler).add(
                Task(
                    channel_id=channel_id,
                    times=args if args else ["08:00"],
                )
            )

        return "Registered"
