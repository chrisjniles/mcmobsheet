"""Block state translation: turn block ids and states into human text."""

from __future__ import annotations

from typing import Optional

from mcmobsheet.entities.common import Row

BLOCK_EMOJI = {
    "minecraft:chest": "\U0001f4e6",
    "minecraft:furnace": "\U0001f525",
    "minecraft:torch": "\U0001f526",
    "minecraft:water": "\U0001f4a7",
    "minecraft:lava": "\U0001f30b",
}
DEFAULT_BLOCK_EMOJI = "\U0001f9f1"  # brick

# state key -> (emoji, label)
_STATE_DISPLAY = {
    "facing": ("\U0001f9ed", "Facing"),
    "half": ("↕️", "Half"),
    "axis": ("\U0001f4d0", "Axis"),
    "shape": ("\U0001f4d0", "Shape"),
    "waterlogged": ("\U0001f4a7", "Waterlogged"),
    "powered": ("⚡", "Powered"),
    "lit": ("\U0001f4a1", "Lit"),
    "open": ("\U0001f6aa", "Open"),
    "type": ("\U0001f527", "Type"),
}
_BOOL_VALUES = {"true", "false"}


def emoji_for(block_id: str) -> str:
    return BLOCK_EMOJI.get(block_id, DEFAULT_BLOCK_EMOJI)


def describe(states: dict[str, str]) -> Optional[str]:
    """Build a natural-language summary like 'facing North, upper half'."""
    parts = []
    if "facing" in states:
        parts.append(f"facing {_titleize(states['facing'])}")
    half = states.get("half")
    if half == "top":
        parts.append("upper half")
    elif half == "bottom":
        parts.append("lower half")
    if "axis" in states:
        parts.append(f"{states['axis'].upper()} axis")
    for flag in ("waterlogged", "lit", "powered", "open"):
        if states.get(flag) == "true":
            parts.append(flag)
    return ", ".join(parts) if parts else None


def state_rows(states: dict[str, str]) -> list[Row]:
    rows = []
    for key, value in states.items():
        if value in _BOOL_VALUES:
            if value == "false":
                continue  # only surface boolean states when they're on
            display_value = "Yes"
        else:
            display_value = _titleize(value)
        emoji, label = _STATE_DISPLAY.get(key, ("\U0001f4d0", _titleize(key)))
        rows.append(Row(emoji, label, display_value))
    return rows


def _titleize(value: str) -> str:
    return value.replace("_", " ").title()
