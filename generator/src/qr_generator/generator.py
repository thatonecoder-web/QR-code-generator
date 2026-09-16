"""The unified, end-to-end QR Code generation pipeline."""

from qr_generator import version_info
from qr_generator.matrix import QRMatrix
from qr_generator.patterns import add_patterns
from qr_generator.placement import place_data
from qr_generator.encoder import encode_and_pad
from qr_generator.codewords import bits_to_codewords, build_final_codewords
from qr_generator.mask import select_best_mask
from qr_generator.format_info import add_format_information


def generate(data: str, error_correction: str = "M") -> QRMatrix:
    """Generate a complete, scannable QR Code matrix for text data.

    Automatically selects the smallest supported version (1-4) that
    fits the data at the requested error correction level ("L", "M",
    "Q", or "H"), then runs the full pipeline: encoding, padding,
    error correction, codeword interleaving, matrix placement,
    automatic best-mask selection, and format information.
    """
    if error_correction not in version_info.ERROR_CORRECTION_LEVELS:
        raise ValueError(
            "error_correction must be one of "
            f"{version_info.ERROR_CORRECTION_LEVELS}"
        )

    encoded_length = len(data.encode("utf-8"))
    version = version_info.choose_version(encoded_length, error_correction)

    return generate_for_version(data, version, error_correction)


def generate_for_version(
    data: str,
    version: int,
    error_correction: str,
) -> QRMatrix:
    """Generate a QR Code matrix for an explicit version and level."""
    data_bits = encode_and_pad(data, version, error_correction)
    data_codewords = bits_to_codewords(data_bits)

    final_codewords = build_final_codewords(
        data_codewords,
        version,
        error_correction,
    )
    final_bits = "".join(format(codeword, "08b") for codeword in final_codewords)
    final_bits += "0" * version_info.remainder_bits(version)

    size = version_info.matrix_size(version)
    matrix = QRMatrix(size)
    add_patterns(matrix, version)
    place_data(matrix, final_bits)

    mask_id, masked_matrix = select_best_mask(matrix)
    add_format_information(masked_matrix, error_correction, mask_id)

    return masked_matrix
