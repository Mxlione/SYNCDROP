"""The constant tables from ISO/IEC 18004 that cannot be derived.

Versions 1 to 10 only. A SyncDrop QR code carries a URL — about fifty characters including the
session token — which fits in version 3 at error correction level M. Version 10 at level L holds
271 bytes, so the limit is five times what is needed and the tables stay small enough to check
by eye against the standard.

Everything that *can* be computed is computed: the format and version information bit strings
are BCH codes, built in ``encode.py`` rather than copied.
"""

from __future__ import annotations

from enum import Enum
from typing import Final


class Level(Enum):
    """How much of the symbol can be destroyed and still read.

    The value is the two-bit field that goes into the format information, which is not the same
    as the order of correction strength — a quirk of the standard worth keeping in one place.
    """

    L = 0b01  # recovers about 7%
    M = 0b00  # about 15%
    Q = 0b11  # about 25%
    H = 0b10  # about 30%


#: Highest version these tables cover.
MAX_VERSION: Final = 10

#: Total codewords in a symbol, data and error correction together, by version.
TOTAL_CODEWORDS: Final = {
    1: 26,
    2: 44,
    3: 70,
    4: 100,
    5: 134,
    6: 172,
    7: 196,
    8: 242,
    9: 292,
    10: 346,
}

#: Error correction codewords per block, and the block structure, by version and level.
#:
#: The structure is a list of ``(how many blocks, data codewords in each)``. Two entries means
#: the symbol has two group sizes, which the standard uses to spread the remainder evenly: a
#: version 5-Q symbol is two blocks of 15 data codewords and two of 16, not four of 15.5.
EC_BLOCKS: Final[dict[tuple[int, Level], tuple[int, list[tuple[int, int]]]]] = {
    (1, Level.L): (7, [(1, 19)]),
    (1, Level.M): (10, [(1, 16)]),
    (1, Level.Q): (13, [(1, 13)]),
    (1, Level.H): (17, [(1, 9)]),
    (2, Level.L): (10, [(1, 34)]),
    (2, Level.M): (16, [(1, 28)]),
    (2, Level.Q): (22, [(1, 22)]),
    (2, Level.H): (28, [(1, 16)]),
    (3, Level.L): (15, [(1, 55)]),
    (3, Level.M): (26, [(1, 44)]),
    (3, Level.Q): (18, [(2, 17)]),
    (3, Level.H): (22, [(2, 13)]),
    (4, Level.L): (20, [(1, 80)]),
    (4, Level.M): (18, [(2, 32)]),
    (4, Level.Q): (26, [(2, 24)]),
    (4, Level.H): (16, [(4, 9)]),
    (5, Level.L): (26, [(1, 108)]),
    (5, Level.M): (24, [(2, 43)]),
    (5, Level.Q): (18, [(2, 15), (2, 16)]),
    (5, Level.H): (22, [(2, 11), (2, 12)]),
    (6, Level.L): (18, [(2, 68)]),
    (6, Level.M): (16, [(4, 27)]),
    (6, Level.Q): (24, [(4, 19)]),
    (6, Level.H): (28, [(4, 15)]),
    (7, Level.L): (20, [(2, 78)]),
    (7, Level.M): (18, [(4, 31)]),
    (7, Level.Q): (18, [(2, 14), (4, 15)]),
    (7, Level.H): (26, [(4, 13), (1, 14)]),
    (8, Level.L): (24, [(2, 97)]),
    (8, Level.M): (22, [(2, 38), (2, 39)]),
    (8, Level.Q): (22, [(4, 18), (2, 19)]),
    (8, Level.H): (26, [(4, 14), (2, 15)]),
    (9, Level.L): (30, [(2, 116)]),
    (9, Level.M): (22, [(3, 36), (2, 37)]),
    (9, Level.Q): (20, [(4, 16), (4, 17)]),
    (9, Level.H): (24, [(4, 12), (4, 13)]),
    (10, Level.L): (18, [(2, 68), (2, 69)]),
    (10, Level.M): (26, [(4, 43), (1, 44)]),
    (10, Level.Q): (24, [(6, 19), (2, 20)]),
    (10, Level.H): (28, [(6, 15), (2, 16)]),
}

#: Where the centres of the alignment patterns go, by version. Version 1 has none.
ALIGNMENT_CENTRES: Final[dict[int, list[int]]] = {
    1: [],
    2: [6, 18],
    3: [6, 22],
    4: [6, 26],
    5: [6, 30],
    6: [6, 34],
    7: [6, 22, 38],
    8: [6, 24, 42],
    9: [6, 26, 46],
    10: [6, 28, 50],
}


def size_of(version: int) -> int:
    """How many modules across a symbol of this version is.

    >>> size_of(1)
    21
    >>> size_of(10)
    57
    """
    return version * 4 + 17


def data_capacity(version: int, level: Level) -> int:
    """How many data codewords a symbol of this version and level holds.

    >>> data_capacity(1, Level.L)
    19
    >>> data_capacity(10, Level.Q)
    154
    """
    _, blocks = EC_BLOCKS[version, level]
    return sum(count * size for count, size in blocks)


def byte_capacity(version: int, level: Level) -> int:
    """How many bytes of payload fit, after the mode and length fields.

    >>> byte_capacity(3, Level.M)
    42
    >>> byte_capacity(10, Level.L)
    271
    """
    # Four bits of mode indicator, then the character count: eight bits up to version 9,
    # sixteen from version 10 in byte mode.
    header_bits = 4 + (8 if version < 10 else 16)
    return (data_capacity(version, level) * 8 - header_bits) // 8
