import io

from mcmobsheet import cli

DONKEY = (
    '/summon minecraft:donkey -548.07 66.00 -522.01 '
    '{Tame: 1b, Health: 16.796165f, CustomName: "Cloppin", ChestedHorse: 1b, '
    'Temper: 65, equipment: {saddle: {count: 1, id: "minecraft:saddle"}}, '
    'attributes: [{id: "minecraft:movement_speed", base: 0.24215288738187263d}, '
    '{id: "minecraft:jump_strength", base: 0.8408389372882603d}, '
    '{id: "minecraft:max_health", base: 16.796165002165434d}], '
    'leash: [I; -551, 66, -523], home_pos: [I; -551, 66, -523]}'
)


def test_argument_mode(capsys):
    rc = cli.main([DONKEY])
    out = capsys.readouterr().out
    assert rc == 0
    assert 'Donkey - "Cloppin"' in out
    assert "Location: -548, 66, -522" in out
    assert "8.4 hearts (16.8)" in out
    assert "~ 3.9 blocks (0.841)" in out


def test_pipe_mode(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("/summon minecraft:creeper 0 64 0 {Health: 20.0f}"))
    monkeypatch.setattr("sys.stdin.isatty", lambda: False, raising=False)
    rc = cli.main([])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Creeper" in out
    assert "10.0 hearts (20.0)" in out


def test_setblock_argument(capsys):
    rc = cli.main(["/setblock -548 66 -522 minecraft:oak_stairs[facing=north,half=top]"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "Oak Stairs facing North, upper half" in out


def test_known_mob_has_no_disclaimer(capsys):
    cli.main([DONKEY])
    out = capsys.readouterr().out
    assert "Best-effort" not in out


def test_unknown_mob_has_disclaimer(capsys):
    cli.main(["/summon minecraft:warden 0 0 0 {Health: 500.0f}"])
    out = capsys.readouterr().out
    assert "Best-effort" in out


def test_bad_command_returns_error(capsys):
    rc = cli.main(["/give @p minecraft:diamond"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "Could not parse" in err
