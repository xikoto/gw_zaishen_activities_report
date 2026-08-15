import json
from datetime import date, datetime, timezone
from pathlib import Path


class ZaishenRotation:
    def __init__(self, json_path: str | Path):
        self.json_path = Path(json_path)

        self._load()

    def _load(self) -> None:
        with self.json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.type = data["type"]
        self.reference_date = datetime.fromisoformat(
            data["reference_date"].replace("Z", "+00:00")
        )
        self.reset_time = data["reset_time"]
        self.cycle_length = data["cycle_length"]
        self.quests = data["quests"]

        self._validate()

    def _validate(self) -> None:
        if self.cycle_length != len(self.quests):
            raise ValueError(
                f"Cycle length ({self.cycle_length}) does not match "
                f"the number of quests ({len(self.quests)})"
            )

        expected_orders = list(range(self.cycle_length))
        actual_orders = [quest["order"] for quest in self.quests]

        if actual_orders != expected_orders:
            raise ValueError(
                f"Quest orders are invalid. "
                f"Expected {expected_orders}, got {actual_orders}"
            )

    def get_quest(self, target_date: date | datetime) -> dict:
        if isinstance(target_date, datetime):
            target_date = target_date.date()

        reference_date = self.reference_date.date()

        days_elapsed = (target_date - reference_date).days
        quest_index = days_elapsed % self.cycle_length

        return self.quests[quest_index]

    def get_today_quest(self) -> dict:
        today = datetime.now(timezone.utc).date()

        return self.get_quest(today)