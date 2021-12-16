#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position

import urllib.request
from typing import List

import json5
import pynput
from pygame.locals import *
from pynput.keyboard import Key, Listener, KeyCode

import Config
from GlobalState import GlobalState
from Utils import *


def is_modifier_key(k: Key):
    try:
        _ = k.char
        return False
    except AttributeError:
        return True


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


class KeyEvent:
    def __init__(self) -> None:
        raise Exception("lol todo :p")


def prompt_choose_keymap(state) -> None:
    """Returns true if a user picks a keymap successfully."""
    print("Keymap is not chosen yet! Asking them to choose...")

    state.add_message("[{:^10s}] Choose a keymap:".format(str(state.get_key())))
    all_keymap_names = list(state.get_all_keymaps().keys())

    i = 0
    for keymapname in all_keymap_names:
        state.add_message("[{}]: {}".format(i, keymapname), i + 1)
        i += 1

    if not is_modifier_key(state.get_key()):
        try:
            user_wants_n = int(state.get_key().char)

            if (user_wants_n >= 0) and (user_wants_n <= len(all_keymap_names)):
                # they select n
                chosen_keymap_name = all_keymap_names[user_wants_n]
                state.choose_keymap(chosen_keymap_name)

                # clear other message logs
                state.blank_message_log()

                mi = 4

                state.add_message("Current keymap:  {}".format(
                    chosen_keymap_name
                ), mi)
                mi += 1

                state.add_message("Valid keys:      {}".format(
                    ','.join(state.current_keymap_mapped_keys())
                ), mi)
                mi += 1

                state.add_message("Valid chords:    {}".format(
                    ','.join(state.current_keymap_mapped_chords())
                ), mi)
                mi += 1

                state.add_message("Valid combos:    {}".format(
                    ','.join(state.current_keymap_mapped_combinations())
                ), mi)
                mi += 1

                # clear the key log, they've chosen
                state.clear_key_log()

                return

        except ValueError:
            pass

    # not successful
    return


def process_mashing(state: GlobalState) -> str:
    """Return a status string if mashing is detected."""
    if state.key_log_length() >= 2:
        # if they've pressed at least 2 keys

        prev_key = state.get_key(-2)

        if prev_key == state.get_key():
            # they mashin', show it
            state.repeats += 1
            return f' (x{state.repeats})'
        else:
            # not mashin', reset
            state.repeats = 1

    return ""


def process_key_press(state: GlobalState, msg: str = "") -> str:
    if not is_modifier_key(state.get_key()):
        key_char = state.get_key().char
        normalized_key_char = key_char.upper()

        print('alphanumeric key {0} pressed'.format(key_char))
        msg += "{}".format(key_char)

        if normalized_key_char in GLOBAL_STATE.current_keymap_mapped_keys():
            msg += ' = {:2s}'.format(
                GLOBAL_STATE.current_keymap_keys_map()[normalized_key_char])
        else:
            msg += ' = ?'

        # print("pressed {} keys".format(state.total_keys_pressed()))

        msg += process_mashing(state)

    else:
        print('special key {0} pressed'.format(state.get_key()))

    return msg


def process_key_chords(state: GlobalState) -> List[List[KeyCode]]:
    results: List[List[KeyCode]] = []

    # for all chords patterns,
    for chord_str in state.current_keymap_chords_map():

        splitchord: List[str] = chord_str.split(' ')
        splitchord = [s.upper() for s in splitchord]

        chordlen = len(splitchord)

        # too short
        if chordlen > state.key_log_length():
            break  # on to next chord

        key_log_slice = []

        for i in range(state.key_log_length() - 1, -1, -1):
            key_log_slice.append(state.get_key(i))
            # print("i={},key={}".format(i, key_log_slice[-1]))
            if len(key_log_slice) >= chordlen:
                break

        key_log_slice.reverse()

        # print("Looking for {} aka {}".format(chord_str,splitchord))
        # print("Inside of {}".format(key_log_slice))

        matching_keys: List[Key] = []
        # for all keys in the chord,
        for i in range(0, len(splitchord)):
            # print('i=           {}'.format(i))

            currentKey = key_log_slice[i]
            current_chord_member = splitchord[i]
            currentKeyCharCode: str = None
            if not is_modifier_key(currentKey):
                currentKeyCharCode = currentKey.char.upper()
            else:
                break  # on to next chord... TODO, NYI for modifiers...
            # print('looking for {}'.format(i))
            #
            # print('current_chord_member={}'.format(current_chord_member))
            # print('current_key_pressed= {}'.format(currentKeyCharCode))

            if not (current_chord_member.upper() == currentKeyCharCode.upper()):
                break  # on to next chord... Not a full chord
            else:
                matching_keys.append(currentKey)

            if i == (len(splitchord) - 1):
                # if we're at the end of the chord,

                results.append(matching_keys)
                break  # not necessary but more readable

    # print("Returning {}".format(results))
    return results


def format_chord_results(state: GlobalState, chordResults: List[List[KeyCode]]) -> str:
    chordmsg = ""

    for i in range(0, len(chordResults)):
        chordResult: List[KeyCode] = chordResults[i]
        keycode: KeyCode

        for j in range(0, len(chordResult)):
            keycode = chordResult[j]
            chordmsg += keycode.char

            if j < (len(chordResult) - 1):
                chordmsg += "-"

        chordmsg += " [{0}]".format(state.chordResult_to_message(chordResult))

        if i < (len(chordResults) - 1):
            chordmsg += ','

    return chordmsg


def process_key_combos(state: GlobalState):
    pass


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


def should_quit(key, state):
    try:
        if key == Key.__getitem__(state.quit_key):  # TODO is this a security risk? __getitem__ with user input?
            return True
    except KeyError:  # Means no key called state.quit_key exists...
        print("WARN:    quit_key '{}' is invalid".format(state.quit_key))

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
