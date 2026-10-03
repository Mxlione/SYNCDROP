"""Drawing a QR symbol: in a terminal, and as SVG for the web page.

The terminal rendering uses half-block characters so that one text row carries two module rows.
A QR drawn one module per character line is twice as tall as it is wide, because terminal cells
are, and a camera will not read a stretched symbol. Two modules per character makes it square.

The colours are the other half of it. A terminal's "white" is whatever the user's theme says, so
the symbol is drawn with explicit black and white rather than inverted text: a camera needs the
contrast to be real, not themed.
"""

from __future__ import annotations

from typing import Final

from syncdrop.qr.encode import Symbol

#: Modules of light margin around the symbol. The standard calls for four and scanners rely on
#: it: without the margin a camera cannot tell where the symbol ends.
QUIET_ZONE: Final = 4

#: Half-block characters, indexed by (upper module dark, lower module dark).
BLOCKS: Final = {
    (False, False): " ",
    (True, False): "▀",  # upper half
    (False, True): "▄",  # lower half
    (True, True): "█",  # full
}

#: Explicit black on white, so the symbol does not depend on the terminal's theme.
DARK_ON_LIGHT: Final = "\x1b[30;47m"
RESET: Final = "\x1b[0m"


def to_text(symbol: Symbol, quiet_zone: int = QUIET_ZONE, colour: bool = True) -> str:
    """Draw the symbol for a terminal, two module rows per text row."""
    size = symbol.size
    padded_width = size + quiet_zone * 2

    def module(row: int, column: int) -> bool:
        """Whether a module is dark, counting the quiet zone as light."""
        row -= quiet_zone
        column -= quiet_zone
        if 0 <= row < size and 0 <= column < size:
            return symbol.modules[row][column]
        return False

    lines = []
    for top in range(0, size + quiet_zone * 2, 2):
        cells = "".join(
            BLOCKS[module(top, column), module(top + 1, column)] for column in range(padded_width)
        )
        lines.append(f"{DARK_ON_LIGHT}{cells}{RESET}" if colour else cells)
    return "\n".join(lines)


def to_svg(symbol: Symbol, quiet_zone: int = QUIET_ZONE, scale: int = 8) -> str:
    """Draw the symbol as SVG.

    One path for every dark module rather than one rectangle each: a version 10 symbol has about
    1600 dark modules, and 1600 elements is a page that scrolls badly on a phone.
    """
    size = symbol.size
    extent = size + quiet_zone * 2

    parts = []
    for row in range(size):
        for column in range(size):
            if symbol.modules[row][column]:
                parts.append(f"M{column + quiet_zone} {row + quiet_zone}h1v1h-1z")

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {extent} {extent}" '
        f'width="{extent * scale}" height="{extent * scale}" shape-rendering="crispEdges" '
        f'role="img" aria-label="QR code for the SyncDrop address">'
        f'<rect width="{extent}" height="{extent}" fill="#ffffff"/>'
        f'<path d="{"".join(parts)}" fill="#000000"/>'
        f"</svg>"
    )
