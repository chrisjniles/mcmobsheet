"""Parse raw /summon and /setblock command strings into structured data."""

from __future__ import annotations

import re

from mcmobsheet import snbt
from mcmobsheet.types import SetblockCommand, SummonCommand

_BLOCK_STATE_RE = re.compile(r"^([^\[\]{}]+)(?:\[(.*)\])?$")


def parse_command(text: str):
    """Parse a /summon or /setblock command into a SummonCommand or SetblockCommand."""
    text = text.strip()
    if text.startswith("/"):
        text = text[1:]

    header, nbt_str = _split_nbt(text)
    tokens = header.split()
    if not tokens:
        raise ValueError("empty command")

    cmd = tokens[0].lower()
    if cmd == "summon":
        return _parse_summon(tokens, nbt_str)
    if cmd == "setblock":
        return _parse_setblock(tokens, nbt_str)
    raise ValueError(f"unsupported command {cmd!r} (expected 'summon' or 'setblock')")


def _split_nbt(text: str):
    """Split a command into (header, nbt_string_or_None) at the first '{'.

    Block states use square brackets, so the first curly brace reliably marks
    the start of the SNBT payload.
    """
    idx = text.find("{")
    if idx == -1:
        return text.strip(), None
    return text[:idx].strip(), text[idx:].strip()


def _parse_nbt(nbt_str):
    if not nbt_str:
        return {}
    try:
        result = snbt.parse(nbt_str)
    except Exception:
        # A malformed NBT blob shouldn't sink the whole command; show what we can.
        return {}
    return result if isinstance(result, dict) else {}


def _parse_summon(tokens, nbt_str) -> SummonCommand:
    if len(tokens) < 2:
        raise ValueError("summon command is missing an entity id")
    entity_id = _normalize_id(tokens[1])
    x = y = z = 0.0
    coords = tokens[2:5]
    if len(coords) == 3:
        x, y, z = (_coord(c) for c in coords)
    return SummonCommand(
        entity_id=entity_id,
        entity_name=_name_from_id(entity_id),
        x=x,
        y=y,
        z=z,
        nbt=_parse_nbt(nbt_str),
    )


def _parse_setblock(tokens, nbt_str) -> SetblockCommand:
    if len(tokens) < 5:
        raise ValueError("setblock command is missing coordinates or a block id")
    x = round(_coord(tokens[1]))
    y = round(_coord(tokens[2]))
    z = round(_coord(tokens[3]))
    block_id, states = _split_block_states(tokens[4])
    block_id = _normalize_id(block_id)
    return SetblockCommand(
        block_id=block_id,
        block_name=_name_from_id(block_id),
        x=x,
        y=y,
        z=z,
        states=states,
        nbt=_parse_nbt(nbt_str),
    )


def _split_block_states(token: str):
    """'oak_stairs[facing=north,half=top]' -> ('oak_stairs', {'facing': 'north', 'half': 'top'})."""
    match = _BLOCK_STATE_RE.match(token)
    if not match:
        return token, {}
    block_id = match.group(1)
    states: dict[str, str] = {}
    if match.group(2):
        for pair in match.group(2).split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                states[key.strip()] = value.strip()
    return block_id, states


def _coord(token: str) -> float:
    """Parse a coordinate, tolerating relative (~) and local (^) prefixes."""
    token = token.strip()
    if token[:1] in ("~", "^"):
        rest = token[1:]
        return float(rest) if rest else 0.0
    try:
        return float(token)
    except ValueError:
        return 0.0


def _normalize_id(raw: str) -> str:
    raw = raw.strip()
    if ":" not in raw:
        raw = "minecraft:" + raw
    return raw


def _name_from_id(full_id: str) -> str:
    name = full_id.split(":", 1)[-1]
    return name.replace("_", " ").title()
