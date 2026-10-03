"""Reed-Solomon error correction over GF(256), as QR codes use it.

A QR code works when it is scratched, folded or half lit because every symbol carries error
correction codewords computed here. The arithmetic is in GF(256) with the primitive polynomial
``x^8 + x^4 + x^3 + x^2 + 1`` (0x11D), which is the field QR specifies.

Multiplication in a Galois field is addition of logarithms, so two 256-entry tables turn every
multiply into two lookups and an add. They are built once at import, which is a few microseconds
and keeps the constants out of the source where a typo would be invisible.
"""

from __future__ import annotations

from typing import Final

#: The primitive polynomial QR uses, from ISO/IEC 18004.
PRIMITIVE: Final = 0x11D

#: Field size. Every value is a byte.
FIELD_SIZE: Final = 256


def _build_tables() -> tuple[list[int], list[int]]:
    """Build the exponent and logarithm tables for GF(256)."""
    exponent = [0] * (FIELD_SIZE * 2)
    logarithm = [0] * FIELD_SIZE

    value = 1
    for power in range(FIELD_SIZE - 1):
        exponent[power] = value
        logarithm[value] = power
        value <<= 1
        if value & FIELD_SIZE:
            value ^= PRIMITIVE

    # Doubling the exponent table means a product of two logarithms never needs a modulo.
    for power in range(FIELD_SIZE - 1, FIELD_SIZE * 2):
        exponent[power] = exponent[power - (FIELD_SIZE - 1)]

    return exponent, logarithm


EXPONENT, LOGARITHM = _build_tables()


def multiply(left: int, right: int) -> int:
    """Multiply two field elements.

    >>> multiply(0, 123)
    0
    >>> multiply(1, 123)
    123
    >>> multiply(2, 128)
    29
    """
    if left == 0 or right == 0:
        return 0
    return EXPONENT[LOGARITHM[left] + LOGARITHM[right]]


def generator_polynomial(degree: int) -> list[int]:
    """The polynomial whose roots are the first ``degree`` powers of 2.

    Dividing the data by this leaves the error correction codewords as the remainder.

    >>> generator_polynomial(2)
    [1, 3, 2]
    """
    polynomial = [1]
    for power in range(degree):
        # Multiply by (x - 2^power), which in this field is (x + 2^power).
        multiplier = EXPONENT[power]
        extended = [*polynomial, 0]
        for index in range(len(polynomial)):
            extended[index + 1] ^= multiply(polynomial[index], multiplier)
        polynomial = extended
    return polynomial


def error_correction(data: bytes, count: int) -> bytes:
    """The ``count`` error correction codewords for ``data``.

    Polynomial long division: the remainder of the data, shifted up by ``count`` places, divided
    by the generator polynomial of that degree.

    The worked example from ISO/IEC 18004, which is how this implementation was checked:

    >>> data = bytes([32, 91, 11, 120, 209, 114, 220, 77, 67, 64, 236, 17, 236])
    >>> list(error_correction(data, 13))
    [168, 72, 22, 82, 217, 54, 156, 0, 46, 15, 180, 122, 16]
    """
    generator = generator_polynomial(count)
    remainder = list(data) + [0] * count

    for index in range(len(data)):
        leading = remainder[index]
        if leading == 0:
            continue
        for offset, coefficient in enumerate(generator):
            remainder[index + offset] ^= multiply(coefficient, leading)

    return bytes(remainder[len(data) :])
