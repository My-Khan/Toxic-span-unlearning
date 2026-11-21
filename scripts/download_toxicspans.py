"""Download the three ToxicSpans source files and check them against fixed SHA-256 sums.

The files are taken from the official ToxicSpans repository (Pavlopoulos et al., 2022,
CC0 1.0) at a pinned commit, so every user starts from byte-identical data.

    python scripts/download_toxicspans.py            # saves to data/raw/
"""
import hashlib
import pathlib
import sys
import urllib.request

COMMIT = "beaf170538df8275c3447b2e26070f2f82e55272"
BASE = f"https://raw.githubusercontent.com/ipavlopoulos/toxic_spans/{COMMIT}/data/"
FILES = {
    "comments.csv": "76cd6ebd10a890d269c0a7e5e451f3da12375219906f314fd9cfb1e18b1a905f",
    "annotations.csv": "f67725aa9de73cd4ef9050222f6ae985ef0e33e8da89cb8137ffeb9a1d0fc32b",
    "spans.csv": "389c6964db5d96d79ecfe038aa4ffe04abafd64b6d6427fbad4ec7fb2c7672aa",
}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main(out_dir: str = "data/raw") -> None:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    ok = True
    for name, expected in FILES.items():
        path = out / name
        if not path.exists():
            print(f"downloading {name} ...")
            urllib.request.urlretrieve(BASE + name, path)
        got = sha256(path)
        status = "ok" if got == expected else "CHECKSUM MISMATCH"
        ok &= got == expected
        print(f"{name:16s} {status}")
    if not ok:
        sys.exit("One or more files differ from the release used in the paper.")


if __name__ == "__main__":
    main(*sys.argv[1:])
