"""Value translation helpers.

Each function converts a raw Minecraft value into a human-readable string,
following the convention: translated value with the raw value in parentheses,
e.g. "8.4 hearts (16.8)".
"""

from __future__ import annotations

import json

# Players move ~4.317 blocks/sec at a movement_speed attribute of 0.1,
# so blocks/sec = speed * 43.17.
_SPEED_TO_BLOCKS_PER_SEC = 43.17


def hearts(hp: float) -> str:
    """16.796165 -> '8.4 hearts (16.8)'  (2 HP = 1 heart)."""
    hp = float(hp)
    return f"{hp / 2:.1f} hearts ({hp:.1f})"


def speed_blocks_per_sec(speed: float) -> str:
    """0.24215 -> '~ 10.5 blocks/sec (0.242)'."""
    speed = float(speed)
    bps = speed * _SPEED_TO_BLOCKS_PER_SEC
    return f"~ {bps:.1f} blocks/sec ({speed:.3f})"


def jump_blocks(strength: float) -> str:
    """Horse jump_strength -> approximate jump height in blocks.

    Uses the polynomial from the Minecraft Wiki relating the jump_strength
    attribute to the height (in blocks) a horse can clear.
    """
    s = float(strength)
    height = (
        -0.1817584952 * s**3
        + 3.689713992 * s**2
        + 2.128599134 * s
        - 0.343930367
    )
    return f"~ {height:.1f} blocks ({s:.3f})"


def damage_hearts(amount: float) -> str:
    """Attack damage points -> hearts of damage."""
    amount = float(amount)
    return f"~ {amount / 2:.1f} hearts ({amount:g})"


def armor_points(value: float) -> str:
    """Armor attribute -> 'N/20'."""
    return f"{float(value):g}/20"


def yes_no(value) -> str:
    """Any truthy/byte value -> 'Yes' / 'No'."""
    return "Yes" if int(value) != 0 else "No"


def coords(x, y, z) -> str:
    """Round each coordinate to an integer: '-548, 66, -522'."""
    return f"{round(float(x))}, {round(float(y))}, {round(float(z))}"


def coords_from_array(arr) -> str:
    """An NBT int array [x, y, z] -> rounded coordinate string."""
    vals = [int(v) for v in arr]
    if len(vals) < 3:
        return ", ".join(str(v) for v in vals)
    return f"{vals[0]}, {vals[1]}, {vals[2]}"


def plain_text(value) -> str:
    """Resolve a CustomName into plain text.

    Handles JSON text components ('{"text":"Cloppin"}'), quoted plain
    strings, and bare strings.
    """
    s = str(value).strip()
    if s.startswith("{") or s.startswith("["):
        try:
            return _extract_text(json.loads(s))
        except (ValueError, TypeError):
            pass
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    return s


def _extract_text(component) -> str:
    """Walk a Minecraft JSON text component and concatenate its text."""
    if isinstance(component, str):
        return component
    if isinstance(component, list):
        return "".join(_extract_text(c) for c in component)
    if isinstance(component, dict):
        text = str(component.get("text", ""))
        for extra in component.get("extra", []) or []:
            text += _extract_text(extra)
        return text
    return str(component)
