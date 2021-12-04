# keylogger using pynput module


from typing import List
import pynput
import pygame, sys
from pygame.locals import *
from pynput.keyboard import Key, Listener
from ctypes import windll, Structure, c_long, byref #windows only
import win32gui
import win32con
import win32api


class RECT(Structure):
    _fields_ = [
        ('left',    c_long),
        ('top',     c_long),
        ('right',   c_long),
        ('bottom',  c_long),
    ]
    
    def width(self):  
        return self.right  - self.left
    
    def height(self): 
        return self.bottom - self.top


def onTop(window): # https://stackoverflow.com/a/25383929/4262535
    '''
    ex:
        onTop(pygame.display.get_wm_info()['window'])
    '''
    rc = RECT()
    windll.user32.GetWindowRect(window, byref(rc))
    windll.user32.SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)


# keymaps
ggst_map={
    'A':"left",
}

tekken7map={
    'A':"left"
}

game_map={
    'GG:S':ggst_map,
    'Tekken 7':tekken7map,
}

# funcs
def write_file(keys: List[str]):

    with open('log.txt', 'w') as f:
        for key in keys:

            # removing ''
            k = str(key).replace("'", "")
            f.write(k)

            # explicitly adding a space after
            # every keystroke for readability
            f.write(' ')


def on_press(key, log: list = None):

    if log:
        log.append(key)
        write_file(log)

    try:
        print('alphanumeric key {0} pressed'.format(key.char))

    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):

    print('{0} released'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

if __name__ == '__main__':

    # using suppress is non-blocking
    keylistener= Listener(on_press=on_press, on_release=on_release)
    keylistener.start()

    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Hello World!')

    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
