import pytest

from mcmobsheet import snbt


def test_empty_compound():
    assert snbt.parse("{}") == {}


def test_typed_scalars_decay_to_plain_numbers():
    result = snbt.parse("{a: 1b, b: 2s, c: 3L, d: 4.5f, e: 6.5d, f: 7}")
    assert result == {"a": 1, "b": 2, "c": 3, "d": 4.5, "e": 6.5, "f": 7}
    assert isinstance(result["d"], float)
    assert isinstance(result["f"], int)


def test_booleans():
    assert snbt.parse("{on: true, off: false}") == {"on": 1, "off": 0}


def test_negative_and_exponent_numbers():
    result = snbt.parse("{m: -0.0784000015258789d, big: 1.6e3f}")
    assert result["m"] == pytest.approx(-0.0784000015258789)
    assert result["big"] == pytest.approx(1600.0)


def test_quoted_strings_and_unquoted_values():
    result = snbt.parse('{name: "Cloppin", id: bare_value}')
    assert result == {"name": "Cloppin", "id": "bare_value"}


def test_escaped_quotes_inside_string():
    # A double-quoted JSON text component with escaped inner quotes.
    result = snbt.parse('{CustomName: "{\\"text\\":\\"Big Guy\\"}"}')
    assert result["CustomName"] == '{"text":"Big Guy"}'


def test_single_quoted_string():
    assert snbt.parse("{t: '{\"text\":\"Hi\"}'}")["t"] == '{"text":"Hi"}'


def test_int_array():
    assert snbt.parse("{leash: [I; -551, 66, -523]}") == {"leash": [-551, 66, -523]}


def test_byte_and_long_arrays():
    assert snbt.parse("{b: [B; 1b, 2b], l: [L; 10L, 20L]}") == {"b": [1, 2], "l": [10, 20]}


def test_empty_list_and_array():
    assert snbt.parse("{items: [], arr: [I;]}") == {"items": [], "arr": []}


def test_nested_compounds_and_lists():
    result = snbt.parse(
        '{equipment: {saddle: {count: 1, id: "minecraft:saddle"}}, '
        'attributes: [{id: "minecraft:max_health", base: 16.8d}]}'
    )
    assert result["equipment"]["saddle"]["id"] == "minecraft:saddle"
    assert result["attributes"][0]["base"] == pytest.approx(16.8)


def test_float_list():
    assert snbt.parse("{Rotation: [183.2f, 0.0f]}")["Rotation"] == pytest.approx([183.2, 0.0])


def test_whitespace_tolerated():
    assert snbt.parse("{  a : 1 , b : 2  }") == {"a": 1, "b": 2}


def test_malformed_raises():
    with pytest.raises(snbt.SNBTError):
        snbt.parse("{a: 1")


def test_trailing_data_raises():
    with pytest.raises(snbt.SNBTError):
        snbt.parse("{} garbage")


def test_parses_full_donkey_blob():
    blob = (
        "{AgeLocked: 0b, Tame: 1b, Owner: [I; -635843156, -2117054767, -1335964012, "
        "-2090256205], Health: 16.796165f, equipment: {saddle: {count: 1, id: "
        '"minecraft:saddle"}}, CustomName: "Cloppin", ChestedHorse: 1b, Temper: 65, '
        'attributes: [{id: "minecraft:movement_speed", base: 0.24215288738187263d}], '
        "leash: [I; -551, 66, -523], Motion: [0.0d, -0.0784000015258789d, 0.0d]}"
    )
    result = snbt.parse(blob)
    assert result["Tame"] == 1
    assert result["CustomName"] == "Cloppin"
    assert result["Owner"] == [-635843156, -2117054767, -1335964012, -2090256205]
    assert result["equipment"]["saddle"]["count"] == 1
    assert result["attributes"][0]["base"] == pytest.approx(0.24215288738187263)
    assert result["leash"] == [-551, 66, -523]
