from typing import Sequence

from impose.entities import Permission
from impose.usecases.image import send_image

from .command import Context, ICommand, Permission


class CommandImage(ICommand):
    def __init__(self, context: Context) -> None:
        self.context = context

    def permission(self) -> Permission:
        return Permission.QUERY_IMAGE

    async def execute(
        self, _user_id: int, channel_id: int, _args: Sequence[str]
    ) -> None:
        with self.context.database.create_session() as session:
            await send_image(session, self.context.discord, channel_id)
