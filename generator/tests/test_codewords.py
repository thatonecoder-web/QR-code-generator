import pytest

from qr_generator.codewords import (
    bits_to_codewords,
    codewords_to_bits,
    split_into_blocks,
    interleave,
    build_final_codewords,
)


def test_bits_to_codewords():
    assert bits_to_codewords("0000000111111111") == [1, 255]


def test_bits_to_codewords_rejects_non_byte_multiple():
    with pytest.raises(ValueError):
        bits_to_codewords("0000000")


def test_codewords_to_bits():
    assert codewords_to_bits([0, 255]) == "0000000011111111"


def test_bits_and_codewords_round_trip():
    codewords = [1, 2, 3, 254, 255]

    assert bits_to_codewords(codewords_to_bits(codewords)) == codewords


def test_split_into_blocks():
    codewords = [1, 2, 3, 4, 5, 6]

    assert split_into_blocks(codewords, [2, 4]) == [[1, 2], [3, 4, 5, 6]]


def test_split_into_blocks_rejects_mismatched_sizes():
    with pytest.raises(ValueError):
        split_into_blocks([1, 2, 3], [2, 2])


def test_interleave_equal_length_blocks():
    blocks = [[1, 2, 3], [4, 5, 6]]

    assert interleave(blocks) == [1, 4, 2, 5, 3, 6]


def test_interleave_unequal_length_blocks():
    blocks = [[1, 2], [3, 4, 5]]

    assert interleave(blocks) == [1, 3, 2, 4, 5]


def test_interleave_rejects_empty_blocks():
    with pytest.raises(ValueError):
        interleave([])


def test_build_final_codewords_length_matches_total_codewords():
    data_codewords = list(range(19))

    final = build_final_codewords(data_codewords, 1, "L")

    # 19 data codewords + 7 error correction codewords for V1-L.
    assert len(final) == 26


def test_build_final_codewords_multi_block():
    data_codewords = list(range(34))

    final = build_final_codewords(data_codewords, 3, "Q")

    # 34 data codewords (2 blocks of 17) + 2*18 EC codewords for V3-Q.
    assert len(final) == 34 + 36
