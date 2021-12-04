# FGfGwK: Fighting Games for Goldfish with Keyboards

## What is this?

For those who can't remember {keyboard input => controller} mappings, and want to see them in-game.

## How do I use it?

You must use Windows currently. When I'm less lazy (never) I will make X11 equivalents for the win32 API code I use to make the window stay on top.

1.  Install Python
2.  Clone this repo
3.  Run:

    ```
    pipenv install
    pipenv shell
    python main.py
    ```
4.  The window should stay on top. Play your game in borderless mode and see the inputs get transformed and shown to you.