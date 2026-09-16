"""QR version, capacity, and structural sizing information.

Only QR Code versions 1-4 are currently supported. This keeps the
capacity, alignment, and block-structure tables small while still
exercising every part of the real QR pipeline (multiple versions,
multiple error-correction levels, and multi-block interleaving).
"""

MIN_VERSION = 1
MAX_VERSION = 4

ERROR_CORRECTION_LEVELS = ("L", "M", "Q", "H")

# Bits used to identify each error-correction level in format information.
ERROR_CORRECTION_BITS = {
    "L": 0b01,
    "M": 0b00,
    "Q": 0b11,
    "H": 0b10,
}

# For each version and error-correction level: the number of
# error-correction codewords per block, and the block structure as a
# list of (block_count, data_codewords_per_block) groups.
_BLOCK_TABLE = {
    1: {
        "L": (7, [(1, 19)]),
        "M": (10, [(1, 16)]),
        "Q": (13, [(1, 13)]),
        "H": (17, [(1, 9)]),
    },
    2: {
        "L": (10, [(1, 34)]),
        "M": (16, [(1, 28)]),
        "Q": (22, [(1, 22)]),
        "H": (28, [(1, 16)]),
    },
    3: {
        "L": (15, [(1, 55)]),
        "M": (26, [(1, 44)]),
        "Q": (18, [(2, 17)]),
        "H": (22, [(2, 13)]),
    },
    4: {
        "L": (20, [(1, 80)]),
        "M": (18, [(2, 32)]),
        "Q": (26, [(2, 24)]),
        "H": (16, [(4, 9)]),
    },
}

# Alignment pattern center positions for each version. Version 1 has
# none; versions 2-4 each have exactly one (the pair combinations that
# would overlap a finder pattern are never valid, so only the
# bottom-right center remains).
_ALIGNMENT_CENTERS = {
    1: [],
    2: [(18, 18)],
    3: [(22, 22)],
    4: [(26, 26)],
}

# Extra "remainder" padding bits appended after all codeword bits,
# needed because the codeword bit count doesn't always divide the
# matrix's free modules evenly.
_REMAINDER_BITS = {
    1: 0,
    2: 7,
    3: 7,
    4: 7,
}


def matrix_size(version: int) -> int:
    """Return the module width/height of a QR matrix for a version."""
    _validate_version(version)

    return 17 + 4 * version


def alignment_centers(version: int) -> list[tuple[int, int]]:
    """Return alignment pattern center coordinates for a version."""
    _validate_version(version)

    return list(_ALIGNMENT_CENTERS[version])


def remainder_bits(version: int) -> int:
    """Return the number of remainder bits for a version."""
    _validate_version(version)

    return _REMAINDER_BITS[version]


def error_correction_codewords_per_block(version: int, level: str) -> int:
    """Return the number of error-correction codewords per block."""
    codewords_per_block, _ = _block_structure(version, level)

    return codewords_per_block


def data_block_sizes(version: int, level: str) -> list[int]:
    """Return the data-codeword size of every block, in order.

    For example, a version/level combination with groups
    ``[(2, 17), (2, 18)]`` returns ``[17, 17, 18, 18]``.
    """
    _, groups = _block_structure(version, level)

    sizes = []
    for block_count, data_codewords in groups:
        sizes.extend([data_codewords] * block_count)

    return sizes


def total_data_codewords(version: int, level: str) -> int:
    """Return the total number of data codewords across all blocks."""
    return sum(data_block_sizes(version, level))


def max_byte_capacity(version: int, level: str) -> int:
    """Return the max number of raw bytes byte-mode data can hold.

    Accounts for the 4-bit mode indicator and 8-bit character count
    indicator used in versions 1-9.
    """
    capacity_bits = total_data_codewords(version, level) * 8
    usable_bits = capacity_bits - 4 - 8

    return max(usable_bits, 0) // 8


def choose_version(data_length: int, level: str) -> int:
    """Return the smallest supported version that fits the data."""
    _validate_level(level)

    for version in range(MIN_VERSION, MAX_VERSION + 1):
        if data_length <= max_byte_capacity(version, level):
            return version

    raise ValueError(
        f"Data is too large for any supported version (max version "
        f"{MAX_VERSION}, error correction level {level})"
    )


def _block_structure(
    version: int,
    level: str,
) -> tuple[int, list[tuple[int, int]]]:
    _validate_version(version)
    _validate_level(level)

    return _BLOCK_TABLE[version][level]


def _validate_version(version: int) -> None:
    if not MIN_VERSION <= version <= MAX_VERSION:
        raise ValueError(
            f"version must be between {MIN_VERSION} and {MAX_VERSION}"
        )


def _validate_level(level: str) -> None:
    if level not in ERROR_CORRECTION_LEVELS:
        raise ValueError(
            f"error correction level must be one of "
            f"{ERROR_CORRECTION_LEVELS}"
        )
