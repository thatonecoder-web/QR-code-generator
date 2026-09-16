import pytest

from qr_generator import version_info


def test_matrix_size_by_version():
    assert version_info.matrix_size(1) == 21
    assert version_info.matrix_size(2) == 25
    assert version_info.matrix_size(3) == 29
    assert version_info.matrix_size(4) == 33


def test_matrix_size_rejects_unsupported_version():
    with pytest.raises(ValueError):
        version_info.matrix_size(0)

    with pytest.raises(ValueError):
        version_info.matrix_size(5)


def test_alignment_centers_version_1_has_none():
    assert version_info.alignment_centers(1) == []


def test_alignment_centers_for_higher_versions():
    assert version_info.alignment_centers(2) == [(18, 18)]
    assert version_info.alignment_centers(3) == [(22, 22)]
    assert version_info.alignment_centers(4) == [(26, 26)]


def test_remainder_bits():
    assert version_info.remainder_bits(1) == 0
    assert version_info.remainder_bits(2) == 7
    assert version_info.remainder_bits(3) == 7
    assert version_info.remainder_bits(4) == 7


def test_data_block_sizes_single_block():
    assert version_info.data_block_sizes(1, "L") == [19]


def test_data_block_sizes_multiple_blocks():
    assert version_info.data_block_sizes(3, "Q") == [17, 17]
    assert version_info.data_block_sizes(4, "H") == [9, 9, 9, 9]


def test_total_data_codewords():
    assert version_info.total_data_codewords(1, "L") == 19
    assert version_info.total_data_codewords(3, "Q") == 34


def test_error_correction_codewords_per_block():
    assert version_info.error_correction_codewords_per_block(1, "L") == 7
    assert version_info.error_correction_codewords_per_block(4, "H") == 16


def test_max_byte_capacity_is_positive_and_increases_with_version():
    small = version_info.max_byte_capacity(1, "H")
    large = version_info.max_byte_capacity(4, "H")

    assert small > 0
    assert large > small


def test_choose_version_picks_smallest_that_fits():
    capacity_v1 = version_info.max_byte_capacity(1, "M")

    assert version_info.choose_version(capacity_v1, "M") == 1
    assert version_info.choose_version(capacity_v1 + 1, "M") == 2


def test_choose_version_rejects_data_too_large_for_any_version():
    capacity_v4 = version_info.max_byte_capacity(4, "H")

    with pytest.raises(ValueError):
        version_info.choose_version(capacity_v4 + 1, "H")


def test_rejects_invalid_error_correction_level():
    with pytest.raises(ValueError):
        version_info.total_data_codewords(1, "Z")
