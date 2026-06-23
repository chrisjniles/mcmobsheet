"""Shared row extractors used by entity translators.

A "row" is an (emoji, label, value) tuple. Extractors return a Row or None;
returning None means "not interesting, skip it" so callers can filter cleanly.
"""

from __future__ import annotations

from typing import NamedTuple, Optional

from mcmobsheet import translate


class Row(NamedTuple):
    emoji: str
    label: str
    value: str


# Title emoji per entity id. Falls back to a paw print for anything unlisted.
# Title emoji per entity id, covering every mob in current Minecraft (26.2).
# Emoji is decorative — the display name is always shown alongside it — so a few
# reused or approximate icons are fine. Anything unlisted falls back to a paw print.
ENTITY_EMOJI = {
    # Equines and camels
    "minecraft:horse": "🐴",
    "minecraft:donkey": "🫏",
    "minecraft:mule": "🐴",
    "minecraft:skeleton_horse": "🐴",
    "minecraft:zombie_horse": "🐴",
    "minecraft:camel": "🐪",
    "minecraft:camel_husk": "🐪",
    "minecraft:llama": "🦙",
    "minecraft:trader_llama": "🦙",
    # Farm and land passives
    "minecraft:cow": "🐄",
    "minecraft:mooshroom": "🍄",
    "minecraft:pig": "🐷",
    "minecraft:sheep": "🐑",
    "minecraft:chicken": "🐔",
    "minecraft:rabbit": "🐰",
    "minecraft:goat": "🐐",
    "minecraft:panda": "🐼",
    "minecraft:fox": "🦊",
    "minecraft:wolf": "🐺",
    "minecraft:cat": "🐱",
    "minecraft:ocelot": "🐆",
    "minecraft:parrot": "🦜",
    "minecraft:bat": "🦇",
    "minecraft:bee": "🐝",
    "minecraft:frog": "🐸",
    "minecraft:tadpole": "🐸",
    "minecraft:turtle": "🐢",
    "minecraft:armadillo": "🦔",
    "minecraft:sniffer": "🦕",
    "minecraft:allay": "🧚",
    "minecraft:polar_bear": "🐻‍❄️",
    # Golems and constructs
    "minecraft:iron_golem": "🗿",
    "minecraft:snow_golem": "⛄",
    "minecraft:copper_golem": "🤖",
    # Aquatic
    "minecraft:cod": "🐟",
    "minecraft:salmon": "🐟",
    "minecraft:tropical_fish": "🐠",
    "minecraft:pufferfish": "🐡",
    "minecraft:squid": "🦑",
    "minecraft:glow_squid": "🦑",
    "minecraft:dolphin": "🐬",
    "minecraft:axolotl": "🦎",
    "minecraft:nautilus": "🐚",
    "minecraft:zombie_nautilus": "🐚",
    # Nether
    "minecraft:strider": "🔥",
    "minecraft:hoglin": "🐗",
    "minecraft:zoglin": "🐗",
    "minecraft:piglin": "🐽",
    "minecraft:piglin_brute": "🐽",
    "minecraft:zombified_piglin": "🧟",
    "minecraft:blaze": "🔥",
    "minecraft:magma_cube": "🟧",
    "minecraft:ghast": "👻",
    "minecraft:happy_ghast": "☁️",
    # Undead and other hostiles
    "minecraft:zombie": "🧟",
    "minecraft:husk": "🧟",
    "minecraft:drowned": "🧟",
    "minecraft:zombie_villager": "🧟",
    "minecraft:giant": "🧟",
    "minecraft:skeleton": "💀",
    "minecraft:stray": "💀",
    "minecraft:bogged": "💀",
    "minecraft:wither_skeleton": "💀",
    "minecraft:parched": "💀",
    "minecraft:creeper": "💣",
    "minecraft:spider": "🕷️",
    "minecraft:cave_spider": "🕷️",
    "minecraft:silverfish": "🐛",
    "minecraft:endermite": "🐛",
    "minecraft:enderman": "👤",
    "minecraft:slime": "🟩",
    "minecraft:sulfur_cube": "🟨",
    "minecraft:witch": "🧙",
    "minecraft:vex": "👿",
    "minecraft:phantom": "🦇",
    "minecraft:warden": "👹",
    "minecraft:breeze": "🌀",
    "minecraft:creaking": "🪵",
    "minecraft:shulker": "📦",
    "minecraft:guardian": "🐡",
    "minecraft:elder_guardian": "🐡",
    # Illagers and raids
    "minecraft:pillager": "🏹",
    "minecraft:vindicator": "🪓",
    "minecraft:evoker": "🔮",
    "minecraft:illusioner": "🎭",
    "minecraft:ravager": "🐂",
    # Villagers and traders
    "minecraft:villager": "🧑‍🌾",
    "minecraft:wandering_trader": "🧳",
    # Bosses
    "minecraft:ender_dragon": "🐉",
    "minecraft:wither": "☠️",
}
DEFAULT_ENTITY_EMOJI = "🐾"  # paw prints

# Boolean tags worth surfacing only when they are set to true.
_TRUE_FLAGS = [
    ("Invulnerable", "\U0001f6e1️", "Invulnerable"),
    ("Silent", "\U0001f507", "Silent"),
    ("NoGravity", "\U0001f388", "No Gravity"),
    ("Glowing", "✨", "Glowing"),
    ("NoAI", "\U0001f6ab", "No AI"),
    ("PersistenceRequired", "\U0001f4cc", "Won't Despawn"),
]

# Attribute id (normalized) -> (emoji, label, formatter).
_ATTRIBUTES = {
    "movementspeed": ("\U0001f3c3", "Move Speed", translate.speed_blocks_per_sec),
    "jumpstrength": ("⬆️", "Jump Height", translate.jump_blocks),
    "maxhealth": ("\U0001f4aa", "Max Health", translate.hearts),
    "attackdamage": ("⚔️", "Attack Damage", translate.damage_hearts),
    "armor": ("\U0001f9ba", "Armor", translate.armor_points),
}

_ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]


def health_row(nbt) -> Optional[Row]:
    if "Health" not in nbt:
        return None
    return Row("❤️", "Health", translate.hearts(nbt["Health"]))


def flag_rows(nbt) -> list[Row]:
    rows = []
    for tag, emoji, label in _TRUE_FLAGS:
        if tag in nbt and int(nbt[tag]) != 0:
            rows.append(Row(emoji, label, "Yes"))
    if int(nbt.get("Fire", 0)) > 0:
        rows.append(Row("\U0001f525", "On Fire", "Yes"))
    if int(nbt.get("Age", 0)) < 0:
        rows.append(Row("\U0001f37c", "Baby", "Yes"))
    return rows


def leash_row(nbt) -> Optional[Row]:
    leash = nbt.get("leash") or nbt.get("Leash")
    if not leash:
        return None
    if _is_coord_array(leash):
        return Row("\U0001f517", "Leashed at", translate.coords_from_array(leash))
    return Row("\U0001f517", "Leashed", "Yes")


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
        emoji, label, formatter = _ATTRIBUTES[key]
        rows.append(Row(emoji, label, formatter(base)))
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
        rows.append(Row("\U0001f9ea", label, value))
    return rows


def _format_duration(ticks) -> str:
    if ticks is None:
        return "active"
    ticks = int(ticks)
    if ticks < 0:
        return "∞"  # infinity
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
