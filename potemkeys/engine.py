"""Input state machine. Pure Python: takes key-name strings, produces display text.

Drive it from one thread (the UI loop) by feeding events queued by the keyboard
listener. ``lines`` is what the UI should draw; ``keymap`` and ``held`` let the
UI draw the cheat sheet.
"""
from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Deque, List, Optional, Set

from potemkeys.config import Options
from potemkeys.keymap import Keymap

MENU_CHOICES = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'


@dataclass(frozen=True)
class Press:
    key: str
    time: float
    injected: bool = False


class Engine:
    def __init__(self, options: Options, run_macro: Optional[Callable[[str], None]] = None,
                 clock: Callable[[], float] = time.monotonic) -> None:
        self.options = options
        self.run_macro = run_macro or (lambda inputs: None)
        self.clock = clock

        self.keymap: Optional[Keymap] = None
        self.held: Set[str] = set()
        self.history: Deque[Press] = deque(maxlen=max(2, options.input_history_length))
        self.repeats = 0
        self.lines: List[str] = []
        self.quit_requested = False

        if options.default_keymap:
            self.select_keymap(options.default_keymap)
        else:
            self.show_menu()

    # -- keymap selection ----------------------------------------------------

    @property
    def keymap_names(self) -> List[str]:
        return list(self.options.keymaps)

    @property
    def in_menu(self) -> bool:
        return self.keymap is None

    def show_menu(self) -> None:
        self.keymap = None
        self.history.clear()
        self.repeats = 0
        self.lines = [f'Pick a keymap by pressing its key ({self.options.quit_key} quits):']
        for choice, name in zip(MENU_CHOICES, self.keymap_names):
            self.lines.append(f'  [{choice}] {name}')
        if len(self.keymap_names) > len(MENU_CHOICES):
            self.lines.append(f'  ... {len(self.keymap_names) - len(MENU_CHOICES)} more not shown')

    def select_keymap(self, name: str) -> None:
        if name not in self.options.keymaps:
            raise KeyError(f'no keymap named {name!r}; have: {", ".join(self.keymap_names)}')
        self.keymap = self.options.keymaps[name]
        self.history.clear()
        self.repeats = 0
        self._render_idle()

    def _menu_choice(self, key: str) -> Optional[str]:
        idx = MENU_CHOICES.find(key)
        if 0 <= idx < len(self.keymap_names):
            return self.keymap_names[idx]
        return None

    # -- events --------------------------------------------------------------

    def on_press(self, key: str, injected: bool = False) -> None:
        key = key.upper()
        now = self.clock()
        self.held.add(key)

        if self.in_menu:
            name = self._menu_choice(key)
            if name:
                self.select_keymap(name)
            return

        if key == self.options.menu_key:
            self.show_menu()
            return

        prev = self.history[-1] if self.history else None
        self.repeats = self.repeats + 1 if prev and prev.key == key else 1
        self.history.append(Press(key, now, injected))

        chord_keys = self._chord_window_keys(now)
        chords = self.keymap.matching_chords(chord_keys)
        combos = self.keymap.matching_combos(key, self.held)
        macros = [] if injected else self.keymap.triggered_macros(key, self.held)
        for m in macros:
            self.run_macro(m.inputs)

        self.lines = [
            'Input: ' + self._history_text(),
            'Chord: ' + (', '.join(f'{"-".join(seq)} = {label}' for seq, label in chords) or '-'),
            'Combo: ' + (', '.join(f'{"-".join(seq)} = {label}' for seq, label in combos) or '-'),
            'Macro: ' + (', '.join(m.name for m in macros) or '-'),
        ] + self._footer()

    def on_release(self, key: str, injected: bool = False) -> None:
        key = key.upper()
        self.held.discard(key)
        if key == self.options.quit_key:
            self.quit_requested = True

    # -- text ----------------------------------------------------------------

    def _chord_window_keys(self, now: float) -> List[str]:
        """Keys of the most recent presses, each within chord_window_ms of the next."""
        window = self.options.chord_window_ms / 1000.0
        keys: List[str] = []
        later = now
        for p in reversed(self.history):
            if later - p.time > window:
                break
            keys.append(p.key)
            later = p.time
        keys.reverse()
        return keys

    def _history_text(self) -> str:
        older = [self._short(p.key) for p in list(self.history)[:-1]]
        latest = self.history[-1]
        current = f'{latest.key} = {self._full(latest.key)}'
        if self.repeats > 1:
            current += f' (x{self.repeats})'
        return (' '.join(older) + '  |  ' if older else '') + current

    def _short(self, key: str) -> str:
        kd = self.keymap.describe(key)
        return kd.short if kd else key

    def _full(self, key: str) -> str:
        kd = self.keymap.describe(key)
        return str(kd) if kd else '?'

    def _footer(self) -> List[str]:
        return [
            '',
            f'Keymap: {self.keymap.name}   ({self.options.menu_key} = menu, {self.options.quit_key} = quit)',
        ]

    def _render_idle(self) -> None:
        self.lines = ['Input: -', 'Chord: -', 'Combo: -', 'Macro: -'] + self._footer()
