"""Options file discovery and loading."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import json5

from potemkeys.keymap import Keymap, resolve_inherits

PROJECT_NAME = 'potemkeys'
OPTIONS_FILE_NAME = PROJECT_NAME + 'options.jsonc'
GIT_URL = 'https://github.com/HenryFBP/' + PROJECT_NAME

Color = Tuple[int, int, int]


@dataclass
class Options:
    title: str = 'potemkeys'
    quit_key: str = 'ESC'
    menu_key: str = 'F1'
    default_keymap: Optional[str] = None
    font_file: Optional[str] = 'DejaVuSansMono.ttf'
    font_type: str = 'dejavusansmono,consolas,menlo,monaco'
    font_size: int = 22
    font_margin: int = 4
    window_width: int = 1000
    window_height: int = 420
    window_always_on_top: bool = True
    icon_path: str = 'pelleds.jpg'
    background_color: Color = (20, 20, 20)
    text_color: Color = (255, 0, 0)
    dim_color: Color = (110, 110, 110)
    highlight_color: Color = (255, 230, 0)
    center_text: bool = False
    show_cheat_sheet: bool = True
    input_history_length: int = 10
    chord_window_ms: int = 400
    keymaps: Dict[str, Keymap] = field(default_factory=dict)
    path: Optional[Path] = None

    @classmethod
    def from_dict(cls, raw: dict, path: Optional[Path] = None) -> 'Options':
        known = {f.name for f in fields(cls)}
        unknown = sorted(set(raw) - known)
        if unknown:
            print(f'[config] ignoring unknown option(s): {", ".join(unknown)}')
        kwargs = {k: v for k, v in raw.items() if k in known and k not in ('keymaps', 'path')}
        for key in ('background_color', 'text_color', 'dim_color', 'highlight_color'):
            if key in kwargs:
                kwargs[key] = tuple(int(c) for c in kwargs[key])
        for key in ('quit_key', 'menu_key'):
            if key in kwargs:
                kwargs[key] = str(kwargs[key]).upper()
        raw_keymaps = raw.get('keymaps') or {}
        keymaps = {name: Keymap.from_dict(name, d) for name, d in resolve_inherits(raw_keymaps).items()}
        if not keymaps:
            raise ValueError('options file defines no keymaps')
        return cls(keymaps=keymaps, path=path, **kwargs)


def bundle_dir() -> Path:
    """Directory holding bundled resources (PyInstaller temp dir or this package)."""
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent))


def executable_dir() -> Optional[Path]:
    """Directory of the frozen executable, or None when running from source."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return None


def candidate_option_paths() -> List[Path]:
    """Where to look for the options file, most-preferred first."""
    dirs = [Path.cwd(), executable_dir(), bundle_dir()]
    seen, out = set(), []
    for d in dirs:
        if d is None or d in seen:
            continue
        seen.add(d)
        out.append(d / OPTIONS_FILE_NAME)
    return out


def find_options_file(explicit: Optional[str] = None) -> Path:
    if explicit:
        p = Path(explicit)
        if not p.is_file():
            raise FileNotFoundError(f'options file not found: {p}')
        return p
    for p in candidate_option_paths():
        if p.is_file():
            return p
    raise FileNotFoundError('no options file found; looked in:\n  ' +
                            '\n  '.join(str(p) for p in candidate_option_paths()))


def load_options(explicit: Optional[str] = None) -> Options:
    path = find_options_file(explicit)
    with open(path, encoding='utf-8') as fh:
        raw = json5.load(fh)
    return Options.from_dict(raw, path=path)


def resource_path(relative: str) -> Path:
    """Resolve a bundled resource like the icon: next to the options file, else in the bundle."""
    for d in (executable_dir(), bundle_dir()):
        if d is not None and (d / relative).exists():
            return d / relative
    return bundle_dir() / relative
