from datetime import datetime, timezone
from pathlib import Path

from discord_client import send_message
from zaishen_rotation import ZaishenRotation


DATA_PATH = Path("data/source")

SOURCE_FILES = [
    "nicholas_sandford.json",
    "shining_blade.json",
    "vanguard_quest.json",
    "zaishen_bounty.json",
    "zaishen_combat.json",
    "zaishen_missions.json",
    "zaishen_vanquish.json",
]


def main():
    fields = []

    for filename in SOURCE_FILES:
        rotation = ZaishenRotation(DATA_PATH / filename)
        quest = rotation.get_today_quest()

        fields.append(
            {
                "name": rotation.type,
                "value": quest["name"],
                "inline": False,
            }
        )

    today = datetime.now(timezone.utc).strftime("%d/%m/%Y")

    embed = {
        "title": "🎮 Guild Wars 1 — Daily Activities",
        "description": today,
        "fields": fields,
    }

    send_message(embed=embed)

    print("Guild Wars 1 — Daily Activities OK")


if __name__ == "__main__":
    main()