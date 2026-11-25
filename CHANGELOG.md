# Changelog

## v0.1.8 – Complete QR Generation Pipeline

- Added QR version handling and capacity calculations.
- Added error-correction level support.
- Added data capacity validation, padding, and terminator handling.
- Added alignment pattern generation.
- Added version-specific matrix construction.
- Improved reserved-module tracking and validation.
- Added QR format-information areas.
- Implemented all 8 QR mask patterns.
- Added mask application and penalty scoring.
- Added automatic best-mask selection.
- Integrated data encoding, error correction, and codeword interleaving.
- Integrated matrix placement, format information, and masking.
- Implemented complete end-to-end QR symbol generation.
- Added a unified QR generation API.
- Added automatic QR version selection.
- Added configurable error-correction levels.
- Added real-world QR scannability validation tests.
- Expanded regression and integration test coverage.
- Updated `examples/basic.py` to demonstrate complete QR generation.
- Updated README and project documentation.
- Updated package version to `0.1.8`.

## v0.1.3 – Error Correction

- Added GF(256) arithmetic.
- Implemented Reed-Solomon error correction.
- Added generator polynomial construction.
- Added error-correction codeword generation.
- Added data and error-correction codeword interleaving.
- Added tests against known Reed-Solomon results.
- Updated package version to `0.1.3`.

## v0.1.2 – QR Matrix & Data Placement

- Added QR matrix initialization and sizing logic.
- Added QR Version 1 matrix support (21×21).
- Added reserved-module tracking.
- Added finder pattern generation.
- Added timing pattern generation.
- Implemented data-bit placement into the QR matrix.
- Added automatic placement direction and zigzag traversal.
- Added matrix validation for occupied and reserved modules.
- Added unit tests for finder patterns, timing patterns, and data placement.
- Updated `examples/basic.py` to display the generated QR matrix.
- Updated package version to `0.1.2`.
- Updated project documentation for QR matrix construction.

## v0.1.1 – Basic QR Data Encoding

- Implemented QR Code byte-mode encoding.
- Added the byte-mode indicator to encoded data.
- Added character count encoding.
- Added conversion of input bytes into QR-compatible bitstreams.
- Updated encoder tests for QR-specific bitstream output.
- Updated `examples/basic.py` to display the encoded bitstream and bit length.
- Updated package version to `0.1.1`.
- Updated project metadata and documentation for the encoding layer.

## v0.1.0 – Project Foundation

- Created the initial `QR-generator` repository structure.
- Added Python package configuration using `pyproject.toml`.
- Created the `qr_generator` package with version tracking.
- Added basic text-to-byte encoding in `encoder.py`.
- Implemented the initial `QRMatrix` class with configurable matrix sizing and get/set operations.
- Added initial unit tests for encoding and matrix functionality.
- Added the `examples/basic.py` demonstration script.
- Added `.gitignore` and development dependencies.
- Added README documentation.
- Added the MIT License.
