import csv
from datetime import datetime, timezone
from pathlib import Path

from discord_client import send_message
from zaishen_rotation import ZaishenRotation


DATA_PATH = Path("data/source")

CSV_FILE = DATA_PATH / "zaishen_data.csv"

SOURCE_FILES = [
    "nicholas_sandford.json",
    "shining_blade.json",
    "vanguard_quest.json",
    "zaishen_bounty.json",
    "zaishen_combat.json",
    "zaishen_missions.json",
    "zaishen_vanquish.json",
]


TYPE_MAPPING = {
    "Zaishen Bounty": "Bounty",
    "Zaishen Combat": "Combat",
    "Zaishen Mission": "Mission",
    "Zaishen Vanquish": "Vanquish",
}


def load_zaishen_data():
    with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        return {
            (row["Name"].strip(), row["Type"].strip()): row
            for row in reader
        }


def main():
    zaishen_data = load_zaishen_data()

    fields = []

    for filename in SOURCE_FILES:
        rotation = ZaishenRotation(DATA_PATH / filename)
        quest = rotation.get_today_quest()

        csv_type = TYPE_MAPPING.get(rotation.type)

        if csv_type is None:
            # Las actividades que no están en zaishen_data.csv
            # se mantienen sin enriquecimiento.
            fields.append(
                {
                    "name": rotation.type,
                    "value": quest["name"],
                    "inline": False,
                }
            )
            continue

        data = zaishen_data.get((quest["name"], csv_type))

        if data is None:
            raise ValueError(
                f"No se encontró '{quest['name']}' "
                f"con tipo '{csv_type}' en {CSV_FILE}"
            )

        name = data["Name"]
        url = data["URL"]
        reward = data["Total Zaishen Copper Coints"]

        fields.append(
            {
                "name": rotation.type,
                "value": f"[{name}]({url}) — 🪙 **{reward}**",
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