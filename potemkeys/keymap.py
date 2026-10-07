"""Keymap model and matching logic. Pure Python, no pynput/pygame.

All key names are uppercase strings: ``"A"``, ``";"``, ``"CTRL"``, ``"F1"``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

_NOTATION_RE = re.compile(r'^(\[[^\]]+\])\s*(.*)$')
_MODIFIER_RE = re.compile(r'^(\([^)]+\))\s*(.*)$')
_CATEGORY_RE = re.compile(r'\s*(\[[^\]]+\])\s*$')


@dataclass(frozen=True)
class KeyDisplay:
    """Parsed form of a mapping value such as ``"[HS] (p) Heavy Slash [bar]"``."""
    notation: str = ''
    modifier: Optional[str] = None
    description: str = ''
    category: Optional[str] = None

    @property
    def short(self) -> str:
        """Compact label: notation if present, otherwise description."""
        return self.notation or self.description

    def __str__(self) -> str:
        return ' '.join(p for p in (self.notation, self.modifier, self.description, self.category) if p)


def parse_key_display(s: str) -> KeyDisplay:
    s = s.strip()
    m = _NOTATION_RE.match(s)
    if not m:
        return KeyDisplay(description=s)
    notation, rest = m.group(1), m.group(2).strip()

    modifier = None
    m = _MODIFIER_RE.match(rest)
    if m:
        modifier, rest = m.group(1), m.group(2).strip()

    category = None
    m = _CATEGORY_RE.search(rest)
    if m and m.start() > 0:
        category, rest = m.group(1), rest[:m.start()].strip()

    return KeyDisplay(notation=notation, modifier=modifier, description=rest, category=category)


def split_combo(s: str) -> List[str]:
    """``"CTRL-X"`` or ``"ALT D"`` -> ``["CTRL", "X"]``. Held keys first, trigger last."""
    s = s.strip()
    parts = s.split() if ' ' in s else s.split('-')
    parts = [p.upper() for p in parts if p]
    # A lone "-" splits into nothing; treat it as the literal key.
    return parts or [s.upper()]


@dataclass(frozen=True)
class Macro:
    name: str
    inputs: str
    held: Tuple[str, ...]
    trigger: str


@dataclass
class Keymap:
    name: str
    keys: Dict[str, KeyDisplay] = field(default_factory=dict)
    chords: Dict[Tuple[str, ...], str] = field(default_factory=dict)
    combos: Dict[Tuple[str, ...], str] = field(default_factory=dict)
    macros: List[Macro] = field(default_factory=list)

    @classmethod
    def from_dict(cls, name: str, raw: dict) -> 'Keymap':
        keys = {k.upper(): parse_key_display(str(v)) for k, v in raw.get('keys', {}).items()}
        chords = {tuple(c.upper().split()): str(v) for c, v in raw.get('chords', {}).items()}
        combos = {tuple(split_combo(c)): str(v) for c, v in raw.get('combinations', {}).items()}
        return cls(name=name, keys=keys, chords=chords, combos=combos, macros=_parse_macros(raw.get('macros', [])))

    def describe(self, key: str) -> Optional[KeyDisplay]:
        return self.keys.get(key.upper())

    def matching_chords(self, history: Sequence[str]) -> List[Tuple[Tuple[str, ...], str]]:
        """Chords whose key sequence equals the tail of ``history``."""
        out = []
        for seq, label in self.chords.items():
            n = len(seq)
            if n <= len(history) and tuple(history[-n:]) == seq:
                out.append((seq, label))
        return out

    def matching_combos(self, key: str, held: Iterable[str]) -> List[Tuple[Tuple[str, ...], str]]:
        """Combos whose trigger is ``key`` and whose other keys are all in ``held``."""
        held = set(held)
        return [(seq, label) for seq, label in self.combos.items()
                if seq[-1] == key and all(h in held for h in seq[:-1])]

    def triggered_macros(self, key: str, held: Iterable[str]) -> List[Macro]:
        held = set(held)
        return [m for m in self.macros if m.trigger == key and all(h in held for h in m.held)]


def _parse_macros(raw) -> List[Macro]:
    # Accept both ``[{name: {...}}, ...]`` and ``{name: {...}}``.
    items = raw.items() if isinstance(raw, dict) else (kv for d in raw for kv in d.items())
    out = []
    for name, spec in items:
        trigger = spec.get('trigger', '')
        if isinstance(trigger, dict):
            trigger = trigger.get('sequence', '')
        parts = split_combo(str(trigger))
        out.append(Macro(name=str(name), inputs=str(spec.get('inputs', '')),
                         held=tuple(parts[:-1]), trigger=parts[-1]))
    return out


def resolve_inherits(raw_keymaps: Dict[str, dict]) -> Dict[str, dict]:
    """Expand ``"inherit": "Parent"`` so each keymap dict is self-contained.

    Child entries override parent entries; macro lists are concatenated.
    """
    resolved: Dict[str, dict] = {}

    def resolve(name: str, chain: Tuple[str, ...]) -> dict:
        if name in resolved:
            return resolved[name]
        if name in chain:
            raise ValueError('keymap inherit cycle: ' + ' -> '.join(chain + (name,)))
        if name not in raw_keymaps:
            raise KeyError(f'keymap {chain[-1]!r} inherits unknown keymap {name!r}')
        raw = dict(raw_keymaps[name])
        parent_name = raw.pop('inherit', None)
        if parent_name is not None:
            parent = resolve(str(parent_name), chain + (name,))
            merged = {}
            for section in ('keys', 'chords', 'combinations'):
                merged[section] = {**parent.get(section, {}), **raw.get(section, {})}
            merged['macros'] = _as_macro_list(parent.get('macros')) + _as_macro_list(raw.get('macros'))
            raw = merged
        resolved[name] = raw
        return raw

    for n in raw_keymaps:
        resolve(n, ())
    return resolved


def _as_macro_list(raw) -> list:
    if not raw:
        return []
    if isinstance(raw, dict):
        return [{k: v} for k, v in raw.items()]
    return list(raw)
