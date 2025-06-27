from __future__ import annotations

import os
import schedule
import logging

from discord import Client
from discord.ext import tasks
from impose.logger import init_global_logger
from concurrent.futures import CancelledError

from impose.service import Service
from impose.usecases.task import TaskHandler
from impose.usecases.command import parse
from impose.adapters.database import Database
from impose.adapters.discord import Discord

CLIENT = Client()
LOGGER = logging.getLogger(__name__)


@CLIENT.event
async def on_ready() -> None:
    LOGGER.info(f"Logged-in as {Service.get_instance().discord.user}")
    execute_scheduled_tasks.start()


@CLIENT.event
async def on_message(message) -> None:
    service = Service.get_instance()

    if message.author == CLIENT.user:
        return

    cmd = parse(message.content)
    if cmd is None or not cmd.type in service.commands:
        return

    LOGGER.info("Trying to execute %s for %d", cmd, message.author.id)

    with service.db.create_session() as session:
        command = service.commands[cmd.type]
        permissions = session.permissions.get(message.author.id)

        if not command.permission in permissions:
            await service.discord.send(
                message.channel.id, "You don't have this privilege..."
            )
            return

        try:
            output = await command.execute(message.author.id, message.channel.id, cmd.args)
            if output:
                await service.discord.send(message.channel.id, output)

        except Exception as err:
            LOGGER.exception(err)
            await service.discord.send(message.channel.id, "Great job, something is broken!")


@tasks.loop(seconds=0.5)
async def execute_scheduled_tasks() -> None:
    try:
        schedule.run_pending()
    except CancelledError:
        pass


if __name__ == "__main__":
    try:
        init_global_logger(os.getenv("LOG_FILE"))
        token = os.environ["IMPOSE_TOKEN"]
        parent_path = os.environ["PARENT_PATH"]
        Service.INSTANCE = Service(Discord(CLIENT), Database(), parent_path)

        service = Service.get_instance()
        with service.db.create_session() as session:
            TaskHandler(session, service.scheduler).register()

        CLIENT.run(token)
    except Exception as err:
        LOGGER.exception(err)
