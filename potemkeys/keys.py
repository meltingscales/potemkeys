"""pynput adapter: global keyboard hook -> key-name strings, and macro playback."""
from __future__ import annotations

import queue
import sys
import threading
import time
from enum import Enum
from typing import List, Optional, Tuple

from pynput.keyboard import Controller, Key, KeyCode, Listener

MODIFIER_BASES = ('CTRL', 'SHIFT', 'ALT', 'CMD', 'SUPER', 'META')

Event = Tuple[str, str, bool]  # ('press' | 'release', key name, injected)


def key_to_str(key) -> Optional[str]:
    """Normalize a pynput key to an uppercase name, or None if unknown.

    ``Key.ctrl_l`` -> ``"CTRL"``, ``Key.f1`` -> ``"F1"``, ``KeyCode('a')`` -> ``"A"``,
    ctrl+x (reported as char ``"\\x18"``) -> ``"X"``.
    """
    if key is None:
        return None
    if isinstance(key, Enum):  # pynput.keyboard.Key member
        name = key.name.upper()
        for base in MODIFIER_BASES:
            if name.startswith(base):
                return base
        return name
    char = getattr(key, 'char', None)
    if char:
        code = ord(char)
        if code < 32:  # control character from ctrl+letter
            return chr(code + 64)
        return char.upper()
    vk = getattr(key, 'vk', None)
    if vk is not None:
        # Windows virtual-key codes and X11 keysyms both put 0-9 and A-Z at their ASCII values;
        # X11 keysyms also use lowercase a-z (on Windows that range is numpad/F-keys).
        if 0x30 <= vk <= 0x39 or 0x41 <= vk <= 0x5A or (0x61 <= vk <= 0x7A and sys.platform != 'win32'):
            return chr(vk).upper()
        return f'VK{vk}'
    return None


def start_listener(events: 'queue.Queue[Event]') -> Listener:
    """Start a daemon listener that pushes (kind, key, injected) onto ``events``."""
    def on_press(key, injected: bool = False):
        name = key_to_str(key)
        if name:
            events.put(('press', name, bool(injected)))

    def on_release(key, injected: bool = False):
        name = key_to_str(key)
        if name:
            events.put(('release', name, bool(injected)))

    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    return listener


# -- macros ------------------------------------------------------------------

_controller: Optional[Controller] = None
_controller_lock = threading.Lock()


def _get_controller() -> Controller:
    global _controller
    with _controller_lock:
        if _controller is None:
            _controller = Controller()
        return _controller


def token_to_key(token: str):
    """``"a"`` -> KeyCode, ``"CTRL"`` -> Key.ctrl, ``"F1"`` -> Key.f1."""
    if len(token) == 1:
        return KeyCode.from_char(token.lower())
    name = token.lower()
    for candidate in (name, name + '_l'):
        if candidate in Key.__members__:
            return Key[candidate]
    raise ValueError(f'unknown macro key {token!r}')


def parse_macro(inputs: str) -> List[Tuple[str, object]]:
    """``"A 0.1 S+J"`` -> ``[('keys', ['A']), ('delay', 0.1), ('keys', ['S', 'J'])]``.

    Keys joined with ``+`` are pressed together and released together.
    """
    steps: List[Tuple[str, object]] = []
    for token in inputs.split():
        try:
            steps.append(('delay', float(token)))
        except ValueError:
            steps.append(('keys', token.split('+')))
    return steps


def run_macro(inputs: str) -> None:
    """Play a macro on a background thread so the UI never blocks."""
    threading.Thread(target=_play, args=(inputs,), daemon=True).start()


def _play(inputs: str) -> None:
    controller = _get_controller()
    for kind, value in parse_macro(inputs):
        if kind == 'delay':
            time.sleep(float(value))
            continue
        try:
            keys = [token_to_key(t) for t in value]
        except ValueError as e:
            print(f'[macro] {e}')
            continue
        for k in keys:
            controller.press(k)
        for k in reversed(keys):
            controller.release(k)
