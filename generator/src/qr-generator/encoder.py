"""Data encoding functionality for QR-generator."""

def encode(data: str) -> bytes:
"""Encode text data into bytes.

```
This is the initial encoding layer. Full QR-specific encoding,
including mode indicators, character counts, and error correction,
will be implemented in later versions.
"""
if not isinstance(data, str):
    raise TypeError("data must be a string")

return data.encode("utf-8")
```

