"""Translator for the horse family (horse, donkey, mule, and undead variants)."""

from __future__ import annotations

from mcmobsheet import translate
from mcmobsheet.entities import common, register
from mcmobsheet.entities.base import BaseEntityTranslator


@register(
    "minecraft:horse",
    "minecraft:donkey",
    "minecraft:mule",
    "minecraft:skeleton_horse",
    "minecraft:zombie_horse",
)
class HorseTranslator(BaseEntityTranslator):
    generic = False

    def status_rows(self) -> list[common.Row]:
        nbt = self.nbt
        rows = [common.health_row(nbt)]

        if "Tame" in nbt:
            rows.append(common.Row("\U0001f91d", "Tamed", translate.yes_no(nbt["Tame"])))

        rows.append(common.Row("\U0001fa91", "Saddled", "Yes" if _saddled(nbt) else "No"))

        if "ChestedHorse" in nbt:
            rows.append(
                common.Row("\U0001f4e6", "Has Chest", translate.yes_no(nbt["ChestedHorse"]))
            )

        rows += common.flag_rows(nbt)
        rows.append(common.leash_row(nbt))

        home = nbt.get("home_pos") or nbt.get("HomePos")
        if home:
            rows.append(common.Row("\U0001f3e0", "Home", translate.coords_from_array(home)))

        return [r for r in rows if r]

    def detail_rows(self) -> list[common.Row]:
        rows = []
        if "Temper" in self.nbt:
            rows.append(common.Row("\U0001f321️", "Temper", f"{int(self.nbt['Temper'])}/100"))
        return rows


def _saddled(nbt) -> bool:
    equipment = nbt.get("equipment")
    if isinstance(equipment, dict) and equipment.get("saddle"):
        return True
    if nbt.get("SaddleItem"):
        return True
    return int(nbt.get("Saddle", 0)) != 0
