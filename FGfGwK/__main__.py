import os
import sys
import urllib

import json5
import pygame
import pynput
from pygame.constants import QUIT
from pynput.keyboard import Listener

from FGfGwK import Config
from FGfGwK.FGfGwK import process_key_combos, format_chord_results, process_key_chords, \
    process_key_press, prompt_choose_keymap, should_quit
from FGfGwK.GlobalState import GlobalState
from FGfGwK.Utils import resource_path, window_always_on_top_x11, window_always_on_top_win32, is_windows

OPTIONS_FILE = resource_path(Config.OPTIONS_FILE_NAME, prefer_adjacent_dir=True)

if not os.path.exists(OPTIONS_FILE):
    # Try within the EXE if it doesn't exist outside...
    OPTIONS_FILE = resource_path(
        Config.OPTIONS_FILE_NAME,
        prefer_adjacent_dir=False)

if not os.path.exists(OPTIONS_FILE):
    print("You don't have an options file. Downloading from '{}' into '{}'.".format(
        Config.CONFIG_URL, OPTIONS_FILE
    ))
    urllib.request.urlretrieve(Config.CONFIG_URL, OPTIONS_FILE)

    if not os.path.exists(OPTIONS_FILE):
        message = "Failed to automatically download options file...\n" \
                  "Please download it at {} and then place it in the same directory as the executable.\n > ".format(
            Config.CONFIG_URL)
        input(message)
        raise FileNotFoundError(message)

    print("Downloaded successfully.")

global GLOBAL_STATE

with open(OPTIONS_FILE, encoding='utf-8') as fh:
    jsonobj = json5.load(fh)
    # lol yes we are doing this shitty fucking programming practice     >:3c global state!
    # noinspection PyUnresolvedReferences,PyRedeclaration
    GLOBAL_STATE = GlobalState(options=jsonobj)

GLOBAL_STATE.enforce_linux_x11_dependencies()


# TODO: How long is this method taking? Probably CPU intensive...
#   We should come up with a parser for keypresses to avoid all these for loops.
def on_press(_key: pynput.keyboard.Key, state: GlobalState = GLOBAL_STATE):
    state.press_key(_key)

    # halt if they haven't chosen a keymap
    if not state.keymap_is_chosen:
        prompt_choose_keymap(state)
        return True

    msg = process_key_press(state)
    state.add_message(msg, 0)

    # handle chords
    matching_chords = process_key_chords(state)

    chordmsg = format_chord_results(state, matching_chords)

    if chordmsg:
        state.add_message("Chord: " + chordmsg, 1)
    else:  # blank if no chord
        state.add_message("", 1)

    # TODO handle key combos
    matching_key_combos = process_key_combos(state)


# noinspection PyUnusedLocal
def on_release(key, state=GLOBAL_STATE):
    state.release_key(key)
    print('{0} released'.format(key))
    if should_quit(key, state):
        # Stop listener
        print("We want to quit!")
        GLOBAL_STATE.running = False
        return False


if __name__ == '__main__':

    # using .start() is non blocking
    keylistener = Listener(on_press=on_press, on_release=on_release)
    keylistener.start()

    window_width, window_height = GLOBAL_STATE.optionsJson['window_width'], GLOBAL_STATE.optionsJson['window_height']
    screen_width, screen_height = GLOBAL_STATE.optionsJson['screen_width'], GLOBAL_STATE.optionsJson['screen_height']

    pygame.init()

    if os.path.exists(GLOBAL_STATE.icon_path):
        pygame_icon = pygame.image.load(GLOBAL_STATE.icon_path)
        pygame.display.set_icon(pygame_icon)

    FONT = pygame.font.SysFont(GLOBAL_STATE.optionsJson['font_type'], GLOBAL_STATE.optionsJson['font_size'])
    DISPLAYSURFACE = pygame.display.set_mode(
        (window_width, window_height), pygame.RESIZABLE
    )
    pygame.display.set_caption(GLOBAL_STATE.title)

    # make on top
    if GLOBAL_STATE.optionsJson['window_always_on_top']:
        if is_windows():
            window_always_on_top_win32(
                pygame,
                x=int((screen_width / 2) - (window_width / 2)),
                y=int((screen_height / 2) - (window_height / 2))
            )
        else:
            window_always_on_top_x11()

    # main game loop
    while GLOBAL_STATE.running:
        window_width, window_height = DISPLAYSURFACE.get_size()

        # set bg color
        DISPLAYSURFACE.fill(GLOBAL_STATE.optionsJson['background_color'])

        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # for all message logs,
        for i in range(0, len(GLOBAL_STATE.message_array_log)):
            messageLog = GLOBAL_STATE.message_array_log[i]

            text = FONT.render(
                messageLog[-1], True, GLOBAL_STATE.optionsJson['text_color'],
                GLOBAL_STATE.optionsJson['background_color'])
            textRect = text.get_rect()

            if GLOBAL_STATE.optionsJson['center_text']:  # TODO Why is this not centered perfectly? idk lol
                textRect.center = (window_width // 2, 0)

            # move it down
            textRect.y += (i * (FONT.get_linesize() + GLOBAL_STATE.optionsJson['font_margin']))

            DISPLAYSURFACE.blit(text, textRect)

        pygame.display.update()
