#!/usr/bin/env python
"""Iterate over the blockchain and download matching blocks."""
import time
from datetime import datetime
from pathlib import Path
from typing import List

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
    response.raise_for_status()
    return response.json().get("topblock", 0)


def get_block_data(block_number: int) -> str:
    """Retrieve block data for a specific block number."""
    response = SESSION.post(BLOCK_DATA_URL, json={"blocknumber": block_number})
    response.raise_for_status()
    return response.text


def match_query(block_data: str, query: List[str]) -> bool:
    """Check if the block data matches the list of query strings."""
    return any([item in block_data for item in query])


@click.command()
@click.option(
    "--query",
    "-q",
    type=str,
    multiple=True,
    help="A query string to search for.",
)
@click.option(
    "--start-block",
    "-s",
    type=int,
    help="Block number to start searching from.",
)
@click.option(
    "--end-block",
    "-e",
    type=int,
    help="Block number to search to.",
)
@click.option(
    "--output-folder",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True),
    default=Path("./blocks"),
    show_default=True,
    help="Output folder path.",
)
@click.option(
    "--delay",
    "-d",
    type=int,
    default=0,
    show_default=True,
    help="How long to wait between HTTP requests.",
)
@click.option(
    "--exit-when-found",
    "-x",
    is_flag=True,
    help="Stop checking when the first match is found.",
)
def cli(
    query: List[str],
    start_block: int,
    end_block: int,
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

    if not start_block:
        # Use the genesis block if no start block specified
        start_from = get_latest_block_number()
        printc("No start block specified, using #0", "warning")

    if not end_block:
        # Use the latest block if no end block specified
        start_from = get_latest_block_number()
        printc(f"No end block specified, using #{start_from}", "warning")

    done = False
    current_block = start_block
    printc(f"Searching from block #{current_block} to #{end_block}", "info")

    # Iterate until we reach the last block
    while not done and current_block <= end_block:
        block_data = get_block_data(current_block)

        if match_query(block_data, query):
            # Rejoice! We found a matching block!
            filename = output_folder / f"{current_block}.html"

            with open(filename, "w", encoding="utf-8") as fhandle:
                fhandle.write(block_data)

            printc(f"Ehrmagherd, we found a match at #{current_block}!", "success")

            if exit_when_found:
                done = True

        if not done:
            # Not done yet, so continue on
            current_block += 1

            if (current_block - start_block) % 100 == 0:
                # Every so often print a status update
                printc(f"Still busy, checking block #{current_block}", "warning")

            # Slow things down a little
            time.sleep(delay)

    printc("All done!", "info")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
