"""Generic best-effort translator that works for any entity."""

from __future__ import annotations

from typing import Optional

from mcmobsheet import translate
from mcmobsheet.entities import common


class BaseEntityTranslator:
    """Renders an entity using only universally-meaningful tags.

    Subclasses register for specific entity ids and add mob-specific rows.
    `generic` controls whether the best-effort disclaimer is shown.
    """

    generic = True

    def __init__(self, command):
        self.cmd = command
        self.nbt = command.nbt

    def emoji(self) -> str:
        return common.ENTITY_EMOJI.get(self.cmd.entity_id, common.DEFAULT_ENTITY_EMOJI)

    def custom_name(self) -> Optional[str]:
        if "CustomName" in self.nbt:
            return translate.plain_text(self.nbt["CustomName"])
        return None

    def status_rows(self) -> list[common.Row]:
        rows = [common.health_row(self.nbt)]
        rows += common.flag_rows(self.nbt)
        rows.append(common.leash_row(self.nbt))
        return [r for r in rows if r]

    def detail_rows(self) -> list[common.Row]:
        return []

    def sections(self):
        result = []
        for title, rows in (
            ("Status", self.status_rows()),
            ("Attributes", common.attribute_rows(self.nbt)),
            ("Effects", common.effect_rows(self.nbt)),
            ("Details", self.detail_rows()),
        ):
            if rows:
                result.append((title, rows))
        return result
