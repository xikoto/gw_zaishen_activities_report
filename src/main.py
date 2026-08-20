import asyncio
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from daily_activities_embed import DailyActivitiesEmbed
from discord_client import send_message
from discord_events import DiscordEvents
from config import load_config


DATA_PATH = Path("data/source")


def generate_daily(data_path: Path, config: dict):
    embed = DailyActivitiesEmbed(
                data_path=data_path,
                config=config,
            ).build()
        
    send_message(embed=embed)

    print("Daily Activities OK")

async def generate_event(config: dict):
    events_config = config["discord"]["events"]
    timezone = ZoneInfo(events_config["timezone"])

    today = datetime.now(timezone).date()

    start_hour, start_minute = map(
        int,
        events_config["start_time"].split(":"),
    )

    end_hour, end_minute = map(
        int,
        events_config["end_time"].split(":"),
    )

    start_time = datetime(
        today.year,
        today.month,
        today.day,
        start_hour,
        start_minute,
        tzinfo=timezone,
    )

    end_time = datetime(
        today.year,
        today.month,
        today.day,
        end_hour,
        end_minute,
        tzinfo=timezone,
    )

    discord_events = DiscordEvents(config)

    event = await discord_events.process(
        event_name="Zaishen Bounty",
        description="Complete today's Zaishen Bounty.",
        start_time=start_time,
        end_time=end_time,
    )

    print("GENERATE EVENT OK")

async def main():
    config = load_config()

    # === GENERATE DAILY ===
    generate_daily(DATA_PATH, config)

    # === CHOOSE MISSION ===

    # === GENERATE EVENT ===
    await generate_event(config)


if __name__ == "__main__":
    asyncio.run(main())