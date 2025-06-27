import logging
from collections.abc import Sequence

from impose.entities import Image, Permission
from impose.usecases.image import get_image_path

from .command import Context, ICommand, Permission

LOGGER = logging.getLogger(__name__)


class CommandTest(ICommand):
    def __init__(self, context: Context) -> None:
        self.context = context

    @property
    def permission(self) -> Permission:
        return Permission.QUERY_IMAGE

    async def execute(
        self, user_id: int, channel_id: int, _args: Sequence[str]
    ) -> str | None:
        img = get_image_path(self.context.parent_path, Image("test.png"))
        LOGGER.info("User %d sent %s to %d", user_id, img, channel_id)
        await self.context.discord.send_file(channel_id, img)
        return None
