"""Block state translation: turn block ids and states into human text."""

from __future__ import annotations

from typing import Optional

from mcmobsheet.entities.common import Row

# state key -> label
_STATE_DISPLAY = {
    "facing": "Facing",
    "half": "Half",
    "axis": "Axis",
    "shape": "Shape",
    "waterlogged": "Waterlogged",
    "powered": "Powered",
    "lit": "Lit",
    "open": "Open",
    "type": "Type",
}
_BOOL_VALUES = {"true", "false"}


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
        label = _STATE_DISPLAY.get(key, _titleize(key))
        rows.append(Row(label, display_value))
    return rows


def _titleize(value: str) -> str:
    return value.replace("_", " ").title()
