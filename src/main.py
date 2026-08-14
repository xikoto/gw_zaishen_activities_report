from datetime import datetime
from zoneinfo import ZoneInfo

from config import load_config
from daily_parser import DailyParser
from wiki_client import WikiClient


def main():
    config = load_config()

    client = WikiClient(
        timeout=config["scraper"]["timeout"]
    )

    html = client.get_page(
        config["scraper"]["daily_url"]
    )

    today = datetime.now(
        ZoneInfo(config["schedule"]["timezone"])
    ).date()

    parser = DailyParser()

    missions = parser.parse(
        html=html,
        target_date=today,
    )

    print(
        f"Daily activities for "
        f"{today.strftime('%d %B %Y')}"
    )

    print()

    for mission in missions:
        print(
            f"{mission.mission_type}: "
            f"{mission.name}"
        )

        print(
            f"  {mission.url}"
        )


if __name__ == "__main__":
    main()