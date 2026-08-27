#!/usr/bin/env python3
"""Recover the decisive deleted image from the Windows thumbnail cache."""

from __future__ import annotations

import argparse
import hashlib
import zipfile
from collections.abc import Iterator
from pathlib import Path


THUMBCACHE_MEMBER = (
    "C/Users/Max/AppData/Local/Microsoft/Windows/Explorer/thumbcache_1280.db"
)

# The same RIZZLER thumbnail occurs under two cache keys. Requiring both and
# requiring byte-identical payloads guards against choosing a malformed entry.
TARGET_CACHE_HASHES = {
    0x15C78729BE0524D8,
    0x237B7FE66E1C61D4,
}


def u32(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 4], "little")


def u64(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset : offset + 8], "little")


def iter_thumbcache_entries(database: bytes) -> Iterator[tuple[int, bytes]]:
    if database[:4] != b"CMMM" or len(database) < 24:
        raise ValueError("not a supported Windows thumbnail cache")

    offset = u32(database, 16)
    while offset + 56 <= len(database) and database[offset : offset + 4] == b"CMMM":
        entry_size = u32(database, offset + 4)
        identifier_length = u32(database, offset + 16)
        padding_size = u32(database, offset + 20)
        data_size = u32(database, offset + 24)
        if entry_size < 56 or offset + entry_size > len(database):
            raise ValueError(f"invalid CMMM entry size at offset 0x{offset:x}")

        payload_offset = offset + 56 + identifier_length + padding_size
        payload_end = payload_offset + data_size
        if payload_end > offset + entry_size:
            raise ValueError(f"payload exceeds CMMM entry at offset 0x{offset:x}")
        if data_size:
            yield u64(database, offset + 8), database[payload_offset:payload_end]
        offset += entry_size


def recover(source_zip: Path, output: Path) -> None:
    with zipfile.ZipFile(source_zip) as archive:
        database = archive.read(THUMBCACHE_MEMBER)

    matches = {
        cache_hash: payload
        for cache_hash, payload in iter_thumbcache_entries(database)
        if cache_hash in TARGET_CACHE_HASHES
    }
    missing = TARGET_CACHE_HASHES - matches.keys()
    if missing:
        formatted = ", ".join(f"{value:016x}" for value in sorted(missing))
        raise ValueError(f"missing expected cache hashes: {formatted}")

    payloads = list(matches.values())
    if payloads[0] != payloads[1]:
        raise ValueError("the two independent cache entries disagree")
    image = payloads[0]
    if not image.startswith(b"\xff\xd8\xff") or not image.endswith(b"\xff\xd9"):
        raise ValueError("recovered payload is not a complete JPEG")

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(image)
    print(f"cache hashes: {', '.join(f'{x:016x}' for x in sorted(matches))}")
    print(f"bytes: {len(image)}")
    print(f"sha256: {hashlib.sha256(image).hexdigest()}")
    print(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path, help="path to the original L3AK_APT.zip")
    parser.add_argument("output", type=Path, help="path for the recovered JPEG")
    args = parser.parse_args()
    recover(args.source_zip, args.output)


if __name__ == "__main__":
    main()
