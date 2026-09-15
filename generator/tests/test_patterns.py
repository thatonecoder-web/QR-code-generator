from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns


def test_add_patterns_requires_version_1_matrix():
    matrix = QRMatrix(25)

    try:
        add_patterns(matrix)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "add_patterns() should reject non-Version 1 matrices"
        )


def test_top_left_finder_pattern():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.get(0, 0) is True
    assert matrix.get(1, 1) is True
    assert matrix.get(2, 2) is True
    assert matrix.get(3, 3) is True
    assert matrix.get(4, 4) is True
    assert matrix.get(1, 1) is True
    assert matrix.get(1, 2) is False


def test_top_right_finder_pattern():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.get(0, 20) is True
    assert matrix.get(1, 19) is True
    assert matrix.get(3, 17) is True
    assert matrix.get(6, 20) is True


def test_bottom_left_finder_pattern():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.get(20, 0) is True
    assert matrix.get(19, 1) is True
    assert matrix.get(17, 3) is True
    assert matrix.get(14, 0) is True


def test_finder_pattern_centers_are_dark():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.get(3, 3) is True
    assert matrix.get(3, 17) is True
    assert matrix.get(17, 3) is True


def test_finder_separators_are_light():
    matrix = QRMatrix()

    add_patterns(matrix)

    # Top-left separator
    assert matrix.get(0, 7) is False
    assert matrix.get(7, 0) is False

    # Top-right separator
    assert matrix.get(0, 13) is False
    assert matrix.get(7, 20) is False

    # Bottom-left separator
    assert matrix.get(13, 0) is False
    assert matrix.get(20, 7) is False


def test_finder_patterns_are_reserved():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.is_reserved(0, 0) is True
    assert matrix.is_reserved(3, 3) is True
    assert matrix.is_reserved(0, 20) is True
    assert matrix.is_reserved(20, 0) is True


def test_finder_separators_are_reserved():
    matrix = QRMatrix()

    add_patterns(matrix)

    assert matrix.is_reserved(0, 7) is True
    assert matrix.is_reserved(7, 0) is True
    assert matrix.is_reserved(0, 13) is True
    assert matrix.is_reserved(7, 20) is True


def test_horizontal_timing_pattern():
    matrix = QRMatrix()

    add_patterns(matrix)

    for column in range(8, 13):
        assert matrix.get(6, column) is (column % 2 == 0)
        assert matrix.is_reserved(6, column) is True


def test_vertical_timing_pattern():
    matrix = QRMatrix()

    add_patterns(matrix)

    for row in range(8, 13):
        assert matrix.get(row, 6) is (row % 2 == 0)
        assert matrix.is_reserved(row, 6) is True


def test_timing_patterns_alternate():
    matrix = QRMatrix()

    add_patterns(matrix)

    horizontal = [
        matrix.get(6, column)
        for column in range(8, 13)
    ]

    vertical = [
        matrix.get(row, 6)
        for row in range(8, 13)
    ]

    assert horizontal == [True, False, True, False, True]
    assert vertical == [True, False, True, False, True]