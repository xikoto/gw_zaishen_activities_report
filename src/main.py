from zaishen_rotation import ZaishenRotation


def main():
    zaishen_combat = ZaishenRotation("data/source/zaishen_combat.json")

    quest = zaishen_combat.get_today_quest()

    print(f"Zaishen {zaishen_combat.type}: {quest['name']}")


if __name__ == "__main__":
    main()