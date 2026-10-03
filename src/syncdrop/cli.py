"""The ``syncdrop`` command.

Prints the address other devices should open, and a QR code so nobody has to type it.
"""

from __future__ import annotations

import argparse
import sys
from typing import Final

from syncdrop import __version__
from syncdrop.network import DEFAULT_PORT, candidates, choose, find_port
from syncdrop.qr.encode import encode
from syncdrop.qr.render import to_text

#: Indented by two, so the address stands away from the edge of a terminal.
INDENT: Final = "  "


def _report_addresses() -> int:
    """List every address and what SyncDrop makes of it."""
    found = candidates()
    if not found:
        print("No network addresses found at all. Is this machine on a network?")
        return 1
    print(f"{'score':>6}  {'interface':<18} {'address':<16} why")
    for one in found:
        print(f"{one.score:>6}  {one.interface:<18} {one.address:<16} {one.why}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run the command."""
    parser = argparse.ArgumentParser(
        prog="syncdrop",
        description=(
            "Move files between devices on one network. One device runs this; every other "
            "device opens the address it prints, in a browser. Nothing is installed on the "
            "far end and nothing leaves the local network."
        ),
    )
    parser.add_argument("--version", action="version", version=f"SyncDrop {__version__}")
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"Port to listen on. Default: {DEFAULT_PORT}, or the next free one above it.",
    )
    parser.add_argument(
        "--address",
        help=(
            "Address to advertise, when the chosen one is wrong. "
            "Run with --addresses to see what there is."
        ),
    )
    parser.add_argument(
        "--addresses",
        action="store_true",
        help="List every address on this machine, with what SyncDrop makes of each.",
    )
    parser.add_argument("--no-qr", action="store_true", help="Do not draw the QR code.")
    arguments = parser.parse_args(argv)

    if arguments.addresses:
        return _report_addresses()

    try:
        chosen = choose(arguments.address)
    except LookupError as problem:
        print(f"SyncDrop cannot start: {problem}", file=sys.stderr)
        return 1

    try:
        port = find_port(arguments.port)
    except OSError as problem:
        print(f"SyncDrop cannot start: {problem}", file=sys.stderr)
        return 1

    url = f"http://{chosen.address}:{port}"

    print()
    print(f"{INDENT}SyncDrop is ready.")
    print()
    print(f"{INDENT}{url}")
    print()
    if not arguments.no_qr:
        print(to_text(encode(url)))
    print(f"{INDENT}Open that on your phone. There is nothing to install.")
    print(f"{INDENT}Using {chosen.interface}: {chosen.why}.")
    print()

    # The transfer itself is the next piece of work. Saying so beats a program that looks like
    # it is running and answers nothing.
    print(f"{INDENT}The transfer server is not written yet, so this address answers nothing.")
    print(f"{INDENT}See TASKS.md, phase 3.")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
