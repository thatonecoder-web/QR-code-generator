import pytest

from qr_generator import version_info
from qr_generator.generator import generate, generate_for_version
from qr_generator.mask import apply_mask
from qr_generator.format_info import (
    encode_format_information,
    read_format_information,
)
from qr_generator.codewords import bits_to_codewords, codewords_to_bits


def _read_zig_zag_bits(matrix):
    """Replay the exact placement traversal, but reading instead of writing."""
    bits = []
    column = matrix.size - 1
    upward = True

    while column > 0:
        if column == 6:
            column -= 1

        rows = range(matrix.size - 1, -1, -1) if upward else range(matrix.size)

        for row in rows:
            for current_column in (column, column - 1):
                if matrix.is_reserved(row, current_column):
                    continue

                bits.append("1" if matrix.get(row, current_column) else "0")

        upward = not upward
        column -= 2

    return "".join(bits)


def _decode_mask_and_level(matrix):
    bits = read_format_information(matrix)

    for level in version_info.ERROR_CORRECTION_LEVELS:
        for mask_id in range(8):
            if encode_format_information(level, mask_id) == bits:
                return level, mask_id

    raise AssertionError("format information does not match any known combination")


def _decode(matrix, version):
    level, mask_id = _decode_mask_and_level(matrix)
    unmasked = apply_mask(matrix, mask_id)

    bits = _read_zig_zag_bits(unmasked)
    remainder = version_info.remainder_bits(version)
    if remainder:
        bits = bits[:-remainder]

    codewords = bits_to_codewords(bits)
    block_sizes = version_info.data_block_sizes(version, level)
    total_data = sum(block_sizes)
    data_part = codewords[:total_data]

    # De-interleave the data codewords back into their original blocks.
    blocks = [[] for _ in block_sizes]
    index = 0
    for position in range(max(block_sizes)):
        for block_index, size in enumerate(block_sizes):
            if position < size:
                blocks[block_index].append(data_part[index])
                index += 1

    data_codewords = [codeword for block in blocks for codeword in block]
    bits = codewords_to_bits(data_codewords)

    assert bits[:4] == "0100", "mode indicator must be byte mode"
    count = int(bits[4:12], 2)
    payload_bits = bits[12:12 + count * 8]
    payload_bytes = bytes(
        int(payload_bits[i:i + 8], 2)
        for i in range(0, len(payload_bits), 8)
    )

    return payload_bytes.decode("utf-8"), level, mask_id


@pytest.mark.parametrize("version", [1, 2, 3, 4])
@pytest.mark.parametrize("level", version_info.ERROR_CORRECTION_LEVELS)
def test_generation_is_scannable(version, level):
    """The generated matrix decodes back to the original text exactly."""
    capacity = version_info.max_byte_capacity(version, level)
    data = ("QR-generator round trip! " * 10)[:capacity]

    matrix = generate_for_version(data, version, level)

    decoded_text, decoded_level, _ = _decode(matrix, version)

    assert decoded_text == data
    assert decoded_level == level


@pytest.mark.parametrize("version", [1, 2, 3, 4])
@pytest.mark.parametrize("level", version_info.ERROR_CORRECTION_LEVELS)
def test_error_correction_codewords_are_recomputable(version, level):
    """Extracted error-correction codewords match freshly-generated ones."""
    from qr_generator.error_correction import generate_error_correction

    capacity = version_info.max_byte_capacity(version, level)
    data = ("regression check " * 10)[:capacity]

    matrix = generate_for_version(data, version, level)
    level_read, mask_id = _decode_mask_and_level(matrix)
    unmasked = apply_mask(matrix, mask_id)

    bits = _read_zig_zag_bits(unmasked)
    remainder = version_info.remainder_bits(version)
    if remainder:
        bits = bits[:-remainder]

    codewords = bits_to_codewords(bits)
    block_sizes = version_info.data_block_sizes(version, level)
    ec_per_block = version_info.error_correction_codewords_per_block(
        version, level
    )
    total_data = sum(block_sizes)
    data_part = codewords[:total_data]
    ec_part = codewords[total_data:]

    data_blocks = [[] for _ in block_sizes]
    index = 0
    for position in range(max(block_sizes)):
        for block_index, size in enumerate(block_sizes):
            if position < size:
                data_blocks[block_index].append(data_part[index])
                index += 1

    ec_blocks = [[] for _ in block_sizes]
    index = 0
    for position in range(ec_per_block):
        for block_index in range(len(block_sizes)):
            ec_blocks[block_index].append(ec_part[index])
            index += 1

    for data_block, ec_block in zip(data_blocks, ec_blocks):
        assert generate_error_correction(data_block, ec_per_block) == ec_block


def test_generate_selects_smallest_fitting_version():
    small_data = "hi"

    matrix = generate(small_data, "L")

    assert matrix.size == version_info.matrix_size(1)


def test_generate_selects_larger_version_when_needed():
    version_1_capacity = version_info.max_byte_capacity(1, "M")
    data = "x" * (version_1_capacity + 1)

    matrix = generate(data, "M")

    assert matrix.size > version_info.matrix_size(1)


def test_generate_rejects_data_too_large_for_any_supported_version():
    too_large = "x" * (version_info.max_byte_capacity(4, "H") + 1)

    with pytest.raises(ValueError):
        generate(too_large, "H")


def test_generate_rejects_invalid_error_correction_level():
    with pytest.raises(ValueError):
        generate("hello", "Z")


def test_generate_defaults_to_medium_error_correction():
    matrix = generate("hello")
    level, _ = _decode_mask_and_level(matrix)

    assert level == "M"


def test_generate_fills_every_module():
    matrix = generate("Full coverage check")

    for row in range(matrix.size):
        for col in range(matrix.size):
            assert matrix.get(row, col) is not None


def test_generate_has_the_single_always_dark_module():
    for version in [1, 2, 3, 4]:
        matrix = generate_for_version("x", version, "L")

        assert matrix.get(4 * version + 9, 8) is True
