from impose.entities import Task
from impose.logger import LOGGER

from .context import Context


class TaskRunner:
    def __init__(self, context: Context, task: Task) -> None:
        self.context = context
        self.task = task

    async def execute(self) -> None:
        with self.context.database.create_session() as session:
            cursor = session.tasks.get_cursor(self.task.channel_id)
            img = session.images.get_from_cursor(cursor)
            if img is None:
                LOGGER.warn(
                    "No more image for %d at cursor %s", self.task.channel_id, cursor
                )
                return

            LOGGER.info("Sending %s to %d", img[0], self.task.channel_id)
            await self.context.discord.send_file(self.task.channel_id, img[0])
            session.tasks.set_cursor(self.task.channel_id, img[1])
