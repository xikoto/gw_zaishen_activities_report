import os

import requests
from dotenv import load_dotenv


load_dotenv()


def send_message(message: str) -> None:
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    response = requests.post(
        webhook_url,
        json={
            "content": message,
        },
        timeout=10,
    )

    response.raise_for_status()