from mcmobsheet.entities import get_translator
from mcmobsheet.entities.base import BaseEntityTranslator
from mcmobsheet.entities.horse import HorseTranslator
from mcmobsheet.parser import parse_command


def _translator(command_text):
    return get_translator(parse_command(command_text))


def test_donkey_uses_horse_translator():
    t = _translator("/summon minecraft:donkey 0 0 0 {Health: 16.0f}")
    assert isinstance(t, HorseTranslator)
    assert t.generic is False


def test_unknown_entity_uses_base_translator():
    t = _translator("/summon minecraft:warden 0 0 0 {Health: 500.0f}")
    assert type(t) is BaseEntityTranslator
    assert t.generic is True


def test_custom_name_plain():
    t = _translator('/summon minecraft:donkey 0 0 0 {CustomName: "Cloppin"}')
    assert t.custom_name() == "Cloppin"


def test_horse_status_includes_expected_rows():
    t = _translator(
        "/summon minecraft:donkey 0 0 0 "
        '{Health: 16.8f, Tame: 1b, ChestedHorse: 1b, Temper: 65, '
        'equipment: {saddle: {count: 1, id: "minecraft:saddle"}}, '
        "home_pos: [I; -551, 66, -523], leash: [I; -551, 66, -523]}"
    )
    sections = dict(t.sections())
    status_labels = [row.label for row in sections["Status"]]
    assert status_labels == ["Health", "Tamed", "Saddled", "Has Chest", "Leashed at", "Home"]
    assert dict((r.label, r.value) for r in sections["Status"])["Saddled"] == "Yes"


def test_horse_temper_in_details():
    t = _translator("/summon minecraft:donkey 0 0 0 {Temper: 65}")
    details = dict(t.sections())["Details"]
    assert details[0].label == "Temper"
    assert details[0].value == "65/100"


def test_attributes_section():
    t = _translator(
        "/summon minecraft:donkey 0 0 0 "
        '{attributes: [{id: "minecraft:movement_speed", base: 0.242d}, '
        '{id: "minecraft:jump_strength", base: 0.841d}, '
        '{id: "minecraft:max_health", base: 16.8d}]}'
    )
    attrs = dict(t.sections())["Attributes"]
    labels = [row.label for row in attrs]
    assert labels == ["Move Speed", "Jump Height", "Max Health"]


def test_unsaddled_horse_shows_no():
    t = _translator("/summon minecraft:horse 0 0 0 {Health: 30.0f, Tame: 0b}")
    status = dict(t.sections())["Status"]
    saddled = dict((r.label, r.value) for r in status)["Saddled"]
    assert saddled == "No"
