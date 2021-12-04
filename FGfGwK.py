#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position
import os
import subprocess
import sys
import time


def is_windows():
    return 'win' in sys.platform


def not_windows():
    return not is_windows()


if not_windows():
    os.environ['DISPLAY'] = ':0'
    print(os.environ['DISPLAY'])

import pynput
import json5
import pygame
from pygame.locals import *
from pynput.keyboard import Listener

if is_windows():
    import ctypes
    from ctypes import wintypes

TITLE = 'This app is for goldfish who can\'t remember buttons. Are you a goldfish? :3c'
RUNNING = True
MESSAGE = ['hello :)']
OPTIONS_FILE = './options.jsonc'
ICON_FILE = './pelleds.jpg'

OPTIONS = {}

with open(OPTIONS_FILE, encoding='utf-8') as fh:
    OPTIONS = json5.load(fh)


def window_always_on_top_WIN32(pygame: pygame, x: int = 100, y: int = 200):
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND,
        wintypes.INT, wintypes.INT,
        wintypes.INT, wintypes.INT, wintypes.UINT
    ]

    hwnd = pygame.display.get_wm_info()['window']

    user32.SetWindowPos(
        hwnd, -1,
        x, y,
        0, 0, 0x0001
    )


def window_always_on_top_X11(xdotool_search=__file__):
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
        raise Exception("Error, could not find a window ID for {0}".format(xdotool_search))

    windowid = None
    try:
        windowid = int(stdout.strip())
    except ValueError:
        raise Exception("Error, was returned '{0}' from xdotool instead of an int!".format(stdout))

    # do something with windowid...
    print("Found window with ID {0}. Going to use wmctrl to make it on top.".format(windowid))

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
if OPTIONS['current_keymap'] not in OPTIONS['keymaps'].keys():
    raise ValueError("""You have specified a game that is not configured!\n
    You want: {}\n
    Valid games: {}""".format(
        OPTIONS['current_keymap'],
        ','.join(list(OPTIONS['keymaps'].keys()))
    ))

ACTIVE_KEYMAP = OPTIONS['keymaps'][OPTIONS['current_keymap']]
MESSAGE = ['You are playing ' + OPTIONS['current_keymap']]

LAST_KEY = [None]
REPEATS = [1]


def on_press(key, strptr=MESSAGE, repeatsptr=REPEATS, lastkeyptr=LAST_KEY):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        strptr[0] = "{}".format(key.char)

        normalized_key = key.char.upper()
        if normalized_key in ACTIVE_KEYMAP.keys():
            strptr[0] += ' = {:2s}'.format(ACTIVE_KEYMAP[normalized_key])
        else:
            strptr[0] += ' = ?'

        if lastkeyptr[0] == normalized_key:
            # they mashin', show it
            repeatsptr[0] += 1
            strptr[0] += f' (x{repeatsptr[0]})'
        else:
            # not mashin', reset
            repeatsptr[0] = 1
        lastkeyptr[0] = normalized_key

    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    print('{0} released'.format(key))
    # if key == Key.esc:
    #     # Stop listener
    #     return False


if __name__ == '__main__':

    # using .start() is non blocking
    keylistener = Listener(on_press=on_press, on_release=on_release)
    keylistener.start()

    window_width, window_height = OPTIONS['window_width'], OPTIONS['window_height']
    screen_width, screen_height = OPTIONS['screen_width'], OPTIONS['screen_height']

    pygame.init()

    pygame_icon = pygame.image.load(ICON_FILE)
    pygame.display.set_icon(pygame_icon)

    FONT = pygame.font.SysFont(OPTIONS['font_type'], OPTIONS['font_size'])
    DISPLAYSURFACE = pygame.display.set_mode(
        (window_width, window_height), pygame.RESIZABLE
    )
    pygame.display.set_caption(TITLE)

    # make on top
    if OPTIONS['window_always_on_top']:
        if is_windows():
            window_always_on_top_WIN32(
                pygame,
                x=int((screen_width / 2) - (window_width / 2)),
                y=int((screen_height / 2) - (window_height / 2))
            )
        else:
            window_always_on_top_X11()

    # main game loop
    while RUNNING:

        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text = FONT.render(
            MESSAGE[0], True, OPTIONS['text_color'], OPTIONS['background_color'])
        textRect = text.get_rect()

        window_width, window_height = DISPLAYSURFACE.get_size()

        if OPTIONS['center_text']:
            textRect.center = (window_width // 2, window_height // 2)

        DISPLAYSURFACE.fill(OPTIONS['background_color'])
        DISPLAYSURFACE.blit(text, textRect)

        pygame.display.update()
