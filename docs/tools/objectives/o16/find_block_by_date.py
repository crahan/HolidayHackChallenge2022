#!/usr/bin/env python
"""Find a block that's close to a specific timestamp."""
from datetime import datetime
from typing import Optional

import bs4 as bs
import click
import requests
from dateutil import parser

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


def extract_epochtime(block_data: str) -> int:
    """Extract the epoch time from block data."""
    soup = bs.BeautifulSoup(block_data, "lxml")
    timestamp = soup.table.find("td", text="\ntimestamp\n")
    epochtime = timestamp.nextSibling.text[1:].split(" ")[0]
    return int(epochtime)


def find_block_by_epochtime(
    epochtime: int, first_block: Optional[int] = None, last_block: Optional[int] = None
) -> int:
    """Find a block that's close to a specific epoch time."""
    genesis_block = 0
    latest_block = get_latest_block_number()

    # If the epochtime is older than the genesis block, return the genesis block
    if epochtime < extract_epochtime(get_block_data(genesis_block)):
        return genesis_block

    # If the epochtime is newer that the latest block, return the latest block
    if epochtime > extract_epochtime(get_block_data(latest_block)):
        return latest_block

    # Use the genesis block as the default for the first block value, if none was specified
    first_block = first_block or genesis_block

    # Use the latest block as the default for the last block, if none was specified
    last_block = last_block or latest_block

    # Calculate the middle block
    mid_block = first_block + ((last_block - first_block) // 2)

    # Search for the closest block
    if mid_block == first_block:
        # Found the closest block that is not an exact match
        print("done!")
        return mid_block
    else:
        print(".", end="", flush=True)
        mid_epochtime = extract_epochtime(get_block_data(mid_block))

        if epochtime < mid_epochtime:
            # Continue searching lower half
            return find_block_by_epochtime(epochtime, first_block, mid_block)
        elif epochtime > mid_epochtime:
            # Continue searching upper half
            return find_block_by_epochtime(epochtime, mid_block, last_block)
        else:
            # Found a block with an exact match
            print("done!")
            return mid_block


@click.command()
@click.option(
    "--timestamp",
    "-t",
    type=str,
    required=True,
    help="Timestamp formatted as 'YYYY-MM-DDTHH:MM:SSZ'.",
)
def cli(timestamp: str) -> None:
    """Find a block that's close to a specific timestamp."""
    printc(f"Searching for a block close to '{timestamp}', please be patient", "info")
    block = find_block_by_epochtime(int(parser.parse(timestamp).timestamp()))
    printc(f"Block found at #{block}", "success")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
