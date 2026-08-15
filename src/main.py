from pathlib import Path

from daily_activities_embed import DailyActivitiesEmbed
from discord_client import send_message
from config import load_config


DATA_PATH = Path("data/source")


def main():
    config = load_config()

    embed = DailyActivitiesEmbed(
        data_path=DATA_PATH,
        config=config,
    ).build()

    send_message(embed=embed)

    print("Daily Activities OK")


if __name__ == "__main__":
    main()