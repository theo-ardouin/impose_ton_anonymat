from __future__ import annotations

import os
import schedule
import asyncio

from discord import Client
from typing import Optional, Sequence
from impose.logger import LOGGER
from concurrent.futures import CancelledError

from impose.service import Service
from impose.usecases import TaskHandler
from impose.adapters import Database, Discord
from impose.entities import Task


IMPOSE_TOKEN = "IMPOSE_TOKEN"
CLIENT = Client()


@CLIENT.event
async def on_ready() -> None:
    LOGGER.info(f"Logged-in as {Service.get_instance().discord.user}")


@CLIENT.event
async def on_message(message) -> None:
    if message.author == CLIENT.user:
        return
    if message.author.id != 321292348187475969:  # Hardcoding ME as admin :D
        return

    service = Service.get_instance()

    cmd = message.content.split(" ")
    if cmd[0] != "!impose":
        return

    if cmd[1] == "start":
        with service.db.create_session() as session:
            TaskHandler(session, service.scheduler).add(
                Task(
                    channel_id=message.channel.id,
                    times=cmd[2:] if len(cmd) > 2 else ["08:00"],
                )
            )
        await message.channel.send(f"Registered for channel {message.channel}")

    elif cmd[1] == "stop":
        with service.db.create_session() as session:
            TaskHandler(session, service.scheduler).remove(message.channel.id)
        await message.channel.send(f"Unregistered {message.channel}")


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
