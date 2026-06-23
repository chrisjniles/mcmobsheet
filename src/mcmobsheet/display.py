"""Render parsed commands into sectioned, human-readable stat sheets."""

from __future__ import annotations

from mcmobsheet import translate
from mcmobsheet.blocks import common as blocks
from mcmobsheet.entities import get_translator
from mcmobsheet.types import SetblockCommand, SummonCommand

REPO_URL = "https://github.com/chrisjniles/mcmobsheet"

_SECTION_WIDTH = 42


def render(cmd) -> str:
    if isinstance(cmd, SummonCommand):
        return render_summon(cmd)
    if isinstance(cmd, SetblockCommand):
        return render_setblock(cmd)
    raise TypeError(f"don't know how to render {type(cmd).__name__}")


def render_summon(cmd: SummonCommand) -> str:
    translator = get_translator(cmd)
    custom = translator.custom_name()

    lines = [_title(cmd.entity_name, custom)]
    lines.append(f"Location: {translate.coords(cmd.x, cmd.y, cmd.z)}")

    for title, rows in translator.sections():
        lines.append("")
        lines.append(_section_header(title))
        lines.extend(_format_rows(rows))

    if translator.generic:
        lines.append("")
        lines.extend(_disclaimer())

    return "\n".join(lines)


def render_setblock(cmd: SetblockCommand) -> str:
    summary = blocks.describe(cmd.states)
    title = cmd.block_name + (f" {summary}" if summary else "")

    lines = [title]
    lines.append(f"Location: {translate.coords(cmd.x, cmd.y, cmd.z)}")

    rows = blocks.state_rows(cmd.states)
    if rows:
        lines.append("")
        lines.append(_section_header("State"))
        lines.extend(_format_rows(rows))

    return "\n".join(lines)


def _title(name: str, custom_name) -> str:
    if custom_name:
        return f'{name} - "{custom_name}"'
    return name


def _section_header(title: str) -> str:
    prefix = f"-- {title} "
    pad = max(0, _SECTION_WIDTH - len(prefix))
    return prefix + "-" * pad


def _format_rows(rows) -> list[str]:
    width = max(len(row.label) for row in rows)
    lines = []
    for row in rows:
        label = (row.label + ":").ljust(width + 1)
        lines.append(f"  {label} {row.value}")
    return lines


def _disclaimer() -> list[str]:
    return [
        "Best-effort display - some info may be incomplete or inaccurate.",
        f"Request mob-specific support: {REPO_URL}/issues",
    ]
