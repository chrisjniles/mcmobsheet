from mcmobsheet.blocks import common as blocks


def test_describe_stairs():
    states = {"facing": "north", "half": "top"}
    assert blocks.describe(states) == "facing North, upper half"


def test_describe_bottom_half():
    assert blocks.describe({"half": "bottom"}) == "lower half"


def test_describe_includes_true_flags_only():
    states = {"waterlogged": "true", "powered": "false"}
    assert blocks.describe(states) == "waterlogged"


def test_describe_empty():
    assert blocks.describe({}) is None


def test_state_rows_hides_false_booleans():
    rows = blocks.state_rows({"facing": "north", "waterlogged": "false"})
    labels = [r.label for r in rows]
    assert "Facing" in labels
    assert "Waterlogged" not in labels


def test_state_rows_shows_true_booleans_as_yes():
    rows = blocks.state_rows({"lit": "true"})
    assert rows[0].label == "Lit"
    assert rows[0].value == "Yes"


def test_emoji_default():
    assert blocks.emoji_for("minecraft:unknown_block") == blocks.DEFAULT_BLOCK_EMOJI
