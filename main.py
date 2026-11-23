"""Entrypoint for the news-image-20261122 make.fun entry (Python 3.13,
standard library only).

The finished front page lives in this repository as entry.png, drawn in
code by make_image.py. This program is what the grader runs: it proves
the image still satisfies the bounty's gate — a whole PNG, every chunk
with a valid checksum, at most 1 MiB and at most 1024x1024 pixels — and
then writes it to the output directory as entry.png. The grader mounts
the output at /output; locally, point MAKEFUN_OUTPUT_DIR at any folder:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import struct
import sys
import zlib
from pathlib import Path

BYTE_LIMIT = 1024 * 1024
SIDE_LIMIT = 1024
SIGNATURE = b"\x89PNG\r\n\x1a\n"
CHUNK_OVERHEAD = 12  # length + type + CRC around every chunk's data


def read_dimensions(data):
    """Return (width, height) from a PNG byte string, or raise ValueError.

    Walks the chunk list from the signature to IEND, checking that no
    chunk is truncated and that each stored CRC matches its contents.
    """
    if data[:8] != SIGNATURE:
        raise ValueError("not a PNG: bad signature")
    offset = 8
    dimensions = None
    reached_end = False
    while offset < len(data):
        if offset + CHUNK_OVERHEAD > len(data):
            raise ValueError("file ends inside a chunk header")
        (size,) = struct.unpack_from(">I", data, offset)
        kind = data[offset + 4 : offset + 8]
        start = offset + 8
        stop = start + size
        if stop + 4 > len(data):
            raise ValueError(f"file ends inside the {kind!r} chunk")
        (crc_stored,) = struct.unpack_from(">I", data, stop)
        crc_actual = zlib.crc32(data[offset + 4 : stop]) & 0xFFFFFFFF
        if crc_actual != crc_stored:
            raise ValueError(f"checksum mismatch in the {kind!r} chunk")
        if kind == b"IHDR":
            dimensions = struct.unpack_from(">II", data, start)
        offset = stop + 4
        if kind == b"IEND":
            reached_end = True
            break
    if dimensions is None:
        raise ValueError("no IHDR chunk: the header describes no image")
    if not reached_end:
        raise ValueError("no IEND chunk: the image is not whole")
    return dimensions


def deliver(source_path, out_dir):
    """Validate the image at source_path and copy it into out_dir."""
    raw = source_path.read_bytes()
    if len(raw) > BYTE_LIMIT:
        raise ValueError(f"image is {len(raw)} bytes; the limit is {BYTE_LIMIT}")
    width, height = read_dimensions(raw)
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ValueError(f"image is {width}x{height}; the limit is 1024x1024")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(raw)
    return target, len(raw), width, height


def main():
    repo = Path(__file__).resolve().parent
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target, size, width, height = deliver(repo / "entry.png", out_dir)
    print(f"entry.png delivered to {target}: {size} bytes, {width}x{height}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
