from mcmobsheet import translate


def test_hearts():
    assert translate.hearts(16.796165) == "8.4 hearts (16.8)"


def test_hearts_full_value():
    assert translate.hearts(20.0) == "10.0 hearts (20.0)"


def test_speed_blocks_per_sec():
    assert translate.speed_blocks_per_sec(0.24215288738187263) == "~ 10.5 blocks/sec (0.242)"


def test_jump_blocks():
    # 0.841 jump_strength clears a bit under 4 blocks.
    assert translate.jump_blocks(0.8408389372882603) == "~ 3.9 blocks (0.841)"


def test_yes_no():
    assert translate.yes_no(1) == "Yes"
    assert translate.yes_no(0) == "No"


def test_coords_rounds():
    assert translate.coords(-548.07, 66.00, -522.51) == "-548, 66, -523"


def test_coords_from_array():
    assert translate.coords_from_array([-551, 66, -523]) == "-551, 66, -523"


def test_plain_text_bare_string():
    assert translate.plain_text("Cloppin") == "Cloppin"


def test_plain_text_json_component():
    assert translate.plain_text('{"text":"Big Guy"}') == "Big Guy"


def test_plain_text_json_with_extra():
    component = '{"text":"Hello ","extra":[{"text":"World"}]}'
    assert translate.plain_text(component) == "Hello World"
