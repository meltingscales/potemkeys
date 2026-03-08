import os
import subprocess
import sys

import pygame

from potemkeys import Config


def is_windows():
    return 'win' in sys.platform


def not_windows():
    return not is_windows()


if is_windows():
    import ctypes
    from ctypes import wintypes


def resource_path(relative_path, prefer_adjacent_dir=False):
    """ Get absolute path to resource, works for dev and for PyInstaller """
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


def window_always_on_top_x11(pygameinstance: pygame):
    windowid = pygameinstance.display.get_wm_info()['window']
    print("Found window with ID {0}. Going to use wmctrl to make it on top.".format(windowid))

    process = subprocess.Popen(
        ['wmctrl', '-i', '-r', str(windowid), '-b', 'add,above'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
