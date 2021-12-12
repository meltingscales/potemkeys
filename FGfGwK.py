#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position
import time
from typing import List
from pynput.keyboard import Key, Listener
from pygame.locals import *
import pynput
import pygame
import json5
import os
import subprocess
import sys
from shutil import which
import urllib.request

# These have to be hardcoded in case options.jsonc doesn't exist...
OPTIONS_FILE_NAME = 'options.jsonc'
GIT_URL = 'https://github.com/HenryFBP/FGfGwK'
CONFIG_URL = GIT_URL + "/raw/master/options.jsonc"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(os.path.join(base_path, relative_path))


def is_windows():
    return 'win' in sys.platform


def not_windows():
    return not is_windows()


if is_windows():
    import ctypes
    from ctypes import wintypes


class GlobalState:
    def __init__(self, options: dict) -> None:
        self.optionsJson: dict = options
        self.keymap: dict = self.optionsJson['keymaps'][self.optionsJson['current_keymap']]
        self.key_log: List[pynput.keyboard.Key] = []
        self.message_log: List[str] = [
            'You are playing ' + self.optionsJson['current_keymap']]
        self.repeats: int = 0
        self.title: str = \
            self.optionsJson.get('title',
                                 'This app is for goldfish who can\'t remember buttons. Are you a goldfish? :3c')
        self.icon_path: str = resource_path(self.optionsJson.get('icon_path'))
        self.running: bool = True
        self.required_linux_tools = {
            'xdotool': 'apt install xdotool',
            'wmctrl': 'apt install wmctrl',
        }

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

    def add_key(self, k: pynput.keyboard.Key):
        self.key_log.append(k)

    def get_key(self, i=-1) -> pynput.keyboard.Key:
        return self.key_log[i]

    def get_key_log_length(self) -> int:
        return len(self.key_log)

    def add_message(self, m: str):
        self.message_log.append(m)

    def get_message(self, i=-1) -> str:
        return self.message_log[i]


OPTIONS_FILE = resource_path(OPTIONS_FILE_NAME)

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
    # lol yes we are fucking doing this shitty programming practice     >:3c
    GLOBAL_STATE = GlobalState(options=jsonobj)
    print("Using file:")
    print(OPTIONS_FILE)

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


# if they want a non existent game
if GLOBAL_STATE.optionsJson['current_keymap'] not in GLOBAL_STATE.optionsJson['keymaps'].keys():
    raise ValueError("""You have specified a game that is not configured!\n
    You want: {}\n
    Valid games: {}""".format(
        GLOBAL_STATE.optionsJson['current_keymap'],
        ','.join(list(GLOBAL_STATE.optionsJson['keymaps'].keys()))
    ))


class KeyEvent:
    def __init__(self) -> None:
        raise Exception("lol todo :p")


def on_press(key: pynput.keyboard.Key, state: GlobalState = GLOBAL_STATE):
    state.add_key(key)

    tmpmessage = ""

    try:
        print('alphanumeric key {0} pressed'.format(state.get_key().char))
        tmpmessage = "{}".format(state.get_key().char)

        normalized_key = state.get_key().char.upper()
        if normalized_key in GLOBAL_STATE.keymap.keys():
            tmpmessage += ' = {:2s}'.format(
                GLOBAL_STATE.keymap[normalized_key])
        else:
            tmpmessage += ' = ?'

        print("pressed {} keys".format(state.get_key_log_length()))

        if state.get_key_log_length() >= 2:
            # if they've pressed at least 2 keys
            if (state.get_key(-2)).char.upper() == normalized_key:
                # they mashin', show it
                state.repeats += 1
                tmpmessage += f' (x{state.repeats})'
            else:
                # not mashin', reset
                state.repeats = 1

    except AttributeError:
        print('special key {0} pressed'.format(state.get_key()))
    finally:
        GLOBAL_STATE.add_message(tmpmessage)


# noinspection PyUnusedLocal
def on_release(key, state=GLOBAL_STATE):
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

        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text = FONT.render(
            GLOBAL_STATE.get_message(), True, GLOBAL_STATE.optionsJson['text_color'],
            GLOBAL_STATE.optionsJson['background_color'])
        textRect = text.get_rect()

        window_width, window_height = DISPLAYSURFACE.get_size()

        if GLOBAL_STATE.optionsJson['center_text']:
            textRect.center = (window_width // 2, window_height // 2)

        DISPLAYSURFACE.fill(GLOBAL_STATE.optionsJson['background_color'])
        DISPLAYSURFACE.blit(text, textRect)

        pygame.display.update()
