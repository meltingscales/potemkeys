# FGfGwK: Fighting Games for Goldfish with Keyboards

![A picture of the application.](/window.png)

## What is this?

For those who can't remember {keyboard input => controller} mappings, and want to see them in-game.

## How do I use it?

You must use Windows currently. 

When I'm less lazy (never) I will make X11 equivalents for the win32 API code I use to make the window stay on top.

1.  Install Python version 3.whatever
2.  Clone this repo
3.  In the repo's folder, run:

    ```
    python -m pip install pipenv
    pipenv install
    pipenv run python main.py
    ```

    Or, just run `start.cmd`.

4.  The window should stay on top.

    Play your game in borderless mode and see the inputs get transformed and shown to you.

## Config

Edit [`options.jsonc`](/options.jsonc).

You can make keymaps for literally any game that uses keyboard, by cloning the items under `keymaps`.

If you make one and want to see it included in the "official" branch of this tool, just fork this repo and make a PR.

## License

No license, DWYW, I'm not your dad.

Just make sure to link/PR, or just fork it if I die or something :P
