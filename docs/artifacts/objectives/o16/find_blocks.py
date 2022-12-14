#!/usr/bin/env python
"""Find and download blockchain data."""
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import click
import requests

SESSION = requests.Session()
TOP_BLOCK_URL = "https://prod-blockbrowser.kringle.co.in/cgi-bin/topblock"
BLOCK_DATA_URL = "https://prod-blockbrowser.kringle.co.in/cgi-bin/blockdata"


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


def get_latest_block_number() -> int:
    """Retrieve the most recent block number."""
    response = SESSION.get(TOP_BLOCK_URL)

    if response.status_code == 200:
        return response.json().get("topblock", 0)
    else:
        return 0


def get_block_data(block_number: int, query: List[str]) -> Optional[str]:
    """Retrieve block data for a specific block number."""
    response = SESSION.post(BLOCK_DATA_URL, json={"blocknumber": block_number})

    if response.status_code == 200:
        if any([item in response.text for item in query]):
            # One or more search strings match, return the value
            return response.text
        else:
            return None
    else:
        printc(f"Got Error {response.status_code} for block #{block_number}", "error")
        return None


@click.command()
@click.option(
    "--query",
    "-q",
    type=str,
    multiple=True,
    required=True,
    help="The string to search for.",
)
@click.option(
    "--start-from",
    "-s",
    type=int,
    help="Block number to work our way down from.",
)
@click.option(
    "--output-folder",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True),
    default=Path("./blocks"),
    help="Output folder path.",
)
@click.option(
    "--delay",
    "-d",
    type=int,
    default=0,
    help="How long to wait between HTTP requests.",
)
@click.option(
    "--exit-when-found",
    "-e",
    is_flag=True,
    help="Stop checking when the first match is found.",
)
def cli(
    query: List[str],
    start_from: int,
    output_folder: Path,
    delay: int,
    exit_when_found: bool,
) -> None:
    """Iterate over the blockchain and download matching blocks."""
    for item in query:
        printc(f"Searching for '{item}'", "info")

    output_folder = Path(output_folder)

    if not output_folder.exists():
        # The blocks folder doesn't exist, create it
        printc(f"{output_folder} does not exist. Creating!", "warning")
        output_folder.mkdir(parents=True)

    if not start_from:
        # No start block specified, so grab the latest one
        start_from = get_latest_block_number()
        printc(f"No start block specified, using latest #{start_from}", "warning")

    done = False
    current_block = start_from
    printc(f"Starting search at block #{current_block}", "info")

    # Iterate until we hit 0 or the first match is found
    while not done and current_block >= 0:
        if response := get_block_data(current_block, query):
            # Rejoice! We found a matching block!
            filename = output_folder / f"{current_block}.html"

            with open(filename, "w", encoding="utf-8") as fhandle:
                fhandle.write(response)

            printc(f"Ehrmagherd, we found one at #{current_block}!", "success")

            if exit_when_found:
                done = True

        if not done:
            # Not done yet, so continue on
            current_block -= 1

            if current_block % 100 == 0:
                # Every so often print a status update
                printc(f"Still busy, checking block #{current_block}", "warning")

            if delay:
                # Slow things down a little
                time.sleep(delay)

    printc("All done!", "info")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
