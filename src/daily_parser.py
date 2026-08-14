from dataclasses import dataclass
from datetime import date
from urllib.parse import urljoin

from bs4 import BeautifulSoup


DAILY_COLUMNS = [
    "Zaishen Mission",
    "Zaishen Bounty",
    "Zaishen Combat",
    "Zaishen Vanquish",
    "Shining Blade",
    "Vanguard Quest",
    "Nicholas Sandford",
]


@dataclass
class DailyMission:
    mission_type: str
    name: str
    url: str


class DailyParser:

    def __init__(
        self,
        base_url: str = "https://wiki.guildwars.com",
    ):
        self.base_url = base_url

    def parse(
        self,
        html: str,
        target_date: date,
    ) -> list[DailyMission]:

        soup = BeautifulSoup(
            html,
            "html.parser",
        )

        table = self._find_daily_table(soup)

        if table is None:
            raise ValueError(
                "Could not find the daily activities table."
            )

        headers = self._get_headers(table)

        header_indexes = {
            header.strip().lower(): index
            for index, header in enumerate(headers)
        }

        date_row = self._find_date_row(
            table,
            target_date,
        )

        if date_row is None:
            raise ValueError(
                "Could not find daily activities for "
                f"{target_date.strftime('%d %B %Y')}"
            )

        cells = date_row.find_all(
            ["td", "th"]
        )

        missions: list[DailyMission] = []

        for mission_type in DAILY_COLUMNS:

            column_index = header_indexes.get(
                mission_type.lower()
            )

            if column_index is None:
                continue

            if column_index >= len(cells):
                continue

            cell = cells[column_index]

            link = cell.find(
                "a",
                href=True,
            )

            if link is None:
                continue

            name = link.get_text(
                " ",
                strip=True,
            )

            href = link["href"]

            url = urljoin(
                self.base_url,
                href,
            )

            missions.append(
                DailyMission(
                    mission_type=mission_type,
                    name=name,
                    url=url,
                )
            )

        return missions

    def _find_daily_table(
        self,
        soup: BeautifulSoup,
    ):
        for table in soup.find_all("table"):

            headers = self._get_headers(table)

            if self._is_daily_table(headers):
                return table

        return None

    def _get_headers(
        self,
        table,
    ) -> list[str]:

        header_row = table.find("tr")

        if header_row is None:
            return []

        headers = header_row.find_all(
            ["th", "td"]
        )

        return [
            cell.get_text(
                " ",
                strip=True,
            )
            for cell in headers
        ]

    def _is_daily_table(
        self,
        headers: list[str],
    ) -> bool:

        normalized = {
            header.strip().lower()
            for header in headers
        }

        required = {
            "date",
            "zaishen mission",
            "zaishen bounty",
            "zaishen combat",
            "zaishen vanquish",
            "shining blade",
            "vanguard quest",
            "nicholas sandford",
        }

        return required.issubset(normalized)

    def _find_date_row(
        self,
        table,
        target_date: date,
    ):

        target_date_text = target_date.strftime(
            "%d %B %Y"
        )

        for row in table.find_all("tr"):

            cells = row.find_all(
                ["td", "th"]
            )

            if not cells:
                continue

            first_cell_text = cells[0].get_text(
                " ",
                strip=True,
            )

            if first_cell_text == target_date_text:
                return row

        return None