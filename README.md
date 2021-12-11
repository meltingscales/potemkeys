# FGfGwK: Fighting Games for Goldfish with Keyboards

[![forthebadge](https://forthebadge.com/images/badges/you-didnt-ask-for-this.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/built-with-swag.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)

[![forthebadge](https://forthebadge.com/images/badges/compatibility-club-penguin.svg)](https://forthebadge.com)

![A picture of the application.](/window.png)

## What is this?

For those who can't remember {keyboard input => controller} mappings, and want to see them in-game.

Created because TEKKEN doesn't show input conversions in multiplayer matches, and neither does Guilty Gear: Strive, and I wanted to see my inputs, so I wasted 6 hours writing this tool.

Works on Windows 11, and tested on Ubuntu.

## How do I use it?

See <https://github.com/HenryFBP/FGfGwK/releases> and download the provided exe/binary file.

##  Development

1.  Install Python version 3.whatever
2.  Clone this repo
3.  In the repo's folder, run:

    ```
    ./scripts/setup[.cmd|.sh]
    pipenv run python FGfFwK.py
    ```

    Or, just run `./scripts/start.cmd` or `./scripts/start.sh`.

4.  The window should stay on top.

    ***Play your game in borderless/windowed mode*** and see the inputs get transformed and shown to you.

## Config

Edit [`options.jsonc`](/options.jsonc).

You can make keymaps for literally any game that uses keyboard, by cloning the items under `keymaps`.

If you make one and want to see it included in the "official" branch of this tool, just fork this repo and make a PR.

## License

No license, DWYW, I'm not your dad.

Just make sure to link/PR, or just fork it if I die or something :P
