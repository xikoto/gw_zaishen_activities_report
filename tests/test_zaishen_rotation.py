from datetime import date
from pathlib import Path

import pytest

from zaishen_rotation import ZaishenRotation


JSON_PATH = "data/source/zaishen_combat.json"
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


def test_reference_date_returns_first_quest():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 10, 22))

    assert quest["order"] == 0
    assert quest["name"] == "Jade Quarry"


def test_second_day_returns_second_quest():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 10, 23))

    assert quest["order"] == 1
    assert quest["name"] == "Codex Arena"


def test_last_day_of_cycle_returns_last_quest():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 11, 18))

    assert quest["order"] == 27
    assert quest["name"] == "Alliance Battles"


def test_cycle_restarts_after_28_days():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 11, 19))

    assert quest["order"] == 0
    assert quest["name"] == "Jade Quarry"


def test_cycle_repeats_after_multiple_cycles():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 12, 17))

    assert quest["order"] == 0
    assert quest["name"] == "Jade Quarry"


def test_date_before_reference_date_wraps_cycle():
    rotation = ZaishenRotation(JSON_PATH)

    quest = rotation.get_quest(date(2009, 10, 21))

    assert quest["order"] == 27
    assert quest["name"] == "Alliance Battles"


@pytest.mark.parametrize("filename", SOURCE_FILES)
def test_source_file_can_be_loaded(filename):
    rotation = ZaishenRotation(DATA_PATH / filename)

    assert rotation.type
    assert rotation.reference_date
    assert rotation.cycle_length > 0
    assert len(rotation.quests) == rotation.cycle_length


@pytest.mark.parametrize("filename", SOURCE_FILES)
def test_source_file_has_valid_quest_orders(filename):
    rotation = ZaishenRotation(DATA_PATH / filename)

    orders = [quest["order"] for quest in rotation.quests]

    assert orders == list(range(rotation.cycle_length))


@pytest.mark.parametrize("filename", SOURCE_FILES)
def test_source_file_can_get_today_quest(filename):
    rotation = ZaishenRotation(DATA_PATH / filename)

    quest = rotation.get_today_quest()

    assert quest is not None
    assert quest["order"] in range(rotation.cycle_length)
    assert quest["name"]