import logging
from pathlib import Path

from impose.entities import Image
from impose.interfaces.database import ISession
from impose.interfaces.discord import IDiscord

LOGGER = logging.getLogger(__name__)


def get_image_path(parent_path: str, image: Image) -> str:
    return str(Path(parent_path) / image)


async def send_image(
    session: ISession, discord: IDiscord, channel_id: int, parent_path: str
) -> None:
    cursor = session.tasks.get_cursor(channel_id)
    content = session.images.get_from_cursor(cursor)
    if content is None:
        LOGGER.warning("No more image for %d at cursor %s", channel_id, cursor)
        return

    image, cursor = content
    img_path = get_image_path(parent_path, image)
    LOGGER.info("Sending %s to %d", img_path, channel_id)
    await discord.send_file(channel_id, img_path)
    session.tasks.set_cursor(channel_id, cursor)
