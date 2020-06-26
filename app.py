import sys
import schedule
import asyncio

from discord import Client
from typing import Sequence
from impose import Config, ImageList, ImposeTonAnonymat, LOGGER, runner, ITask
from concurrent.futures import CancelledError

CLIENT = Client()


@CLIENT.event
async def on_ready() -> None:
    LOGGER.info(f"Logged-in as {CLIENT.user}")


async def scheduler(tasks: Sequence[ITask]) -> None:
    try:
        await CLIENT.wait_until_ready()

        for task in tasks:
            schedule.every().day.at(task.time_of_day).do(runner, task.execute)

        while True:
            schedule.run_pending()
            await asyncio.sleep(0.5)
    except CancelledError:
        pass


if __name__ == "__main__":
    try:
        config = Config.load()
        CLIENT.loop.create_task(
            scheduler([ImposeTonAnonymat(CLIENT, config, ImageList.load())])
        )
        CLIENT.run(config.token)
    except Exception as err:
        LOGGER.exception(err)
