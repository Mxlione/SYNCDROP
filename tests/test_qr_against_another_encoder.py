"""Compare SyncDrop's QR encoder against an independent one, module for module.

This is the test that decides whether the encoder is right. Everything else checks a piece in
isolation; this checks the whole thing against somebody else's reading of the same standard.

The mask is forced on both sides. Mask selection is a scoring decision, and the two
implementations score differently — python-qrcode's third penalty rule looks for the seven
module finder pattern without requiring the four light modules the standard asks for. A symbol
with a different mask is still correct, so comparing the chosen masks would fail for a reason
that does not matter. Comparing every mask leaves nowhere for an encoding error to hide.

Writing this found three real bugs, each of which produced a symbol that looked exactly like a
QR code and would not scan:

- The BCH check was computed before the value was shifted, so the loop never ran. A first test
  written with a value of zero passed anyway.
- The format information was written least significant bit first, giving the mirror of the
  right answer.
- The second copy of the format information split its fifteen bits eight and seven instead of
  seven and eight, leaving one module in a 21-module row never written at all.
"""

from __future__ import annotations

import random

import pytest

from syncdrop.qr.encode import encode
from syncdrop.qr.tables import MAX_VERSION, Level

qrcode = pytest.importorskip("qrcode", reason="the independent encoder is not installed")

LEVELS = {
    Level.L: qrcode.constants.ERROR_CORRECT_L,
    Level.M: qrcode.constants.ERROR_CORRECT_M,
    Level.Q: qrcode.constants.ERROR_CORRECT_Q,
    Level.H: qrcode.constants.ERROR_CORRECT_H,
}


def their_matrix(text: str, level: Level, mask: int) -> list[list[bool]] | None:
    """The other encoder's symbol, or None when it needs a version beyond these tables."""
    from qrcode.util import MODE_8BIT_BYTE, QRData

    code = qrcode.QRCode(
        version=None, error_correction=LEVELS[level], box_size=1, border=0, mask_pattern=mask
    )
    code.add_data(QRData(text.encode(), mode=MODE_8BIT_BYTE))
    code.make(fit=True)
    if code.version > MAX_VERSION:
        return None
    return [[bool(module) for module in row] for row in code.get_matrix()]


def compare(text: str, level: Level, mask: int) -> None:
    """Assert both encoders produce exactly the same symbol."""
    theirs = their_matrix(text, level, mask)
    if theirs is None:
        pytest.skip("needs a version beyond these tables")
    mine = [
        list(row) for row in encode(text, level, version=len(theirs) // 4 - 4, mask=mask).modules
    ]
    assert len(mine) == len(theirs), "different sizes"
    wrong = [
        (row, column)
        for row in range(len(mine))
        for column in range(len(mine))
        if mine[row][column] != theirs[row][column]
    ]
    assert not wrong, f"{len(wrong)} modules differ, first at {wrong[0]}"


@pytest.mark.parametrize("level", list(Level), ids=lambda level: level.name)
@pytest.mark.parametrize("mask", range(8))
def test_a_url_matches_for_every_level_and_mask(level: Level, mask: int) -> None:
    compare("http://192.168.1.42:8080/?s=7f3a9c21", level, mask)


@pytest.mark.parametrize("length", [1, 7, 8, 13, 14, 15, 40, 100, 200])
def test_payload_lengths_around_the_padding_boundaries(length: int) -> None:
    """Lengths that fill a symbol exactly, and lengths that leave it needing padding.

    The padding rule is where two implementations most easily disagree, and a payload that
    happens to fill the symbol exactly hides the disagreement entirely.
    """
    compare("A" * length, Level.M, mask=0)


@pytest.mark.slow
def test_random_payloads_across_versions_and_levels() -> None:
    """A sweep wide enough that a bug in one version or one level cannot hide."""
    generator = random.Random(20260103)
    checked = 0
    for _ in range(25):
        length = generator.randrange(1, 200)
        text = "".join(
            generator.choice("abcdefghijklmnopqrstuvwxyz0123456789:/.?=-") for _ in range(length)
        )
        for level in Level:
            for mask in range(8):
                if their_matrix(text, level, mask) is None:
                    continue
                compare(text, level, mask)
                checked += 1
    assert checked > 500, f"only {checked} symbols compared; the sweep is not covering enough"
