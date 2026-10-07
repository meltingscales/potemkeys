# potemkeys

On-screen keyboard-to-controller button map for fighting games, for goldfish who can't
remember which key is Heavy Slash. Stays on top of your (borderless/windowed) game and shows:

- the key you just pressed and what it maps to, plus a strip of your recent inputs
- chords (`A A` = dash), combinations (hold `S`, press `K` = `2H`) and macros
- a cheat sheet of the whole keymap, with held keys lit up

![Playing](/media/screenshot1.png)

![Keymap menu](/media/screenshot2.png)

Name: Potemkin (Guilty Gear) + keys. Formerly "FGfGwK: Fighting Games for Goldfish with Keyboards".

## Download

- [Windows](https://github.com/HenryFBP/potemkeys/releases/download/latest-windows/potemkeys.exe)
- [Linux](https://github.com/HenryFBP/potemkeys/releases/download/latest-ubuntu/potemkeys)
- [macOS](https://github.com/HenryFBP/potemkeys/releases/download/latest-macos/potemkeys)
- PyPI: `pip install --upgrade potemkeys` then `potemkeys` (or `python -m potemkeys`)

All builds: <https://github.com/HenryFBP/potemkeys/releases>

## Usage

1. Run it. Pick a keymap by pressing its number/letter.
2. Play your game in borderless or windowed mode. The window stays on top.
3. `F1` goes back to the keymap menu, `ESC` quits (both configurable).

```
potemkeys --keymap "GG:S Default"   # skip the menu
potemkeys --list-keymaps
potemkeys --config path/to/potemkeysoptions.jsonc
```

Linux note: on Wayland sessions neither SDL nor anything else can force always-on-top; run under
XWayland or pin the window from your compositor.

## Config

Everything lives in [`potemkeysoptions.jsonc`](/potemkeys/potemkeysoptions.jsonc) (JSON5, comments allowed).
The app looks for it in the current directory, then next to the executable, then falls back to the bundled copy.
Drop a copy next to the `.exe` to customize.

A keymap:

```jsonc
"GG:S Default": {
  "keys": {
    "A": "[←]   Left",
    "K": "[HS]  HSlash",          // "[notation] (modifier) description [category]"
  },
  "chords": { "A A": "dash" },                       // taps in sequence, within chord_window_ms
  "combinations": { "S-K": "[2H] Crouching HS" },    // hold S, press K
  "macros": [
    { "Buster": { "inputs": "A 0.1 A S+J", "trigger": "ALT D" } }  // keys, delays in seconds, S+J together
  ]
},
"My GG:S": { "inherit": "GG:S Default", "keys": { "E": "[RC] Roman Cancel" } }
```

Key names are single characters (`A`, `;`) or pynput key names in caps (`CTRL`, `ALT`, `F1`, `SPACE`).
Made a keymap for another game? Open a PR.

## Development

```
./scripts/setup.sh      # installs uv, syncs deps   (setup.cmd on Windows)
just run                # or: uv run python -m potemkeys
just test
just exe                # PyInstaller build into dist/
uv build && uv publish  # PyPI
```

Code layout: `keymap.py` (keymap model + matching), `engine.py` (input state, display lines),
`keys.py` (pynput adapter + macro playback), `app.py` (pygame window), `config.py` (options file).
Everything except `keys.py`/`app.py` is pure Python and unit tested.

## License

No license, DWYW, I'm not your dad.
