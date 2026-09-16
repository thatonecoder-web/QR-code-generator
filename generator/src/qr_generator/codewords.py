"""Codeword-level helpers: bit/codeword conversion and interleaving."""

from qr_generator import version_info
from qr_generator.error_correction import generate_error_correction


def bits_to_codewords(bits: str) -> list[int]:
    """Convert a bitstream into 8-bit codewords."""
    if len(bits) % 8 != 0:
        raise ValueError("Bitstream length must be a multiple of 8")

    return [
        int(bits[index:index + 8], 2)
        for index in range(0, len(bits), 8)
    ]


def codewords_to_bits(codewords: list[int]) -> str:
    """Convert codewords into an 8-bit-per-codeword bitstream."""
    return "".join(
        format(codeword, "08b")
        for codeword in codewords
    )


def split_into_blocks(
    codewords: list[int],
    block_sizes: list[int],
) -> list[list[int]]:
    """Split a flat codeword list into blocks of the given sizes."""
    if sum(block_sizes) != len(codewords):
        raise ValueError(
            "block_sizes must account for every codeword exactly once"
        )

    blocks = []
    start = 0

    for size in block_sizes:
        blocks.append(codewords[start:start + size])
        start += size

    return blocks


def interleave(blocks: list[list[int]]) -> list[int]:
    """Interleave codewords from same-position across blocks.

    Shorter blocks simply run out early and are skipped, matching the
    QR Code interleaving rule for version/level combinations with
    unequal block sizes.
    """
    if not blocks:
        raise ValueError("blocks must not be empty")

    max_length = max(len(block) for block in blocks)
    interleaved = []

    for index in range(max_length):
        for block in blocks:
            if index < len(block):
                interleaved.append(block[index])

    return interleaved


def build_final_codewords(
    data_codewords: list[int],
    version: int,
    level: str,
) -> list[int]:
    """Split data into blocks, generate EC codewords, and interleave.

    Returns the full interleaved data+error-correction codeword
    sequence, ready to be converted to bits and placed in the matrix.
    """
    block_sizes = version_info.data_block_sizes(version, level)
    ec_per_block = version_info.error_correction_codewords_per_block(
        version,
        level,
    )

    data_blocks = split_into_blocks(data_codewords, block_sizes)
    ec_blocks = [
        generate_error_correction(block, ec_per_block)
        for block in data_blocks
    ]

    return interleave(data_blocks) + interleave(ec_blocks)
