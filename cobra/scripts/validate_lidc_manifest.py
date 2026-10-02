"""Validate a genuine TCIA LIDC manifest and XML annotation archive."""
from __future__ import annotations
import argparse, re, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

UID_RE = re.compile(r"^1\.3\.6\.1\.4\.1\.14519\.")
def manifest_uids(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    marker = "ListOfSeriesToDownload="
    if marker not in lines:
        raise ValueError("TCIA manifest has no ListOfSeriesToDownload section")
    values = []
    for line in lines[lines.index(marker)+1:]:
        line = line.strip()
        if line and UID_RE.match(line):
            values.append(line)
    if not values:
        raise ValueError("No LIDC SeriesInstanceUIDs found in manifest")
    return values

def xml_uids(zip_path: Path) -> list[str]:
    out = []
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".xml")]
        if not names:
            raise ValueError("XML archive contains no XML files")
        for name in names:
            root = ET.fromstring(z.read(name))
            for e in root.iter():
                if e.tag.split("}")[-1].lower() == "seriesinstanceuid" and e.text:
                    out.append(e.text.strip())
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--xml-zip", required=True)
    args = ap.parse_args()
    m, x = manifest_uids(Path(args.manifest)), xml_uids(Path(args.xml_zip))
    ms, xs = set(m), set(x)
    print(f"manifest_series_uids={len(ms)}")
    print(f"xml_series_uids={len(xs)}")
    print(f"intersection={len(ms & xs)}")
    print(f"xml_only={len(xs-ms)}")
    print(f"manifest_only={len(ms-xs)}")
    if not (ms & xs):
        raise SystemExit("FAIL: no SeriesInstanceUID overlap; do not proceed")
    print("PASS: non-empty SeriesInstanceUID overlap established")

if __name__ == "__main__":
    main()
