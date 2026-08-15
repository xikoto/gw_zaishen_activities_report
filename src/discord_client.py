import os

import requests
from dotenv import load_dotenv


load_dotenv()

webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

if not webhook_url:
    raise RuntimeError(
        "DISCORD_WEBHOOK_URL environment variable is not configured"
    )


def send_message(
    message: str | None = None,
    embed: dict | None = None,
) -> None:
    webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

    payload = {}

    if message:
        payload["content"] = message

    if embed:
        payload["embeds"] = [embed]

    response = requests.post(
        webhook_url,
        json=payload,
        timeout=10,
    )

    response.raise_for_status()