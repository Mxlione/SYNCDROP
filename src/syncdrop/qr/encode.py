"""Turning bytes into a QR matrix.

The steps, in the order the standard sets them out: encode the payload as a bit stream, split it
into blocks, compute error correction for each, interleave them, lay the result into a grid
around the patterns a scanner uses to find and orient the symbol, then try all eight masks and
keep whichever scores best.

Byte mode only. SyncDrop encodes URLs, which contain characters alphanumeric mode cannot hold,
and the saving from a numeric mode nothing here would ever use is not worth the code.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from syncdrop.qr.reedsolomon import error_correction
from syncdrop.qr.tables import (
    ALIGNMENT_CENTRES,
    EC_BLOCKS,
    MAX_VERSION,
    Level,
    byte_capacity,
    size_of,
)

#: The four-bit mode indicator for byte mode.
BYTE_MODE: Final = 0b0100

#: The bytes the standard pads with, alternating, when the payload does not fill the symbol.
PAD_BYTES: Final = (0xEC, 0x11)

#: Bits left over after the codewords, by version. They are written as zeros.
REMAINDER_BITS: Final = {1: 0, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7, 7: 0, 8: 0, 9: 0, 10: 0}

#: BCH generator for the 15-bit format information, and the mask applied afterwards so that an
#: all-zero format never produces an all-zero pattern.
FORMAT_GENERATOR: Final = 0b101_0011_0111
FORMAT_MASK: Final = 0b101_0100_0001_0010

#: BCH generator for the 18-bit version information, used from version 7. Thirteen bits:
#: x^12 + x^11 + x^10 + x^9 + x^8 + x^5 + x^2 + 1.
VERSION_GENERATOR: Final = 0b1_1111_0010_0101


class CapacityError(ValueError):
    """The payload does not fit in any version these tables cover."""


@dataclass(frozen=True, slots=True)
class Symbol:
    """A finished QR code: a square of booleans, dark where True."""

    modules: tuple[tuple[bool, ...], ...]
    version: int
    level: Level
    mask: int

    @property
    def size(self) -> int:
        """How many modules across."""
        return len(self.modules)


def smallest_version(payload: bytes, level: Level) -> int:
    """The smallest version that holds this payload at this level."""
    for version in range(1, MAX_VERSION + 1):
        if len(payload) <= byte_capacity(version, level):
            return version
    biggest = byte_capacity(MAX_VERSION, level)
    raise CapacityError(
        f"{len(payload)} bytes will not fit: version {MAX_VERSION} at level {level.name} "
        f"holds {biggest}. SyncDrop encodes URLs, which are far shorter than this."
    )


def _bit_stream(payload: bytes, version: int, level: Level) -> list[int]:
    """The payload as bits: mode, length, data, terminator and padding."""
    from syncdrop.qr.tables import data_capacity

    count_bits = 8 if version < 10 else 16
    bits: list[int] = []

    def push(value: int, width: int) -> None:
        bits.extend((value >> shift) & 1 for shift in range(width - 1, -1, -1))

    push(BYTE_MODE, 4)
    push(len(payload), count_bits)
    for byte in payload:
        push(byte, 8)

    capacity_bits = data_capacity(version, level) * 8

    # A terminator of up to four zero bits, shortened if the symbol is nearly full.
    push(0, min(4, capacity_bits - len(bits)))

    # Then to a byte boundary, then alternating pad bytes.
    if len(bits) % 8:
        push(0, 8 - len(bits) % 8)
    for index in range((capacity_bits - len(bits)) // 8):
        push(PAD_BYTES[index % 2], 8)

    return bits


def _pack(bits: list[int]) -> bytes:
    """Gather a bit stream into codewords.

    The stream is always a whole number of bytes by this point, because the padding step fills
    it to the symbol's exact data capacity.
    """
    packed = bytearray()
    for start in range(0, len(bits), 8):
        byte = 0
        for bit in bits[start : start + 8]:
            byte = (byte << 1) | bit
        packed.append(byte)
    return bytes(packed)


def _interleave(codewords: bytes, version: int, level: Level) -> bytes:
    """Split into blocks, add error correction, and weave the blocks together.

    Interleaving is what makes a QR code survive a stain rather than a scratch: damage that
    would destroy one block entirely is spread across every block, so each loses only a little
    and all of them can still be corrected.
    """
    ec_per_block, structure = EC_BLOCKS[version, level]

    data_blocks: list[bytes] = []
    offset = 0
    for count, size in structure:
        for _ in range(count):
            data_blocks.append(codewords[offset : offset + size])
            offset += size

    ec_blocks = [error_correction(block, ec_per_block) for block in data_blocks]

    woven = bytearray()
    for index in range(max(len(block) for block in data_blocks)):
        woven.extend(block[index] for block in data_blocks if index < len(block))
    for index in range(ec_per_block):
        woven.extend(block[index] for block in ec_blocks)
    return bytes(woven)


def _bch(value: int, generator: int, width: int) -> int:
    """Append a BCH check to ``value``, as the format and version information need.

    The value is shifted up by the width of the check first, and *then* reduced. Reducing before
    shifting leaves the loop with nothing to do, because the value is shorter than the generator
    — and the result still looks plausible, which is how it survived a first test written with a
    value of zero.
    """
    check = value << (width - 1)
    generator_width = generator.bit_length()
    while check.bit_length() >= generator_width:
        check ^= generator << (check.bit_length() - generator_width)
    return (value << (width - 1)) | check


def format_bits(level: Level, mask: int) -> int:
    """The fifteen bits of format information, error corrected and masked.

    Checked against the table in ISO/IEC 18004 annex C:

    >>> f"{format_bits(Level.L, 0):#06x}"
    '0x77c4'
    >>> f"{format_bits(Level.M, 0):#06x}"
    '0x5412'
    >>> f"{format_bits(Level.Q, 7):#06x}"
    '0x2bed'
    >>> f"{format_bits(Level.H, 7):#06x}"
    '0x083b'
    """
    return _bch((level.value << 3) | mask, FORMAT_GENERATOR, 11) ^ FORMAT_MASK


def version_bits(version: int) -> int:
    """The eighteen bits of version information, for version 7 and up.

    Checked against the table in ISO/IEC 18004 annex D:

    >>> f"{version_bits(7):#07x}"
    '0x07c94'
    >>> f"{version_bits(10):#07x}"
    '0x0a4d3'
    """
    return _bch(version, VERSION_GENERATOR, 13)


#: The eight mask patterns. Each says, for a module at (row, column), whether to invert it.
#: Masking exists so that no symbol ends up mostly one colour or full of runs that look like a
#: finder pattern, either of which a scanner struggles with.
MASKS: Final = (
    lambda row, column: (row + column) % 2 == 0,
    lambda row, _: row % 2 == 0,
    lambda _, column: column % 3 == 0,
    lambda row, column: (row + column) % 3 == 0,
    lambda row, column: (row // 2 + column // 3) % 2 == 0,
    lambda row, column: (row * column) % 2 + (row * column) % 3 == 0,
    lambda row, column: ((row * column) % 2 + (row * column) % 3) % 2 == 0,
    lambda row, column: ((row + column) % 2 + (row * column) % 3) % 2 == 0,
)

# The four penalty weights from the standard. They are not tuned here; changing them produces
# symbols that still scan but differ from every other encoder, which makes a comparison test
# useless.
PENALTY_RUN: Final = 3
PENALTY_BLOCK: Final = 3
PENALTY_FINDER_LOOKALIKE: Final = 40
PENALTY_IMBALANCE: Final = 10

#: The run of modules that a scanner reads as part of a finder pattern.
FINDER_LOOKALIKE: Final = (True, False, True, True, True, False, True)


def _blank(size: int) -> list[list[bool | None]]:
    """A grid with nothing decided yet. ``None`` means no module has been placed."""
    return [[None] * size for _ in range(size)]


def _place_finder(grid: list[list[bool | None]], top: int, left: int) -> None:
    """One finder pattern and its separator: the square a scanner looks for first."""
    size = len(grid)
    for row in range(-1, 8):
        for column in range(-1, 8):
            here_row, here_column = top + row, left + column
            if not (0 <= here_row < size and 0 <= here_column < size):
                continue
            # The seven-by-seven pattern, surrounded by a one-module light separator.
            inside = 0 <= row <= 6 and 0 <= column <= 6
            dark = inside and (
                row in (0, 6) or column in (0, 6) or (2 <= row <= 4 and 2 <= column <= 4)
            )
            grid[here_row][here_column] = dark


def _place_alignment(grid: list[list[bool | None]], version: int) -> None:
    """The smaller squares that let a scanner correct for a bent or angled surface."""
    centres = ALIGNMENT_CENTRES[version]
    for row_centre in centres:
        for column_centre in centres:
            # Not where a finder pattern already is.
            if (row_centre, column_centre) in {
                (centres[0], centres[0]),
                (centres[0], centres[-1]),
                (centres[-1], centres[0]),
            }:
                continue
            for row in range(-2, 3):
                for column in range(-2, 3):
                    grid[row_centre + row][column_centre + column] = max(abs(row), abs(column)) != 1


def _place_function_patterns(version: int) -> tuple[list[list[bool | None]], list[list[bool]]]:
    """Everything that is not data, and a map of where that is.

    The map matters as much as the patterns: data is laid out by walking the grid and skipping
    whatever is already spoken for, including the areas reserved for format and version
    information that are not written until a mask has been chosen.
    """
    size = size_of(version)
    grid = _blank(size)

    _place_finder(grid, 0, 0)
    _place_finder(grid, 0, size - 7)
    _place_finder(grid, size - 7, 0)

    # Timing patterns: alternating modules that tell a scanner the module pitch.
    for index in range(8, size - 8):
        grid[6][index] = index % 2 == 0
        grid[index][6] = index % 2 == 0

    _place_alignment(grid, version)

    # The one module that is always dark, for reasons the standard does not give.
    grid[size - 8][8] = True

    reserved = [[module is not None for module in row] for row in grid]

    # Format information: written later, reserved now.
    for index in range(9):
        if grid[8][index] is None:
            reserved[8][index] = True
        if grid[index][8] is None:
            reserved[index][8] = True
    for index in range(8):
        reserved[8][size - 1 - index] = True
        reserved[size - 1 - index][8] = True

    # Version information, from version 7.
    if version >= 7:
        for index in range(18):
            row, column = index // 3, index % 3
            reserved[row][size - 11 + column] = True
            reserved[size - 11 + column][row] = True

    return grid, reserved


def _place_data(
    grid: list[list[bool | None]], reserved: list[list[bool]], codewords: bytes, version: int
) -> None:
    """Walk the grid in the standard's zigzag and drop the bits in.

    Two columns at a time, from the bottom right, alternating direction. Column 6 is skipped
    entirely because it is the vertical timing pattern.
    """
    size = len(grid)
    bits = [(byte >> shift) & 1 for byte in codewords for shift in range(7, -1, -1)]
    bits.extend([0] * REMAINDER_BITS[version])

    index = 0
    column = size - 1
    upward = True
    while column > 0:
        if column == 6:
            column -= 1
        for step in range(size):
            row = size - 1 - step if upward else step
            for here in (column, column - 1):
                if reserved[row][here]:
                    continue
                grid[row][here] = bool(bits[index]) if index < len(bits) else False
                index += 1
        upward = not upward
        column -= 2


def _penalty(modules: list[list[bool]]) -> int:
    """Score a masked symbol. Lower is better.

    The four rules the standard gives, in order: long runs of one colour, solid two-by-two
    blocks, runs that a scanner could mistake for a finder pattern, and an overall imbalance
    between dark and light.
    """
    size = len(modules)
    score = 0

    # Rule 1: runs of five or more.
    for line in (*modules, *zip(*modules, strict=True)):
        run_colour = line[0]
        run_length = 1
        for module in line[1:]:
            if module == run_colour:
                run_length += 1
            else:
                if run_length >= 5:
                    score += PENALTY_RUN + run_length - 5
                run_colour = module
                run_length = 1
        if run_length >= 5:
            score += PENALTY_RUN + run_length - 5

    # Rule 2: two-by-two blocks of one colour.
    for row in range(size - 1):
        for column in range(size - 1):
            corner = modules[row][column]
            if (
                modules[row][column + 1] == corner
                and modules[row + 1][column] == corner
                and modules[row + 1][column + 1] == corner
            ):
                score += PENALTY_BLOCK

    # Rule 3: a finder-like run with four light modules on one side of it.
    light = (False,) * 4
    for line in (*modules, *zip(*modules, strict=True)):
        sequence = tuple(line)
        for start in range(size - 10):
            window = sequence[start : start + 11]
            if window[:7] == FINDER_LOOKALIKE and window[7:] == light:
                score += PENALTY_FINDER_LOOKALIKE
            if window[:4] == light and window[4:] == FINDER_LOOKALIKE:
                score += PENALTY_FINDER_LOOKALIKE

    # Rule 4: how far the proportion of dark modules sits from half, in steps of 5%.
    # The division stays in floating point: rounding the percentage to a whole number first
    # moves the result across a 5% step boundary for symbols that are close to one.
    dark = sum(sum(row) for row in modules)
    deviation = abs(dark * 100 / (size * size) - 50)
    score += PENALTY_IMBALANCE * int(deviation / 5)

    return score


def _write_format(modules: list[list[bool]], level: Level, mask: int) -> None:
    """The fifteen format bits, written twice so that losing a corner is survivable."""
    size = len(modules)
    bits = format_bits(level, mask)

    def bit(index: int) -> bool:
        """Bit ``index`` of the format information, numbered from the most significant.

        The standard numbers these 14 down to 0 and writes them in that order along the two
        sequences below. Reading them from the least significant end instead produces the mirror
        of the right answer, which still looks like a plausible QR code and does not scan.
        """
        return bool((bits >> (14 - index)) & 1)

    for index in range(6):
        modules[8][index] = bit(index)
    modules[8][7] = bit(6)
    modules[8][8] = bit(7)
    modules[7][8] = bit(8)
    for index in range(9, 15):
        modules[14 - index][8] = bit(index)

    # The second copy splits seven bits and eight, not eight and seven: the module at
    # (size - 8, 8) is the one that is always dark, so the vertical run stops one short and the
    # horizontal run starts one column earlier to make up for it. Getting this wrong leaves
    # column size - 8 never written, which is a single wrong module — enough to make a scanner
    # read the wrong mask and give up, and small enough to miss entirely by eye.
    for index in range(7):
        modules[size - 1 - index][8] = bit(index)
    for index in range(7, 15):
        modules[8][size - 15 + index] = bit(index)

    modules[size - 8][8] = True


def _write_version(modules: list[list[bool]], version: int) -> None:
    """The eighteen version bits, also written twice. Version 7 and up only."""
    size = len(modules)
    bits = version_bits(version)
    for index in range(18):
        value = bool((bits >> index) & 1)
        row, column = index // 3, index % 3
        modules[row][size - 11 + column] = value
        modules[size - 11 + column][row] = value


def encode(
    payload: bytes | str,
    level: Level = Level.M,
    version: int | None = None,
    mask: int | None = None,
) -> Symbol:
    """Encode a payload as a QR symbol.

    Every mask is tried and the lowest scoring one kept, which is what the standard requires.
    ``mask`` forces one instead, which exists so that this encoder's output can be compared
    module for module against another one: two encoders that agree on every forced mask but
    choose differently differ in their penalty scoring, not in their encoding.

    >>> symbol = encode("https://example.test")
    >>> symbol.version, symbol.level.name, symbol.size
    (2, 'M', 25)
    """
    if isinstance(payload, str):
        payload = payload.encode()
    if version is None:
        version = smallest_version(payload, level)
    elif len(payload) > byte_capacity(version, level):
        raise CapacityError(
            f"{len(payload)} bytes will not fit in version {version} at level {level.name}, "
            f"which holds {byte_capacity(version, level)}"
        )

    codewords = _interleave(_pack(_bit_stream(payload, version, level)), version, level)

    grid, reserved = _place_function_patterns(version)
    _place_data(grid, reserved, codewords, version)

    best: Symbol | None = None
    best_score = -1
    for candidate in range(len(MASKS)) if mask is None else (mask,):
        shaped = [
            [
                bool(module) ^ (MASKS[candidate](row, column) and not reserved[row][column])
                for column, module in enumerate(line)
            ]
            for row, line in enumerate(grid)
        ]
        _write_format(shaped, level, candidate)
        if version >= 7:
            _write_version(shaped, version)

        score = _penalty(shaped)
        if best is None or score < best_score:
            best = Symbol(tuple(tuple(row) for row in shaped), version, level, candidate)
            best_score = score

    assert best is not None  # noqa: S101 - there is always at least one mask
    return best
