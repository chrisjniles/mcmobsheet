"""Canonical documentation text, shared by `mcmobsheet help` and the man page.

`scripts/generate_man.py` renders MANUAL into man/mcmobsheet.1. When MANUAL
changes, regenerate that file as part of the release checklist.
"""

from __future__ import annotations

from mcmobsheet import __version__

MANUAL = f"""\
NAME
    mcmobsheet - translate Minecraft /summon and /setblock data into
    readable info

SYNOPSIS
    mcmobsheet [COMMAND ...]
    mcmobsheet help
    mcmobsheet --version

DESCRIPTION
    mcmobsheet takes a /summon or /setblock command, as copied from
    Minecraft's F3+I debug screen, and prints a plain-text summary: mob
    name, health, location, equipment, block facing/state, and similar
    details depending on what was summoned or placed.

    There are three ways to give it a command:

    Argument mode
        Pass the command as arguments:

            mcmobsheet /summon minecraft:creeper 0 64 0 {{Health: 20.0f}}

    Pipe mode
        Pipe the command in on stdin:

            echo '/summon minecraft:creeper 0 64 0 {{Health: 20.0f}}' | mcmobsheet

    Interactive mode
        Run mcmobsheet with no arguments and stdin attached to a
        terminal. It prompts for one command at a time:

            $ mcmobsheet
            mcmobsheet - paste a /summon or /setblock command (from F3+I) and press Enter.
            Type 'help' for the manual, 'quit' or Ctrl+D to exit.

            mcmobsheet> /summon minecraft:creeper 0 64 0 {{Health: 20.0f}}

        Type 'help' or '?' at the prompt to see this manual again.
        Type 'quit', 'exit', or press Ctrl+D to leave.

EXIT STATUS
    0   The command was parsed and a summary was printed.
    1   The input could not be parsed as a /summon or /setblock command.

VERSION
    mcmobsheet {__version__}

SEE ALSO
    https://github.com/chrisjniles/mcmobsheet
"""


def render_man() -> str:
    """Render MANUAL as a roff man page (used by scripts/generate_man.py)."""
    out = [f'.TH MCMOBSHEET 1 "" "mcmobsheet {__version__}" "User Commands"', ".nf"]
    for line in MANUAL.splitlines():
        if line and line == line.upper() and line[0].isalpha() and not line.startswith(" "):
            out.append(".fi")
            out.append(f".SH {line}")
            out.append(".nf")
            continue
        escaped = line.replace("\\", "\\\\")
        if escaped.startswith("."):
            escaped = "\\&" + escaped
        out.append(escaped)
    out.append(".fi")
    return "\n".join(out) + "\n"
