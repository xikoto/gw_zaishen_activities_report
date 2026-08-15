import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from zaishen_rotation import ZaishenRotation


class DailyActivitiesEmbed:
    ZAISHEN_FILES = [
        "zaishen_bounty.json",
        "zaishen_combat.json",
        "zaishen_missions.json",
        "zaishen_vanquish.json",
    ]

    ENRICHED_FILES = [
        "vanguard_data.json",
        "shining_blade_data.json",
        "nicholas_sandford_data.json",
    ]

    TYPE_MAPPING = {
        "Zaishen Bounty": "Bounty",
        "Zaishen Combat": "Combat",
        "Zaishen Mission": "Mission",
        "Zaishen Vanquish": "Vanquish",
    }

    DEFAULT_TITLE = "🎮 Guild Wars 1 — Daily Activities"
    DEFAULT_DESCRIPTION = "{date}"

    DEFAULT_LABELS = {
        "Zaishen Bounty": "🎯 Zaishen Bounty",
        "Zaishen Combat": "⚔️ Zaishen Combat",
        "Zaishen Mission": "📜 Zaishen Mission",
        "Zaishen Vanquish": "💀 Zaishen Vanquish",
        "Vanguard Quest": "🛡️ Vanguard",
        "Shining Blade": "⚔️ Shining Blade",
        "Nicholas Sandford": "🎒 Nicholas Sandford",
    }

    def __init__(self, data_path: Path, config: dict):
        self.data_path = data_path
        self.config = config

        self.csv_file = data_path / "zaishen_data.csv"
        self.zaishen_data = self._load_zaishen_data()

    def build(self) -> dict:
        fields = []

        # ---------------------------------------------------------
        # Zaishen
        # ---------------------------------------------------------

        for filename in self.ZAISHEN_FILES:
            print(f"FILENAME: {filename}")
            rotation = ZaishenRotation(
                self.data_path / filename
            )

            quest = rotation.get_today_quest()

            fields.append(
                self._build_zaishen_field(
                    rotation,
                    quest,
                )
            )

        # ---------------------------------------------------------
        # Vanguard / Shining Blade / Nicholas
        # ---------------------------------------------------------

        for filename in self.ENRICHED_FILES:
            print(f"FILENAME: {filename}")
            quest = self._get_today_enriched_quest(
                self.data_path / filename
            )

            fields.append(
                self._build_enriched_field(
                    quest,
                )
            )

        return {
            "title": self._get_title(),
            "description": self._get_description(),
            "fields": fields,
        }

    # =============================================================
    # Zaishen
    # =============================================================

    def _build_zaishen_field(
        self,
        rotation,
        quest,
    ) -> dict:
        csv_type = self.TYPE_MAPPING[rotation.type]

        data = self.zaishen_data.get(
            (quest["name"], csv_type)
        )

        if data is None:
            raise ValueError(
                f"No se encontró '{quest['name']}' "
                f"con tipo '{csv_type}' en {self.csv_file}"
            )

        name = data["Name"]
        url = data["URL"]
        reward = data["Total Zaishen Copper Coints"]

        return {
            "name": self._get_label(rotation.type),
            "value": (
                f"[{name}]({url})"
                f" — 🪙 **{reward}**"
            ),
            "inline": False,
        }

    # =============================================================
    # Enriched activities
    # =============================================================

    def _get_today_enriched_quest(
        self,
        filepath: Path,
    ) -> dict:
        with filepath.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        reference_date = datetime.fromisoformat(
            data["reference_date"].replace("Z", "+00:00")
        )

        now = datetime.now(timezone.utc)

        elapsed_days = (
            now.date() - reference_date.date()
        ).days

        index = elapsed_days % data["cycle_length"]

        quests = data["quests"]

        for quest in quests:
            if quest["order"] == index:
                return {
                    **quest,
                    "type": data["type"],
                }

        raise ValueError(
            f"No se encontró la entrada con order={index} "
            f"en {filepath}"
        )

    def _build_enriched_field(
        self,
        quest: dict,
    ) -> dict:
        activity_type = quest["type"]

        if activity_type == "Vanguard Quest":
            return self._build_vanguard_field(quest)

        if activity_type == "Shining Blade":
            return self._build_shining_blade_field(quest)

        if activity_type == "Nicholas Sandford":
            return self._build_nicholas_field(quest)

        raise ValueError(
            f"Tipo de actividad enriquecida desconocido: "
            f"{activity_type}"
        )

    def _build_vanguard_field(
        self,
        quest: dict,
    ) -> dict:
        return {
            "name": self._get_label(quest["type"]),
            "value": (
                f"[{quest['name']}]"
                f"({quest['wiki_url']})"
            ),
            "inline": False,
        }

    def _build_shining_blade_field(
        self,
        quest: dict,
    ) -> dict:
        return {
            "name": self._get_label(quest["type"]),
            "value": (
                f"[{quest['name']}]"
                f"({quest['wiki_url']})"
                f" — 💰 **{quest['gold']}g**"
                f" — ⚔️ **"
                f"{quest['war_supplies']['hm']}"
                f" War Supplies**"
            ),
            "inline": False,
        }

    def _build_nicholas_field(
        self,
        quest: dict,
    ) -> dict:
        return {
            "name": self._get_label(quest["type"]),
            "value": (
                f"[{quest['name']}]"
                f"({quest['wiki_url']})"
                f" — 📦 **5x**"
            ),
            "inline": False,
        }

    # =============================================================
    # Configuration
    # =============================================================

    def _get_title(self) -> str:
        daily_config = self.config.get(
            "discord",
            {},
        ).get(
            "daily",
            {},
        )

        return daily_config.get(
            "title",
            self.DEFAULT_TITLE,
        )

    def _get_description(self) -> str:
        daily_config = self.config.get(
            "discord",
            {},
        ).get(
            "daily",
            {},
        )

        description = daily_config.get(
            "description",
            self.DEFAULT_DESCRIPTION,
        )

        now = datetime.now(timezone.utc)

        return description.format(
            date=now.strftime("%d/%m/%Y"),
            date_iso=now.strftime("%Y-%m-%d"),
        )

    def _get_label(
        self,
        activity_type: str,
    ) -> str:
        daily_config = self.config.get(
            "discord",
            {},
        ).get(
            "daily",
            {},
        )

        labels = daily_config.get(
            "labels",
            {},
        )

        return labels.get(
            activity_type,
            self.DEFAULT_LABELS.get(
                activity_type,
                activity_type,
            ),
        )

    # =============================================================
    # CSV
    # =============================================================

    def _load_zaishen_data(self) -> dict:
        with self.csv_file.open(
            "r",
            encoding="utf-8-sig",
            newline="",
        ) as file:
            reader = csv.DictReader(file)

            return {
                (
                    row["Name"].strip(),
                    row["Type"].strip(),
                ): row
                for row in reader
            }