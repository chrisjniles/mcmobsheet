"""Entity translator registry.

Translators register for one or more entity ids via the @register decorator.
get_translator() returns an instance for a parsed command, falling back to the
generic BaseEntityTranslator for unrecognized entities.
"""

from __future__ import annotations

REGISTRY: dict[str, type] = {}


def register(*entity_ids: str):
    def wrap(cls):
        for entity_id in entity_ids:
            REGISTRY[entity_id] = cls
        return cls

    return wrap


from mcmobsheet.entities.base import BaseEntityTranslator  # noqa: E402


def get_translator(command):
    cls = REGISTRY.get(command.entity_id, BaseEntityTranslator)
    return cls(command)


# Import concrete translators so their @register decorators run.
from mcmobsheet.entities import horse  # noqa: E402,F401
