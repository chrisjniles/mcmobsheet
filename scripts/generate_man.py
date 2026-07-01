#!/usr/bin/env python3
"""Regenerate man/mcmobsheet.1 from mcmobsheet._docs.MANUAL.

Run this after editing MANUAL, before tagging a release.
"""

from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))

from mcmobsheet._docs import render_man  # noqa: E402

OUTPUT = pathlib.Path(__file__).resolve().parent.parent / "man" / "mcmobsheet.1"


def main() -> int:
    OUTPUT.write_text(render_man())
    print(f"Wrote {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
