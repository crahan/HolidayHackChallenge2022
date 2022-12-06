#!/usr/bin/env python
"""Check if KringleCon 2022 is live!"""
import os
import time
from datetime import datetime

import click
import requests
from dotenv import load_dotenv

URL = "https://2022.kringlecon.com/login"
TIMEOUT = 10
DELAY = 120
load_dotenv()


def format_message(msg: str, msg_type: str) -> str:
    """Format and colorize a message."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    message = f"{timestamp} - {msg}"

    msg_type_mapper = {
        "SUCCESS": click.style(f"[+] {message}", fg="green"),
        "INFO": click.style(f"[-] {message}", fg="yellow"),
        "WARNING": click.style(f"[!] {message}", fg="red"),
    }

    return msg_type_mapper.get(msg_type.upper(), message)


def is_live() -> bool:
    """Check if the login page is accessible."""
    response = requests.get(
        URL,
        timeout=TIMEOUT,
        headers={"User-Agent": "[Taps mic]... Yo, is this thing live?"},
    )

    return response.status_code == 200


def send_notification() -> bool:
    """Send out a Pushover notification."""
    api_url = "https://api.pushover.net/1/messages.json"
    response = requests.post(
        api_url,
        timeout=TIMEOUT,
        data={
            "token": os.environ.get("HHC2022_TOKEN"),
            "user": os.environ.get("HHC2022_USER"),
            "title": "It haz begun!!!!",
            "html": 1,
            "message": (
                "SANS Holiday Hack Challenge 2022 has opened its doors. "
                f'Go <a href="{URL}">check it out</a>!'
            ),
        },
    )

    return response.status_code == 200


def check():
    """Loop and check if HHC2022 has started."""
    while True:
        if is_live():
            click.echo(
                format_message(
                    "It's started! Sending a push notification!", msg_type="success"
                )
            )

            if not send_notification():
                click.echo(
                    format_message(
                        "Uh-oh! Push notification failed!", msg_type="warning"
                    )
                )

        else:
            click.echo(format_message("Not yet. Soon though!", msg_type="info"))

        time.sleep(DELAY)


if __name__ == "__main__":
    click.echo(
        format_message(f"Checking {URL} every {DELAY} seconds.", msg_type="info")
    )
    check()
