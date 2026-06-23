"""Command-line interface with three input modes: argument, pipe, interactive."""

from __future__ import annotations

import argparse
import sys

from mcmobsheet import __version__
from mcmobsheet.display import render
from mcmobsheet.parser import parse_command

_PROMPT = "mcmobsheet> "
_BANNER = (
    "mcmobsheet - paste a /summon or /setblock command (from F3+I) and press Enter.\n"
    "Type 'quit' or press Ctrl+D to exit.\n"
)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="mcmobsheet",
        description="Translate Minecraft /summon and /setblock data into readable info.",
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="A /summon or /setblock command. Omit to read stdin or start interactive mode.",
    )
    parser.add_argument("--version", action="version", version=f"mcmobsheet {__version__}")
    args = parser.parse_args(argv)

    if args.command:
        return _process(" ".join(args.command))
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        return _process(data) if data else 0
    return _interactive()


def _interactive() -> int:
    print(_BANNER)
    while True:
        try:
            line = input(_PROMPT).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not line:
            continue
        if line.lower() in ("quit", "exit"):
            return 0
        _process(line)
        print()


def _process(text: str) -> int:
    try:
        cmd = parse_command(text)
    except Exception as exc:  # noqa: BLE001 - surface any parse failure to the user
        print(f"Could not parse command: {exc}", file=sys.stderr)
        return 1
    print(render(cmd))
    return 0
