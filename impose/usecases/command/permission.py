from collections.abc import Sequence

from impose.entities import Permission

from .command import Context, ICommand, Permission


class CommandPermission(ICommand):
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def permission(self) -> Permission:
        return Permission.WRITE_PERMISSION

    async def execute(
        self, _: int, _channel_id: int, args: Sequence[str]
    ) -> str | None:
        with self.context.database.create_session() as session:
            try:
                session.permissions.update(
                    int(args[0]), {Permission(arg) for arg in args[1:]}
                )
                return "Permissions have been updated"
            except (IndexError, ValueError):
                return "!impose perm <user_id> <scope...>"
