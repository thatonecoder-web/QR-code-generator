import pytest

from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.placement import place_data
from qr_generator.mask import (
    apply_mask,
    calculate_penalty,
    select_best_mask,
    MASK_COUNT,
)


def _fully_placed_matrix(version=1, bit="1"):
    from qr_generator import version_info

    size = version_info.matrix_size(version)
    matrix = QRMatrix(size)
    add_patterns(matrix, version)

    free_modules = sum(
        1
        for row in range(size)
        for col in range(size)
        if not matrix.is_reserved(row, col)
    )
    place_data(matrix, bit * free_modules)

    return matrix


def test_mask_count_is_eight():
    assert MASK_COUNT == 8


def test_apply_mask_rejects_invalid_id():
    matrix = _fully_placed_matrix()

    with pytest.raises(ValueError):
        apply_mask(matrix, 8)

    with pytest.raises(ValueError):
        apply_mask(matrix, -1)


def test_apply_mask_leaves_reserved_modules_untouched():
    matrix = _fully_placed_matrix()

    masked = apply_mask(matrix, 0)

    for row in range(matrix.size):
        for col in range(matrix.size):
            if matrix.is_reserved(row, col):
                assert masked.get(row, col) == matrix.get(row, col)


def test_apply_mask_toggles_data_modules_according_to_pattern():
    matrix = _fully_placed_matrix(bit="0")

    masked = apply_mask(matrix, 0)

    # Mask 0 flips a module whenever (row + col) is even.
    for row in range(matrix.size):
        for col in range(matrix.size):
            if matrix.is_reserved(row, col):
                continue

            expected = (row + col) % 2 == 0
            assert masked.get(row, col) == expected


def test_apply_mask_is_its_own_inverse():
    matrix = _fully_placed_matrix()

    masked = apply_mask(matrix, 3)
    unmasked = apply_mask(masked, 3)

    for row in range(matrix.size):
        for col in range(matrix.size):
            assert unmasked.get(row, col) == matrix.get(row, col)


def test_calculate_penalty_returns_non_negative_int():
    matrix = _fully_placed_matrix()

    penalty = calculate_penalty(matrix)

    assert isinstance(penalty, int)
    assert penalty >= 0


def test_calculate_penalty_penalizes_long_runs():
    all_light = QRMatrix(21)
    for row in range(21):
        for col in range(21):
            all_light.set(row, col, False)

    checkerboard = QRMatrix(21)
    for row in range(21):
        for col in range(21):
            checkerboard.set(row, col, (row + col) % 2 == 0)

    assert calculate_penalty(all_light) > calculate_penalty(checkerboard)


def test_select_best_mask_returns_valid_id_and_matrix():
    matrix = _fully_placed_matrix()

    mask_id, masked_matrix = select_best_mask(matrix)

    assert 0 <= mask_id < MASK_COUNT
    assert masked_matrix.size == matrix.size


def test_select_best_mask_has_lowest_penalty_among_all_masks():
    matrix = _fully_placed_matrix()

    best_mask_id, best_matrix = select_best_mask(matrix)
    best_penalty = calculate_penalty(best_matrix)

    for mask_id in range(MASK_COUNT):
        candidate = apply_mask(matrix, mask_id)
        assert calculate_penalty(candidate) >= best_penalty
