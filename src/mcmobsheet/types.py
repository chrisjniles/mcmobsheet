from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SummonCommand:
    entity_id: str
    entity_name: str
    x: float
    y: float
    z: float
    nbt: dict = field(default_factory=dict)


@dataclass
class SetblockCommand:
    block_id: str
    block_name: str
    x: int
    y: int
    z: int
    states: dict[str, str] = field(default_factory=dict)
    nbt: dict = field(default_factory=dict)
