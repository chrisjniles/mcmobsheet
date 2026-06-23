"""Shared row extractors used by entity translators.

A "row" is a (label, value) pair. Extractors return a Row or None; returning
None means "not interesting, skip it" so callers can filter cleanly.
"""

from __future__ import annotations

from typing import NamedTuple, Optional

from mcmobsheet import translate


class Row(NamedTuple):
    label: str
    value: str


# Boolean tags worth surfacing only when they are set to true.
_TRUE_FLAGS = [
    ("Invulnerable", "Invulnerable"),
    ("Silent", "Silent"),
    ("NoGravity", "No Gravity"),
    ("Glowing", "Glowing"),
    ("NoAI", "No AI"),
    ("PersistenceRequired", "Won't Despawn"),
]

# Attribute id (normalized) -> (label, formatter).
_ATTRIBUTES = {
    "movementspeed": ("Move Speed", translate.speed_blocks_per_sec),
    "jumpstrength": ("Jump Height", translate.jump_blocks),
    "maxhealth": ("Max Health", translate.hearts),
    "attackdamage": ("Attack Damage", translate.damage_hearts),
    "armor": ("Armor", translate.armor_points),
}

_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def health_row(nbt) -> Optional[Row]:
    if "Health" not in nbt:
        return None
    return Row("Health", translate.hearts(nbt["Health"]))


def flag_rows(nbt) -> list[Row]:
    rows = []
    for tag, label in _TRUE_FLAGS:
        if tag in nbt and int(nbt[tag]) != 0:
            rows.append(Row(label, "Yes"))
    if int(nbt.get("Fire", 0)) > 0:
        rows.append(Row("On Fire", "Yes"))
    if int(nbt.get("Age", 0)) < 0:
        rows.append(Row("Baby", "Yes"))
    return rows


def leash_row(nbt) -> Optional[Row]:
    leash = nbt.get("leash") or nbt.get("Leash")
    if not leash:
        return None
    if _is_coord_array(leash):
        return Row("Leashed at", translate.coords_from_array(leash))
    return Row("Leashed", "Yes")


def attribute_rows(nbt) -> list[Row]:
    attributes = nbt.get("attributes") or nbt.get("Attributes") or []
    rows = []
    for attr in attributes:
        raw_id = attr.get("id", attr.get("Name", ""))
        key = _normalize_attr(raw_id)
        if key not in _ATTRIBUTES:
            continue
        base = attr.get("base", attr.get("Base"))
        if base is None:
            continue
        label, formatter = _ATTRIBUTES[key]
        rows.append(Row(label, formatter(base)))
    return rows


def effect_rows(nbt) -> list[Row]:
    effects = nbt.get("active_effects") or nbt.get("ActiveEffects") or []
    rows = []
    for eff in effects:
        raw_id = eff.get("id", eff.get("Id"))
        if not isinstance(raw_id, str):
            continue  # numeric legacy effect ids aren't worth a lookup table
        name = raw_id.split(":")[-1].replace("_", " ").title()
        level = int(eff.get("amplifier", eff.get("Amplifier", 0))) + 1
        label = f"{name} {_roman(level)}".strip()
        duration = eff.get("duration", eff.get("Duration"))
        value = _format_duration(duration)
        rows.append(Row(label, value))
    return rows


def _format_duration(ticks) -> str:
    if ticks is None:
        return "active"
    ticks = int(ticks)
    if ticks < 0:
        return "infinite"
    seconds = ticks // 20
    return f"{seconds // 60}:{seconds % 60:02d}"


def _roman(n: int) -> str:
    if 0 <= n < len(_ROMAN):
        return _ROMAN[n]
    return str(n)


def _normalize_attr(raw_id) -> str:
    text = str(raw_id).split(":")[-1].split(".")[-1]
    return text.replace("_", "").lower()


def _is_coord_array(value) -> bool:
    try:
        return len(value) >= 3 and not isinstance(value, (str, dict))
    except TypeError:
        return False
