from pathlib import Path

from zaishen_rotation import ZaishenRotation


DATA_PATH = Path("data/source")

ACTIVITIES = [
    "nicholas_sandford.json",
    "shining_blade.json",
    "vanguard_quest.json",
    "zaishen_bounty.json",
    "zaishen_combat.json",
    "zaishen_missions.json",
    "zaishen_vanquish.json",
]


def main():
    for filename in ACTIVITIES:
        rotation = ZaishenRotation(DATA_PATH / filename)
        quest = rotation.get_today_quest()

        print(f"{rotation.type}: {quest['name']}")


if __name__ == "__main__":
    main()