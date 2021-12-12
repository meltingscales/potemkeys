# FGfGwK: Fighting Games for Goldfish with Keyboards

[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/compatibility-club-penguin.svg)](https://forthebadge.com)

![A picture of the application.](/media/screenshot1.png)

![Another picture of the application.](/media/screenshot2.png)

## What is this?

For those who can't remember {keyboard input => controller} mappings, and want to see them in-game.

Created because TEKKEN doesn't show input conversions in multiplayer matches, and neither does Guilty Gear: Strive, 
and I wanted to see my inputs, so I wasted 6 hours writing this tool.

Works on Windows 11, and tested on Ubuntu.

## This tool sucks, it doesn't do X!

See [./TODO.md](./TODO.md). Or fork this repo and add it yourself, and make a Pull Request, I'll probably accept your changes.

## How do I use it?

See <https://github.com/HenryFBP/FGfGwK/releases> and download the provided exe/binary file.
 
If you put `FGfGwKoptions.jsonc` in the same folder as the EXE file, it will prefer that over its temporary directory.

If you want to know where the temp file is, look at the console output when the .exe first starts up.

##  Development

1.  Install Python version 3.whatever
2.  Clone this repo
3.  In the repo's folder, run:

    ```
    ./scripts/setup[.cmd|.sh]
    ./scripts/start[.cmd|.sh]
    ```

4.  The window should stay on top.

    ***Play your game in borderless/windowed mode*** and see the inputs get transformed and shown to you.

### Testing exe generation

    ./scripts/generate_exe[.cmd|.sh]
    ./dist/FGfGwK[.exe|.app]

## Config

Edit [`FGfGwKoptions.jsonc`](/FGfGwKoptions.jsonc).

You can make keymaps for literally any game that uses keyboard, by cloning the items under `keymaps`.

If you make one and want to see it included in the "official" branch of this tool, just fork this repo and make a PR.

## License

No license, DWYW, I'm not your dad.

Just make sure to link/PR, or just fork it if I die or something :P

## VIRUSES????

https://www.reddit.com/r/learnpython/comments/e99bhe/why_does_pyinstaller_trigger_windows_defender

### REEEEEEEEEEEEEEE

https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/ms537361(v=vs.85)?redirectedfrom=MSDN
