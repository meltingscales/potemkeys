#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position

import os
import subprocess
import sys
import urllib.request
from shutil import which
from typing import List, Set, Dict

import json5
import pygame
import pynput
from pygame.locals import *
from pynput.keyboard import Key, Listener

# These have to be hardcoded in case FGfGwKoptions.jsonc doesn't exist...
OPTIONS_FILE_NAME = 'FGfGwKoptions.jsonc'
GIT_URL = 'https://github.com/HenryFBP/FGfGwK'
CONFIG_URL = "{0}/raw/master/{1}".format(GIT_URL, OPTIONS_FILE_NAME)

""" Get absolute path to resource, works for dev and for PyInstaller """


def resource_path(relative_path, prefer_adjacent_dir=False):
    external_exe_file_dir = os.path.dirname(os.path.abspath(__file__))
    current_file_dir = os.getcwd()

    msg = ""
    if prefer_adjacent_dir:
        base_path = current_file_dir
        msg += "Not bundled in exe: "
    else:
        # _MEIPASS is a special env var set by pyinstaller.
        base_path = getattr(sys, '_MEIPASS', external_exe_file_dir)
        msg += "Bundled in exe:     "

    retval = os.path.abspath(os.path.join(base_path, relative_path))
    msg += retval
    print(msg)

    return retval


def is_windows():
    return 'win' in sys.platform


def not_windows():
    return not is_windows()


if is_windows():
    import ctypes
    from ctypes import wintypes


def is_modifier_key(k: Key):
    try:
        _ = k.char
        return False
    except AttributeError:
        return True


class GlobalState:
    def __init__(self, options: dict) -> None:
        self.optionsJson: dict = options
        self.keymap: dict = None
        self.keymap_is_chosen = False
        self.key_log: List[Key] = []
        self.message_array_log: List[List[str]] = self.optionsJson['default_messages']
        self.repeats: int = 0
        self.title: str = \
            self.optionsJson.get('title')
        self.icon_path: str = resource_path(self.optionsJson.get('icon_path'))
        self.running: bool = True
        self.required_linux_tools = {
            'xdotool': 'apt install xdotool',
            'wmctrl': 'apt install wmctrl',
        }

        self.currently_pressed_keys: Set[Key] = set()

    def choose_keymap(self, name: str):
        if name in self.all_keymaps().keys():
            self.keymap_is_chosen = True
            self.keymap = self.all_keymaps()[name]
        else:
            raise ValueError("No keymap called {}!".format(name))
        return self.keymap

    def all_keymaps(self) -> Dict[str, str]:
        return self.optionsJson.get('keymaps', dict())

    def current_keymap_keys_map(self) -> Dict[str, str]:
        return self.keymap.get('keys', dict())

    def current_keymap_chords_map(self) -> Dict[str, str]:
        return self.keymap.get('chords', dict())

    def current_keymap_mapped_keys(self) -> List[str]:
        return list(self.current_keymap_keys_map().keys())

    def enforce_linux_x11_dependencies(self):

        if not_windows():

            # os.environ['DISPLAY'] = ':0'
            # print(os.environ['DISPLAY'])

            for toolname in self.required_linux_tools.keys():
                packagename = self.required_linux_tools[toolname]
                if not which(toolname):
                    errormsg = (
                        ("Executable '{}' is missing. \n"
                         "Please install the package by running '{}'.").format(
                            toolname, packagename))
                    input(errormsg)
                    raise FileNotFoundError(errormsg)

    def is_key_pressed(self, k: Key):
        return k in self.currently_pressed_keys

    def press_key(self, k: Key):
        self.add_key(k)
        self.currently_pressed_keys.add(k)

    def release_key(self, k: Key):
        try:
            self.currently_pressed_keys.remove(k)
        except KeyError as ke:
            print(
                """ERROR: Probably a threading issue ;_;"
Failed to 'release' this key because it was already released: {}
Stack trace:"
""".format(k))
            print(ke)

    def add_key(self, k: Key):
        self.key_log.append(k)

    def get_key(self, i=-1) -> Key:
        return self.key_log[i]

    def total_keys_pressed(self) -> int:
        return len(self.key_log)

    def add_message(self, m: str, i=0):
        # ensure log is large enough
        while i >= len(self.message_array_log):
            self.message_array_log.append(list())

        self.message_array_log[i].append(m)

    def blank_message_log(self):
        for i in range(0, len(self.message_array_log)):
            self.add_message("", i)

    def get_message(self, j=-1, i=0) -> str:
        return self.message_array_log[i][j]

    def get_message_log(self, i=0) -> List[str]:
        return self.message_array_log[i]


OPTIONS_FILE = resource_path(OPTIONS_FILE_NAME, prefer_adjacent_dir=True)

if not os.path.exists(OPTIONS_FILE):
    # Try within the EXE if it doesn't exist outside...
    OPTIONS_FILE = resource_path(
        OPTIONS_FILE_NAME,
        prefer_adjacent_dir=False)

if not os.path.exists(OPTIONS_FILE):
    print("You don't have an options file. Downloading from '{}' into '{}'.".format(
        CONFIG_URL, OPTIONS_FILE
    ))
    urllib.request.urlretrieve(CONFIG_URL, OPTIONS_FILE)

    if not os.path.exists(OPTIONS_FILE):
        message = "Failed to automatically download options file...\n" \
                  "Please download it at {} and then place it in the same directory as the executable.\n > ".format(
            CONFIG_URL)
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


def window_always_on_top_win32(pygameinstance: pygame, x: int = 100, y: int = 200):
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND,
        wintypes.INT, wintypes.INT,
        wintypes.INT, wintypes.INT, wintypes.UINT
    ]

    hwnd = pygameinstance.display.get_wm_info()['window']

    user32.SetWindowPos(
        hwnd, -1,
        x, y,
        0, 0, 0x0001
    )


def window_always_on_top_x11(xdotool_search=__file__):
    print("searching with xdotool for class " + xdotool_search)

    process = subprocess.Popen(
        ['xdotool', 'search', '--class', xdotool_search],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    print(stdout)
    print(stderr)

    if stdout.strip() == '':
        raise Exception(
            "Error, could not find a window ID for {0}".format(xdotool_search))

    # noinspection PyUnusedLocal
    windowid = None
    try:
        windowid = int(stdout.strip())
    except ValueError:
        raise Exception(
            "Error, was returned '{0}' from xdotool instead of an int!".format(stdout))

    # do something with windowid...
    print("Found window with ID {0}. Going to use wmctrl to make it on top.".format(
        windowid))

    # show info
    process = subprocess.Popen(
        ['xprop', '-id', str(windowid)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    print(stdout)
    print(stderr)

    process = subprocess.Popen(
        ['wmctrl', '-i', '-r', str(windowid), '-b', 'add,above'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    print(stdout)
    print(stderr)


class KeyEvent:
    def __init__(self) -> None:
        raise Exception("lol todo :p")


def prompt_choose_keymap(state) -> None:
    """Returns true if a user picks a keymap successfully."""
    print("Keymap is not chosen yet! Asking them to choose...")

    state.add_message("[{:^10s}] Choose a keymap:".format(str(state.get_key())))
    all_keymap_names = list(state.all_keymaps().keys())

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

                state.add_message("Current keymap:  {}".format(chosen_keymap_name), 4)
                state.add_message("Valid keys:      {}".format(
                    ','.join(state.current_keymap_mapped_keys())
                ), 5)

                return

        except ValueError:
            pass

    # not successful
    return


def process_mashing(state: GlobalState) -> str:
    """Return a status string if mashing is detected."""
    if state.total_keys_pressed() >= 2:
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


def process_key_chords(state: GlobalState, msg: str = "") -> str:
    for chord_str in state.current_keymap_chords_map():
        print("Testing {}".format(chord_str))

    return msg + 'tbi'


def on_press(_key: pynput.keyboard.Key, state: GlobalState = GLOBAL_STATE):
    state.press_key(_key)

    # halt if they haven't chosen a keymap
    if not state.keymap_is_chosen:
        prompt_choose_keymap(state)
        return True

    msg = process_key_press(state)
    state.add_message(msg)

    # handle chords
    chordmsg = process_key_chords(state) + " (chord display)"
    if chordmsg:
        state.add_message(chordmsg, 1)


# noinspection PyUnusedLocal
def on_release(key, state=GLOBAL_STATE):
    state.release_key(key)
    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        print("We want to quit!")
        # GLOBAL_STATE.running = False
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
