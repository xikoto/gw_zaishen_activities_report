import os
from datetime import datetime

import discord


class DiscordEvents:
    def __init__(self, config: dict):
        events_config = config["discord"]["events"]

        self.enabled = events_config["enabled"]
        self.name_prefix = events_config["name_prefix"]

        self.token = os.environ["DISCORD_BOT_TOKEN"]
        self.guild_id = int(os.environ["DISCORD_GUILD_ID"])
        self.channel_id = int(os.environ["DISCORD_EVENT_CHANNEL_ID"])

    async def _get_guild(self, client: discord.Client) -> discord.Guild:
        return await client.fetch_guild(self.guild_id)

    async def _get_channel(
        self,
        client: discord.Client,
    ) -> discord.abc.GuildChannel:
        channel = await client.fetch_channel(self.channel_id)

        if not isinstance(channel, discord.abc.GuildChannel):
            raise TypeError(
                f"Channel {self.channel_id} is not a guild channel"
            )

        return channel

    async def _delete_bot_events(
        self,
        guild: discord.Guild,
    ) -> None:
        events = await guild.fetch_scheduled_events()

        for event in events:
            if event.name.startswith(self.name_prefix):
                await event.delete()

    async def _create_event(
        self,
        guild: discord.Guild,
        channel: discord.abc.GuildChannel,
        name: str,
        description: str,
        start_time: datetime,
        end_time: datetime | None = None,
    ) -> discord.ScheduledEvent:
        return await guild.create_scheduled_event(
            name=f"{self.name_prefix} {name}",
            description=description,
            start_time=start_time,
            end_time=end_time,
            channel=channel,
            entity_type=discord.EntityType.voice,
            privacy_level=discord.PrivacyLevel.guild_only,
        )

    async def process(
        self,
        event_name: str,
        description: str,
        start_time: datetime,
        end_time: datetime | None = None,
    ) -> discord.ScheduledEvent | None:

        if not self.enabled:
            return None

        client = discord.Client(
            intents=discord.Intents.none(),
        )

        try:
            await client.login(self.token)

            guild = await self._get_guild(client)
            channel = await self._get_channel(client)

            await self._delete_bot_events(guild)

            event = await self._create_event(
                guild=guild,
                channel=channel,
                name=event_name,
                description=description,
                start_time=start_time,
                end_time=end_time,
            )

            return event

        finally:
            await client.close()