from impose.entities import Task

from impose.usecases.image import send_image

from .context import Context


class TaskRunner:
    def __init__(self, context: Context, task: Task) -> None:
        self.context = context
        self.task = task

    async def execute(self) -> None:
        with self.context.database.create_session() as session:
            await send_image(session, self.context.discord, self.task.channel_id)
