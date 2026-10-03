"""The QR encoder.

SyncDrop encodes its own QR codes so that it has no runtime dependencies. That is only worth
doing if the output is right, and "it looked like a QR code" is not a test: a symbol with one
wrong module in the format information still looks exactly like a QR code and will not scan.

So the real test compares every module against an independent implementation, across versions,
error correction levels and all eight masks. The rest check the pieces individually, against the
worked examples and tables in ISO/IEC 18004.
"""

from __future__ import annotations

import pytest

from syncdrop.qr.encode import (
    CapacityError,
    encode,
    format_bits,
    smallest_version,
    version_bits,
)
from syncdrop.qr.reedsolomon import error_correction, generator_polynomial, multiply
from syncdrop.qr.render import QUIET_ZONE, to_svg, to_text
from syncdrop.qr.tables import EC_BLOCKS, MAX_VERSION, TOTAL_CODEWORDS, Level, byte_capacity

# The complete format information table from ISO/IEC 18004 annex C, all 32 entries.
FORMAT_TABLE = {
    (Level.L, 0): 0x77C4, (Level.L, 1): 0x72F3, (Level.L, 2): 0x7DAA, (Level.L, 3): 0x789D,
    (Level.L, 4): 0x662F, (Level.L, 5): 0x6318, (Level.L, 6): 0x6C41, (Level.L, 7): 0x6976,
    (Level.M, 0): 0x5412, (Level.M, 1): 0x5125, (Level.M, 2): 0x5E7C, (Level.M, 3): 0x5B4B,
    (Level.M, 4): 0x45F9, (Level.M, 5): 0x40CE, (Level.M, 6): 0x4F97, (Level.M, 7): 0x4AA0,
    (Level.Q, 0): 0x355F, (Level.Q, 1): 0x3068, (Level.Q, 2): 0x3F31, (Level.Q, 3): 0x3A06,
    (Level.Q, 4): 0x24B4, (Level.Q, 5): 0x2183, (Level.Q, 6): 0x2EDA, (Level.Q, 7): 0x2BED,
    (Level.H, 0): 0x1689, (Level.H, 1): 0x13BE, (Level.H, 2): 0x1CE7, (Level.H, 3): 0x19D0,
    (Level.H, 4): 0x0762, (Level.H, 5): 0x0255, (Level.H, 6): 0x0D0C, (Level.H, 7): 0x083B,
}  # fmt: skip

# Version information, annex D. Only versions 7 and up carry it.
VERSION_TABLE = {7: 0x07C94, 8: 0x085BC, 9: 0x09A99, 10: 0x0A4D3}


class TestReedSolomon:
    def test_the_worked_example_from_the_standard(self) -> None:
        """ISO/IEC 18004's own example, which is what this was checked against first."""
        data = bytes([32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236])
        assert list(error_correction(data, 13)) == [
            168, 72, 22, 82, 217, 54, 156, 0, 46, 15, 180, 122, 16,
        ]  # fmt: skip

    def test_a_known_generator_polynomial(self) -> None:
        """The degree 7 generator, from the table in the standard."""
        assert generator_polynomial(7) == [1, 127, 122, 154, 164, 11, 68, 117]

    def test_multiplying_by_zero(self) -> None:
        assert multiply(0, 200) == 0
        assert multiply(200, 0) == 0

    def test_multiplying_by_one(self) -> None:
        for value in range(256):
            assert multiply(1, value) == value

    def test_multiplication_commutes(self) -> None:
        for left in range(0, 256, 17):
            for right in range(0, 256, 23):
                assert multiply(left, right) == multiply(right, left)

    def test_the_right_number_of_codewords_comes_back(self) -> None:
        for count in (7, 10, 13, 17, 30):
            assert len(error_correction(b"something", count)) == count


class TestTables:
    def test_every_block_structure_accounts_for_the_whole_symbol(self) -> None:
        """Data plus error correction must be exactly the symbol's capacity, for all 40 rows.

        This is the check that catches a mistyped table, which is otherwise invisible: a wrong
        number produces symbols that encode and never scan.
        """
        for (version, level), (ec_per_block, blocks) in EC_BLOCKS.items():
            total = sum(count * (size + ec_per_block) for count, size in blocks)
            assert total == TOTAL_CODEWORDS[version], f"version {version} level {level.name}"

    def test_every_version_and_level_is_present(self) -> None:
        assert len(EC_BLOCKS) == MAX_VERSION * len(Level)

    def test_capacity_grows_with_version(self) -> None:
        for level in Level:
            capacities = [byte_capacity(v, level) for v in range(1, MAX_VERSION + 1)]
            assert capacities == sorted(capacities)

    def test_stronger_correction_holds_less(self) -> None:
        """The whole trade: more recoverable damage, fewer bytes."""
        for version in range(1, MAX_VERSION + 1):
            assert byte_capacity(version, Level.L) > byte_capacity(version, Level.H)


class TestBchCodes:
    @pytest.mark.parametrize(
        ("level", "mask"), sorted(FORMAT_TABLE, key=lambda key: (key[0].name, key[1]))
    )
    def test_format_information_matches_the_standard(self, level: Level, mask: int) -> None:
        assert format_bits(level, mask) == FORMAT_TABLE[level, mask]

    @pytest.mark.parametrize("version", sorted(VERSION_TABLE))
    def test_version_information_matches_the_standard(self, version: int) -> None:
        assert version_bits(version) == VERSION_TABLE[version]


class TestEncoding:
    def test_the_smallest_version_that_fits_is_chosen(self) -> None:
        assert smallest_version(b"A", Level.M) == 1
        assert smallest_version(b"A" * 14, Level.M) == 1
        assert smallest_version(b"A" * 15, Level.M) == 2

    def test_too_much_data_is_refused_with_the_limit(self) -> None:
        with pytest.raises(CapacityError, match="holds"):
            encode(b"A" * 5000, Level.H)

    def test_a_payload_that_will_not_fit_the_given_version(self) -> None:
        with pytest.raises(CapacityError, match="version 1"):
            encode(b"A" * 100, Level.M, version=1)

    def test_the_symbol_is_square(self) -> None:
        symbol = encode("https://example.test")
        assert all(len(row) == symbol.size for row in symbol.modules)

    def test_bytes_and_text_encode_the_same(self) -> None:
        assert encode("hello").modules == encode(b"hello").modules

    @pytest.mark.parametrize("version", range(1, MAX_VERSION + 1))
    def test_finder_patterns_are_where_a_scanner_looks(self, version: int) -> None:
        """Three corners, each a dark ring around a dark centre, whatever the mask does."""
        symbol = encode(b"x" * byte_capacity(version, Level.L), Level.L, version=version)
        size = symbol.size
        for top, left in ((0, 0), (0, size - 7), (size - 7, 0)):
            assert symbol.modules[top][left], "finder corner is light"
            assert symbol.modules[top + 3][left + 3], "finder centre is light"
            assert not symbol.modules[top + 1][left + 1], "finder ring is filled in"

    def test_the_always_dark_module_is_dark(self) -> None:
        for version in range(1, MAX_VERSION + 1):
            symbol = encode(b"x", Level.M, version=version)
            assert symbol.modules[symbol.size - 8][8]


class TestRendering:
    def test_the_terminal_drawing_is_square(self) -> None:
        """Two module rows per text row, so the symbol is not twice as tall as it is wide."""
        symbol = encode("https://example.test")
        lines = to_text(symbol, colour=False).splitlines()
        width = len(lines[0])
        assert width == symbol.size + QUIET_ZONE * 2
        assert len(lines) == (width + 1) // 2

    def test_the_quiet_zone_is_there(self) -> None:
        """A scanner cannot find the edge of a symbol drawn without a margin."""
        lines = to_text(encode("x"), colour=False).splitlines()
        assert lines[0].strip() == ""
        assert lines[-1].strip() == ""

    def test_colour_can_be_turned_off(self) -> None:
        """For a terminal that does not do escape codes, and for tests."""
        assert "\x1b" not in to_text(encode("x"), colour=False)
        assert "\x1b" in to_text(encode("x"), colour=True)

    def test_the_svg_is_well_formed_enough_to_parse(self) -> None:
        # The input is this project's own output, not anything from a network.
        from xml.etree import ElementTree

        root = ElementTree.fromstring(to_svg(encode("https://example.test")))  # noqa: S314
        assert root.tag.endswith("svg")

    def test_the_svg_carries_the_quiet_zone(self) -> None:
        symbol = encode("x")
        extent = symbol.size + QUIET_ZONE * 2
        assert f'viewBox="0 0 {extent} {extent}"' in to_svg(symbol)

    def test_the_svg_has_one_path_for_every_dark_module(self) -> None:
        """One element rather than hundreds, so a phone renders it without stuttering."""
        svg = to_svg(encode("https://example.test"))
        assert svg.count("<path") == 1
