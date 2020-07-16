from __future__ import annotations

import os
import schedule
import asyncio

from discord import Client
from typing import Optional, Sequence
from impose.logger import LOGGER
from concurrent.futures import CancelledError

from impose.service import Service
from impose.usecases.task import TaskHandler
from impose.usecases.command import parse
from impose.adapters import Database, Discord
from impose.entities import Task


IMPOSE_TOKEN = "IMPOSE_TOKEN"
CLIENT = Client()


@CLIENT.event
async def on_ready() -> None:
    LOGGER.info(f"Logged-in as {Service.get_instance().discord.user}")


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
            await service.discord.send(message.channel.id, "You don't have this privilege...")
            return

        await command.execute(message.author.id, message.channel.id, cmd.args)


async def execute_scheduled_tasks() -> None:
    try:
        await CLIENT.wait_until_ready()
        while True:
            schedule.run_pending()
            await asyncio.sleep(0.5)
    except CancelledError:
        pass


if __name__ == "__main__":
    try:
        Service.INSTANCE = Service(Discord(CLIENT), Database())

        service = Service.get_instance()
        with service.db.create_session() as session:
            TaskHandler(session, service.scheduler).register()

        CLIENT.loop.create_task(execute_scheduled_tasks())
        CLIENT.run(os.environ[IMPOSE_TOKEN])
    except Exception as err:
        LOGGER.exception(err)
