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


def test_matrix_starts_unreserved():
    matrix = QRMatrix()

    assert matrix.is_reserved(0, 0) is False


def test_matrix_can_reserve_position():
    matrix = QRMatrix()

    matrix.reserve(5, 5)

    assert matrix.is_reserved(5, 5) is True


def test_reserved_position_can_store_value():
    matrix = QRMatrix()

    matrix.set_reserved(5, 5, True)

    assert matrix.is_reserved(5, 5) is True
    assert matrix.get(5, 5) is True


def test_reserved_position_can_store_light_module():
    matrix = QRMatrix()

    matrix.set_reserved(5, 5, False)

    assert matrix.is_reserved(5, 5) is True
    assert matrix.get(5, 5) is False


def test_reserving_does_not_change_value():
    matrix = QRMatrix()

    matrix.set(5, 5, True)
    matrix.reserve(5, 5)

    assert matrix.get(5, 5) is True
    assert matrix.is_reserved(5, 5) is True