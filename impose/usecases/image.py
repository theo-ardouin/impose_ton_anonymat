from impose.interfaces import IDiscord, ISession
from impose.logger import LOGGER


async def send_image(session: ISession, discord: IDiscord, channel_id: int) -> None:
    cursor = session.tasks.get_cursor(channel_id)
    img = session.images.get_from_cursor(cursor)
    if img is None:
        LOGGER.warn("No more image for %d at cursor %s", channel_id, cursor)
        return

    LOGGER.info("Sending %s to %d", img[0], channel_id)
    await discord.send_file(channel_id, img[0])
    session.tasks.set_cursor(channel_id, img[1])
