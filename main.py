# keylogger using pynput module

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position

from typing import List
import pynput
import os
import pygame
import sys
from pygame.locals import *
from pynput.keyboard import Key, Listener
import ctypes
from ctypes import windll, wintypes, Structure, c_long, byref  # windows only
import win32gui
import win32con
import win32api
from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT
from ctypes import windll

NOSIZE = 1
NOMOVE = 2
TOPMOST = -1
NOT_TOPMOST = -2

TITLE = 'This app is for goldfish who can\'t remember buttons. Are you a goldfish? :3c'
RUNNING = True
MESSAGE = ['hello :)']

white = (255, 255, 255)
black = (0,0,0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)


def window_always_on_top_WIN32(pygame: pygame, x: int = 100, y: int = 200):

    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND,
        wintypes.INT, wintypes.INT,
        wintypes.INT, wintypes.INT, wintypes.UINT
    ]

    hwnd=pygame.display.get_wm_info()['window']

    user32.SetWindowPos(
        hwnd, -1,
        x, y,
        0, 0, 0x0001
    )


# keymaps
ggst_map = {
    'W': "jump",
    'A': "left",
    'S': "crouch",
    'D': "right",

    'U': '[P] Punch',
    'I': '[S] Slash',
    'J': '[K] Kick',
    'K': '[HS] HSlash',
    'O': '[D] Dust'
}

tekken7map = {
    'W': "jump",
    'A': "left",
    'S': "crouch",
    'D': "right",
}

ALL_GAME_MAPS = {
    'GG:S': ggst_map,
    'Tekken 7': tekken7map,
}

# just use GG:S for now
ACTIVE_GAME_MAP = ALL_GAME_MAPS['GG:S']


def on_press(key, strref=MESSAGE):

    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        strref[0] = "{}".format(key.char)

        normalized_key = key.char.upper()
        if(normalized_key in ACTIVE_GAME_MAP.keys()):
            strref[0] += '={}'.format(ACTIVE_GAME_MAP[normalized_key])

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

    gamewidth, gameheight = 400, 300
    screenwidth, screenheight = 1920, 1080

    pygame.init()

    FONT = pygame.font.SysFont("Consolas", 32)
    DISPLAYSURFACE = pygame.display.set_mode(
        (gamewidth, gameheight), pygame.RESIZABLE
    )
    pygame.display.set_caption(TITLE)
    # our int handle is 

    # make on top
    window_always_on_top_WIN32(
        pygame,
        x=int((screenwidth/2)-(gamewidth/2)),
        y=int((screenheight/2)-(gameheight/2))
    )

    # main game loop
    while RUNNING:

        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text = FONT.render(MESSAGE[0], True, red, black)
        textRect = text.get_rect()
        
        gamewidth, gameheight = DISPLAYSURFACE.get_size()


        textRect.center = (gamewidth // 2, gameheight // 2)
        DISPLAYSURFACE.fill(black)
        DISPLAYSURFACE.blit(text, textRect)

        pygame.display.update()
