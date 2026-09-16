# QR-generator

A QR code generator built from scratch in Python.

QR-generator is a learning-focused implementation of the QR Code standard, built without relying on external QR-generation libraries. The goal is to understand how QR codes work internally, from data encoding and error correction to matrix construction and rendering.

## 🚧 Status

**Early development**

The project is currently being built incrementally, with features being added and tested as development progresses.

## 🎯 Goals

* Implement QR encoding from scratch
* Support multiple QR data modes
* Implement error correction
* Generate and apply QR masking patterns
* Construct valid QR matrices
* Render QR codes as images and/or SVG
* Provide a simple command-line interface
* Build a comprehensive test suite

## 🛠️ Planned Features

* [x] Basic QR matrix generation
* [ ] Numeric encoding
* [ ] Alphanumeric encoding
* [x] Byte/text encoding
* [x] Error correction
* [x] QR masking
* [x] Multiple QR versions (1-4)
* [ ] PNG rendering
* [ ] SVG rendering
* [ ] Command-line interface
* [x] Automated tests
* [x] QR decoding compatibility tests

## ✅ Current Capabilities

QR-generator can now produce complete, scannable QR Code symbols end to end:

* Byte-mode data encoding with terminator and padding
* Versions 1-4, with automatic version selection based on data length
* All four error-correction levels (L, M, Q, H)
* Reed-Solomon error correction with codeword interleaving
* Finder, separator, timing, and alignment patterns
* Format information (BCH-encoded, both copies)
* All 8 masking patterns with automatic penalty-based best-mask selection

```python
from qr_generator.generator import generate

matrix = generate("Hello, QR-generator!", error_correction="M")
print(matrix)
```

## 📚 Why?

Most QR-code libraries make generating a QR code as simple as calling one function.

That's useful, but it doesn't explain what is actually happening underneath.

QR-generator is an attempt to build that process from the ground up and learn the algorithms, mathematics, and data structures involved along the way.

## 🧪 Development

QR-generator is written in **Python** and developed incrementally using versioned releases.

The project follows a test-driven approach where practical, with each major feature being verified as development progresses.
