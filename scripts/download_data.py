"""Download and verify the official GSS 2022 Stata release."""

from __future__ import annotations

import hashlib
import json
import sys
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "data" / "source_manifest.json"
RAW_DIR = ROOT / "data" / "raw"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    archive = RAW_DIR / "2022_stata.zip"

    if not archive.exists():
        print(f"Downloading {manifest['source_url']}")
        urllib.request.urlretrieve(manifest["source_url"], archive)

    observed = sha256(archive)
    expected = manifest["archive_sha256"]
    if observed.lower() != expected.lower():
        raise RuntimeError(
            "The downloaded archive checksum differs from the reviewed release. "
            f"Expected {expected}; observed {observed}."
        )

    target = RAW_DIR / manifest["stata_member"]
    if not target.exists():
        with zipfile.ZipFile(archive) as bundle:
            bundle.extractall(RAW_DIR)

    print(f"Verified archive: {observed}")
    print(f"Dataset ready: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

