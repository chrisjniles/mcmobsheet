# mcmobsheet

A CLI tool that turns Minecraft Java Edition `/summon` and `/setblock` data into
clean, human-readable stat sheets.

In-game, press **"F3 + I"** while targeting a mob or block to copy its full data to
your clipboard. Paste that into `mcmobsheet` and it translates the raw NBT into
something you can actually read - health in hearts, jump strength in blocks,
attributes in real units, and only the details that matter.

```
Donkey - "Cloppin"
Location: -548, 66, -522

-- Status --------------------------------
  Health:        8.4 hearts (16.8)
  Tamed:         Yes
  Saddled:       Yes
  Has Chest:     Yes
  Won't Despawn: Yes
  Leashed at:    -551, 66, -523
  Home:          -551, 66, -523

-- Attributes ----------------------------
  Move Speed:  ~ 10.5 blocks/sec (0.242)
  Jump Height: ~ 3.9 blocks (0.841)
  Max Health:  8.4 hearts (16.8)

-- Details -------------------------------
  Temper: 65/100
```

## Install

### Homebrew

```sh
brew install chrisjniles/tap/mcmobsheet
```

### From source

```sh
git clone https://github.com/chrisjniles/mcmobsheet
cd mcmobsheet
pip install .
```

Requires Python 3.10+.

## Usage

### Interactive mode (default)

Run `mcmobsheet` with no arguments to start an interactive prompt. Paste a command
copied with **F3 + I** and press Enter. Type `quit` or press Ctrl+D to exit.

```sh
$ mcmobsheet
mcmobsheet - paste a /summon or /setblock command (from F3+I) and press Enter.
Type 'quit' or press Ctrl+D to exit.

mcmobsheet> /summon minecraft:donkey -548.07 66.00 -522.01 {Tame: 1b, ...}
```

### Other input modes

You can also pass a command directly as an argument:

```sh
mcmobsheet '/summon minecraft:donkey -548.07 66.00 -522.01 {Tame: 1b, ...}'
```

...or pipe it in from your clipboard:

```sh
pbpaste | mcmobsheet
```

## What it understands

- **Any entity** - best-effort stats (health, attributes, status effects, common
  flags) for every mob, with a note when there's no dedicated translator yet. Every
  mob in current Minecraft (Java 26.2) renders at least a minimal sheet.
- **Horse family** - donkeys, horses, mules, and skeleton/zombie horses get
  tailored output: taming, saddle, chest, temper, jump height, and more.
- **Blocks** - `/setblock` commands with block states like
  `oak_stairs[facing=north,half=top]` render as `Oak Stairs facing North, upper half`.

Values are shown translated with the raw value in parentheses, e.g.
`8.4 hearts (16.8)`. Engine-internal and default/zero data is hidden so you only
see what's interesting.

## Missing your favorite mob?

The generic translator covers any entity, but mob-specific details (variants,
trades, inventories, and so on) need dedicated support. If something you care about
isn't shown, [open an issue](https://github.com/chrisjniles/mcmobsheet/issues) and
include the `/summon` text you copied.

## Development

```sh
pip install -e .
pip install pytest
pytest
```

## License

mcmobsheet is free software, licensed under the
[GNU General Public License v3.0](LICENSE) or later.

Copyright (C) 2026 Chris Niles

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.
