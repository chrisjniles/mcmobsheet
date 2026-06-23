"""Guards that every mob in current Minecraft renders at least a minimal fact sheet.

CURRENT_MOBS is the full living-mob roster for Minecraft Java 26.2 ("Chaos Cubed",
June 2026), derived from the PrismarineJS minecraft-data 1.21.11 registry plus the
sole 26.2 addition (sulfur_cube). When a new version adds mobs, extend this list.
"""

import pytest

from mcmobsheet.display import render_summon
from mcmobsheet.types import SummonCommand

CURRENT_MOBS = [
    'minecraft:allay', 'minecraft:armadillo', 'minecraft:axolotl', 'minecraft:bat',
    'minecraft:bee', 'minecraft:blaze', 'minecraft:bogged', 'minecraft:breeze',
    'minecraft:camel', 'minecraft:camel_husk', 'minecraft:cat', 'minecraft:cave_spider',
    'minecraft:chicken', 'minecraft:cod', 'minecraft:copper_golem', 'minecraft:cow',
    'minecraft:creaking', 'minecraft:creeper', 'minecraft:dolphin', 'minecraft:donkey',
    'minecraft:drowned', 'minecraft:elder_guardian', 'minecraft:ender_dragon',
    'minecraft:enderman', 'minecraft:endermite', 'minecraft:evoker', 'minecraft:fox',
    'minecraft:frog', 'minecraft:ghast', 'minecraft:giant', 'minecraft:glow_squid',
    'minecraft:goat', 'minecraft:guardian', 'minecraft:happy_ghast', 'minecraft:hoglin',
    'minecraft:horse', 'minecraft:husk', 'minecraft:illusioner', 'minecraft:iron_golem',
    'minecraft:llama', 'minecraft:magma_cube', 'minecraft:mooshroom', 'minecraft:mule',
    'minecraft:nautilus', 'minecraft:ocelot', 'minecraft:panda', 'minecraft:parched',
    'minecraft:parrot', 'minecraft:phantom', 'minecraft:pig', 'minecraft:piglin',
    'minecraft:piglin_brute', 'minecraft:pillager', 'minecraft:polar_bear',
    'minecraft:pufferfish', 'minecraft:rabbit', 'minecraft:ravager', 'minecraft:salmon',
    'minecraft:sheep', 'minecraft:shulker', 'minecraft:silverfish', 'minecraft:skeleton',
    'minecraft:skeleton_horse', 'minecraft:slime', 'minecraft:sniffer',
    'minecraft:snow_golem', 'minecraft:spider', 'minecraft:squid', 'minecraft:stray',
    'minecraft:strider', 'minecraft:sulfur_cube', 'minecraft:tadpole',
    'minecraft:trader_llama', 'minecraft:tropical_fish', 'minecraft:turtle',
    'minecraft:vex', 'minecraft:villager', 'minecraft:vindicator',
    'minecraft:wandering_trader', 'minecraft:warden', 'minecraft:witch',
    'minecraft:wither', 'minecraft:wither_skeleton', 'minecraft:wolf', 'minecraft:zoglin',
    'minecraft:zombie', 'minecraft:zombie_horse', 'minecraft:zombie_nautilus',
    'minecraft:zombie_villager', 'minecraft:zombified_piglin',
]


def test_roster_has_no_duplicates():
    assert len(CURRENT_MOBS) == len(set(CURRENT_MOBS))


@pytest.mark.parametrize("entity_id", CURRENT_MOBS)
def test_each_mob_renders_minimal_sheet(entity_id):
    name = entity_id.split(":", 1)[1].replace("_", " ").title()
    cmd = SummonCommand(
        entity_id=entity_id, entity_name=name, x=1.4, y=64.0, z=-2.6, nbt={}
    )
    output = render_summon(cmd)
    first_line = output.splitlines()[0]
    # Title is the readable name; minimal sheet always carries a rounded location.
    assert first_line == name
    assert "Location: 1, 64, -3" in output
