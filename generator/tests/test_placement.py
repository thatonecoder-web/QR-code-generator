from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.placement import place_data


def test_place_data_sets_modules():
    matrix = QRMatrix()

    bits = "10101010"

    place_data(matrix, bits)

    values = [
        matrix.get(20, 20),
        matrix.get(20, 19),
        matrix.get(19, 20),
        matrix.get(19, 19),
        matrix.get(18, 20),
        matrix.get(18, 19),
        matrix.get(17, 20),
        matrix.get(17, 19),
    ]

    assert values == [
        True,
        False,
        True,
        False,
        True,
        False,
        True,
        False,
    ]


def test_place_data_skips_reserved_modules():
    matrix = QRMatrix()

    matrix.reserve(20, 20)
    matrix.reserve(20, 19)

    place_data(matrix, "1010")

    assert matrix.get(20, 20) is None
    assert matrix.get(20, 19) is None

    assert matrix.get(19, 20) is True
    assert matrix.get(19, 19) is False


def test_place_data_skips_timing_column():
    matrix = QRMatrix()

    add_patterns(matrix)

    place_data(matrix, "1" * 100)

    for row in range(matrix.size):
        assert matrix.is_reserved(row, 6) is True


def test_place_data_does_not_overwrite_patterns():
    matrix = QRMatrix()

    add_patterns(matrix)

    original = matrix.to_list()

    place_data(matrix, "1" * 100)

    for row in range(matrix.size):
        for column in range(matrix.size):
            if matrix.is_reserved(row, column):
                assert matrix.get(row, column) == original[row][column]


def test_place_data_accepts_empty_bitstream():
    matrix = QRMatrix()

    place_data(matrix, "")

    assert matrix.get(20, 20) is None


def test_place_data_rejects_invalid_bits():
    matrix = QRMatrix()

    try:
        place_data(matrix, "10102010")
    except ValueError:
        pass
    else:
        raise AssertionError(
            "place_data() should reject bits other than 0 and 1"
        )


def test_place_data_rejects_oversized_bitstream():
    matrix = QRMatrix()

    bits = "1" * 1000

    try:
        place_data(matrix, bits)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "place_data() should reject a bitstream that is too large"
        )


def test_place_data_alternates_direction():
    matrix = QRMatrix()

    # Enough bits to reach multiple two-column strips.
    bits = "10" * 20

    place_data(matrix, bits)

    # The first strip begins at the bottom-right and travels upward.
    assert matrix.get(20, 20) is True
    assert matrix.get(20, 19) is False

    assert matrix.get(19, 20) is True
    assert matrix.get(19, 19) is False