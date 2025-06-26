from discord import Client, File

from impose.interfaces.discord import IDiscord


class Discord(IDiscord):
    def __init__(self, client: Client) -> None:
        self.client = client

    @property
    def user(self) -> str:
        return str(self.client.user)

    async def send(self, channel_id: int, message: str) -> None:
        await self.client.get_channel(channel_id).send(message)

    async def send_file(self, channel_id: int, filename: str) -> None:
        await self.client.get_channel(channel_id).send(file=File(filename))
