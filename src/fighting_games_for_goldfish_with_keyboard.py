# keylogger using pynput module

# links that make me want to kill myself
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
MESSAGE=['phucking beesechurger']

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# class RECT(Structure):
#     _fields_ = [
#         ('left',    c_long),
#         ('top',     c_long),
#         ('right',   c_long),
#         ('bottom',  c_long),
#     ]
#     def width(self):
#         return self.right  - self.left
#     def height(self):
#         return self.bottom - self.top


# def onTop(window:int): # https://stackoverflow.com/a/25383929/4262535
#     '''
#     ex:
#         onTop(pygame.display.get_wm_info()['window'])
#     '''
#     rc = RECT()
#     windll.user32.GetWindowRect(window, byref(rc))
#     windll.user32.SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)

def window_always_on_top(hwnd: int, x: int = 100, y: int = 200):
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [
        wintypes.HWND, wintypes.HWND,
        wintypes.INT, wintypes.INT,
        wintypes.INT, wintypes.INT, wintypes.UINT
    ]

    user32.SetWindowPos(
        hwnd, -1,
        x, y,
        0, 0, 0x0001
    )


# keymaps
ggst_map = {
    'A': "left",
}

tekken7map = {
    'A': "left"
}

game_map = {
    'GG:S': ggst_map,
    'Tekken 7': tekken7map,
}


def on_press(key,strref=MESSAGE):

    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        strref[0]="NIGGA YOU PRESSING "+key.char+" ?????"

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

    width, height = 400, 300

    pygame.init()

    FONT = pygame.font.SysFont("Arial",32)
    DISPLAYSURFACE = pygame.display.set_mode((width, height))
    pygame.display.set_caption(TITLE)
    # our int handle is pygame.display.get_wm_info()['window']

    # make on top
    window_handle: int = pygame.display.get_wm_info()['window']
    window_always_on_top(
        window_handle,
        x=int((1920/2)-(width/2)),
        # who cares????? so what, you can do math 😭😔
        y=int((1080/2)-(height/2))
    )
    
    # main game loop
    while RUNNING:

        # handle game events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        text = FONT.render(MESSAGE[0], True, green, blue)
        textRect = text.get_rect()
        textRect.center = (width // 2, height // 2)
        DISPLAYSURFACE.fill(white)
        DISPLAYSURFACE.blit(text, textRect)

        pygame.display.update()
