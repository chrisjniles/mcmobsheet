from mcmobsheet.parser import parse_command
from mcmobsheet.types import SetblockCommand, SummonCommand


def test_parse_summon_basic():
    cmd = parse_command("/summon minecraft:donkey -548.07 66.00 -522.01 {Health: 16.8f}")
    assert isinstance(cmd, SummonCommand)
    assert cmd.entity_id == "minecraft:donkey"
    assert cmd.entity_name == "Donkey"
    assert (round(cmd.x), round(cmd.y), round(cmd.z)) == (-548, 66, -522)
    assert float(cmd.nbt["Health"]) == 16.8


def test_parse_summon_without_nbt():
    cmd = parse_command("/summon minecraft:cow 1 2 3")
    assert cmd.nbt == {}


def test_parse_summon_without_coords():
    cmd = parse_command("/summon minecraft:cow")
    assert (cmd.x, cmd.y, cmd.z) == (0.0, 0.0, 0.0)


def test_leading_slash_optional():
    assert parse_command("summon minecraft:pig 0 0 0").entity_id == "minecraft:pig"


def test_unqualified_id_gets_namespace():
    assert parse_command("/summon pig 0 0 0").entity_id == "minecraft:pig"


def test_relative_coords_tolerated():
    cmd = parse_command("/summon minecraft:pig ~ ~ ~")
    assert (cmd.x, cmd.y, cmd.z) == (0.0, 0.0, 0.0)


def test_parse_setblock_with_states():
    cmd = parse_command("/setblock -548 66 -522 minecraft:oak_stairs[facing=north,half=top]")
    assert isinstance(cmd, SetblockCommand)
    assert cmd.block_id == "minecraft:oak_stairs"
    assert cmd.block_name == "Oak Stairs"
    assert (cmd.x, cmd.y, cmd.z) == (-548, 66, -522)
    assert cmd.states == {"facing": "north", "half": "top"}


def test_parse_setblock_without_states():
    cmd = parse_command("/setblock 0 0 0 minecraft:stone")
    assert cmd.states == {}


def test_malformed_nbt_does_not_raise():
    cmd = parse_command("/summon minecraft:pig 0 0 0 {this is not valid")
    assert cmd.nbt == {}


def test_unsupported_command_raises():
    try:
        parse_command("/give @p minecraft:diamond")
    except ValueError:
        return
    raise AssertionError("expected ValueError for unsupported command")
