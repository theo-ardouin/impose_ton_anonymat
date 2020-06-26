from discord import Client, File
from dataclasses import dataclass

from .config import Config
from .task import ITask
from .imagelist import ImageList
from .logger import LOGGER


class ImposeTonAnonymat(ITask):
    def __init__(self, client: Client, config: Config, images: ImageList) -> None:
        super().__init__()
        self.client = client
        self.config = config
        self.images = images

    @property
    def time_of_day(self) -> str:
        return self.config.time_of_day

    async def execute(self) -> None:
        image = self.images.current
        channel = self.client.get_channel(self.config.channel)

        LOGGER.info(f"Sending '{image}' to channel {self.config.channel}")
        try:
            await channel.send(file=File(image))
        except FileNotFoundError as err:
            LOGGER.exception(err)
            await channel.send(f"Oh no! Image '{image}' is broken :(")
        self.images.next()
        self.images.save(self.images)
