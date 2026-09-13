from qr_generator.matrix import QRMatrix


def test_default_matrix_size():
    matrix = QRMatrix()

    assert matrix.size == 21
    assert len(matrix.to_list()) == 21
    assert len(matrix.to_list()[0]) == 21


def test_matrix_set_and_get():
    matrix = QRMatrix()

    matrix.set(5, 5, True)

    assert matrix.get(5, 5) is True


def test_matrix_starts_empty():
    matrix = QRMatrix()

    assert matrix.get(0, 0) is None
