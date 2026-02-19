from __future__ import annotations

import importlib
import platform
import sys
from pathlib import Path

REQUIRED_PACKAGES = [
    "pandas",
    "numpy",
    "matplotlib",
    "scipy",
    "statsmodels",
    "sklearn",
    "openpyxl",
    "pyarrow",
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    cwd = Path.cwd().resolve()

    if cwd != root:
        print(f"ERROR: run from repo root: {root}")
        sys.exit(1)

    print(f"python={sys.version.split()[0]}")
    print(f"platform={platform.platform()}")
    print(f"cwd={cwd}")

    for pkg in REQUIRED_PACKAGES:
        importlib.import_module(pkg)
        print(f"import_ok={pkg}")

    print("OK")


if __name__ == "__main__":
    main()
