#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position

import threading
import time
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pynput
from pynput.keyboard import Key, KeyCode

from potemkeys.GlobalState import GlobalState


def is_modifier_key(k) -> bool:
    try:
        _ = k.char
        return False
    except AttributeError:
        return True


def normalize_modifier_name(k: Key) -> str:
    """Normalize ctrl_l/ctrl_r -> CTRL, shift_l/shift_r -> SHIFT, etc."""
    name = k.name.upper()
    for base in ['CTRL', 'SHIFT', 'ALT', 'CMD', 'SUPER', 'META']:
        if name.startswith(base):
            return base
    return name


def get_key_str(k) -> str:
    """Get a normalized uppercase string for any key."""
    if is_modifier_key(k):
        return normalize_modifier_name(k)
    try:
        return k.char.upper()
    except AttributeError:
        return str(k).upper()


def is_key_str_pressed(state: GlobalState, key_str: str) -> bool:
    """Check if a key string (e.g. 'CTRL', 'S') is currently held down."""
    key_str = key_str.upper()
    for pressed_key in state.get_all_pressed_keys():
        if get_key_str(pressed_key) == key_str:
            return True
    return False


# ---------------------------------------------------------------------------
# Key display parser
# ---------------------------------------------------------------------------

@dataclass
class KeyDisplay:
    """Parsed representation of a key mapping value like '[HS] (p) HSlash [bar]'."""
    notation: str           # e.g. '[HS]'
    modifier: Optional[str] # e.g. '(p)', or None
    description: str        # e.g. 'HSlash'
    category: Optional[str] # e.g. '[bar]', or None

    def __str__(self):
        parts = [self.notation]
        if self.modifier:
            parts.append(self.modifier)
        parts.append(self.description)
        if self.category:
            parts.append(self.category)
        return ' '.join(parts)


def parse_key_display(s: str) -> KeyDisplay:
    """Parse a mapping value string into a KeyDisplay.

    Supports formats like:
      '[HS]  HSlash'
      '[HS] (p) foo [bar]'
    """
    import re
    s = s.strip()

    # Extract first bracketed token as notation
    m = re.match(r'^(\[[^\]]+\])\s*(.*)', s)
    if not m:
        return KeyDisplay(notation='', modifier=None, description=s, category=None)

    notation = m.group(1)
    rest = m.group(2).strip()

    # Optional parenthesised modifier
    modifier = None
    m2 = re.match(r'^(\([^)]+\))\s*(.*)', rest)
    if m2:
        modifier = m2.group(1)
        rest = m2.group(2).strip()

    # Optional trailing bracketed category
    category = None
    m3 = re.search(r'\s*(\[[^\]]+\])\s*$', rest)
    if m3:
        category = m3.group(1)
        rest = rest[:m3.start()].strip()

    return KeyDisplay(notation=notation, modifier=modifier, description=rest, category=category)


# ---------------------------------------------------------------------------
# Keymap selection
# ---------------------------------------------------------------------------

def display_keymap_menu(state) -> None:
    """Populate the message log with the keymap selection menu."""
    all_keymap_names = list(state.get_all_keymaps().keys())
    state.add_message("Choose a keymap by pressing its number:", 0)
    for i, keymapname in enumerate(all_keymap_names):
        state.add_message("[{}]: {}".format(i, keymapname), i + 1)


def prompt_choose_keymap(state) -> None:
    """Try to select a keymap based on the current keypress; refresh the menu display."""
    print("Keymap is not chosen yet! Asking them to choose...")

    all_keymap_names = list(state.get_all_keymaps().keys())

    display_keymap_menu(state)

    if not is_modifier_key(state.get_key()):
        try:
            user_wants_n = int(state.get_key().char)

            if (user_wants_n >= 0) and (user_wants_n <= len(all_keymap_names)):
                # they select n
                chosen_keymap_name = all_keymap_names[user_wants_n]
                state.choose_keymap(chosen_keymap_name)

                # clear other message logs
                state.blank_message_log()

                mi = 4

                state.add_message("Valid keys:      {}".format(
                    ','.join(state.current_keymap_mapped_keys())
                ), mi)
                mi += 1

                state.add_message("Valid chords:    {}".format(
                    ','.join(state.current_keymap_mapped_chords())
                ), mi)
                mi += 1

                state.add_message("Valid combos:    {}".format(
                    ','.join(state.current_keymap_mapped_combinations())
                ), mi)
                mi += 1

                state.add_message("Current keymap:  {}".format(
                    chosen_keymap_name
                ), mi)
                mi += 1

                # clear the key log, they've chosen
                state.clear_key_log()

                return

        except ValueError:
            pass

    # not successful
    return


# ---------------------------------------------------------------------------
# Key processing
# ---------------------------------------------------------------------------

def process_mashing(state: GlobalState) -> str:
    """Return a status string if mashing is detected."""
    if state.key_log_length() >= 2:
        prev_key = state.get_key(-2)

        if prev_key == state.get_key():
            state.repeats += 1
            return f' (x{state.repeats})'
        else:
            state.repeats = 1

    return ""


def process_key_press(state: GlobalState, msg: str = "") -> str:
    key = state.get_key()

    if not is_modifier_key(key):
        key_char = key.char
        normalized_key_char = key_char.upper()

        print('alphanumeric key {0} pressed'.format(key_char))
        msg += "{}".format(key_char)

        if normalized_key_char in state.current_keymap_mapped_keys():
            kd = parse_key_display(state.current_keymap_keys_map()[normalized_key_char])
            msg += ' = {}'.format(kd)
        else:
            msg += ' = ?'

    else:
        key_name = normalize_modifier_name(key)
        print('modifier key {0} pressed'.format(key_name))
        msg += key_name

        if key_name in state.current_keymap_mapped_keys():
            kd = parse_key_display(state.current_keymap_keys_map()[key_name])
            msg += ' = {}'.format(kd)
        else:
            msg += ' = ?'

    msg += process_mashing(state)
    return msg


def process_key_chords(state: GlobalState) -> List[List[KeyCode]]:
    results: List[List[KeyCode]] = []

    for chord_str in state.current_keymap_chords_map():

        splitchord: List[str] = chord_str.split(' ')
        splitchord = [s.upper() for s in splitchord]

        chordlen = len(splitchord)

        if chordlen > state.key_log_length():
            break

        key_log_slice = []

        for i in range(state.key_log_length() - 1, -1, -1):
            key_log_slice.append(state.get_key(i))
            if len(key_log_slice) >= chordlen:
                break

        key_log_slice.reverse()

        matching_keys: List[Key] = []
        for i in range(0, len(splitchord)):
            currentKey = key_log_slice[i]
            current_chord_member = splitchord[i]
            currentKeyCharCode: str = get_key_str(currentKey)

            if not (current_chord_member.upper() == currentKeyCharCode.upper()):
                break
            else:
                matching_keys.append(currentKey)

            if i == (len(splitchord) - 1):
                results.append(matching_keys)
                break

    return results


def format_chord_results(state: GlobalState, chordResults: List[List[KeyCode]]) -> str:
    chordmsg = ""

    for i in range(0, len(chordResults)):
        chordResult: List[KeyCode] = chordResults[i]
        keycode: KeyCode

        for j in range(0, len(chordResult)):
            keycode = chordResult[j]
            chordmsg += get_key_str(keycode)

            if j < (len(chordResult) - 1):
                chordmsg += "-"

        chordmsg += " [{0}]".format(state.chordResult_to_message(chordResult))

        if i < (len(chordResults) - 1):
            chordmsg += ','

    return chordmsg


def process_key_combos(state: GlobalState) -> List[Tuple[str, str]]:
    """Detect held-key combinations like CTRL-X or S-K.

    Returns a list of (combo_str, value) tuples for each matching combination.
    """
    results: List[Tuple[str, str]] = []

    for combo_str, combo_value in state.current_keymap_combinations_map().items():
        parts = [p.upper() for p in combo_str.split('-')]
        if len(parts) < 2:
            continue

        held_parts = parts[:-1]
        trigger_part = parts[-1]

        current_key_str = get_key_str(state.get_key())
        if current_key_str != trigger_part:
            continue

        if all(is_key_str_pressed(state, h) for h in held_parts):
            results.append((combo_str, combo_value))

    return results


def format_combo_results(comboResults: List[Tuple[str, str]]) -> str:
    if not comboResults:
        return ""
    return ', '.join('{} = {}'.format(k, v) for k, v in comboResults)


# ---------------------------------------------------------------------------
# Macros
# ---------------------------------------------------------------------------

_macro_controller: Optional[pynput.keyboard.Controller] = None


def _get_macro_controller() -> pynput.keyboard.Controller:
    global _macro_controller
    if _macro_controller is None:
        _macro_controller = pynput.keyboard.Controller()
    return _macro_controller


def _parse_macro_inputs(inputs_str: str):
    """Yield ('delay', float) or ('key', str) tuples from a macro input string."""
    for token in inputs_str.split():
        try:
            yield ('delay', float(token))
        except ValueError:
            yield ('key', token)


def _run_macro(inputs_str: str) -> None:
    """Execute a macro input sequence (runs in a thread)."""
    controller = _get_macro_controller()
    for kind, value in _parse_macro_inputs(inputs_str):
        if kind == 'delay':
            time.sleep(value)
        else:
            try:
                key = KeyCode.from_char(value.lower())
                controller.press(key)
                controller.release(key)
            except Exception as e:
                print(f"Macro key error for '{value}': {e}")


def process_macros(state: GlobalState) -> List[str]:
    """Detect macro triggers and execute matching macros.

    Returns names of triggered macros.
    """
    triggered: List[str] = []

    for macro_item in state.current_keymap_macros():
        for name, macro_def in macro_item.items():
            trigger = macro_def.get('trigger', {})
            inputs = macro_def.get('inputs', '')

            if trigger.get('type') != 'combination':
                continue

            sequence = trigger.get('sequence', '')
            parts = [p.upper() for p in sequence.split()]
            if not parts:
                continue

            trigger_part = parts[-1]
            held_parts = parts[:-1]

            if get_key_str(state.get_key()) != trigger_part:
                continue

            if all(is_key_str_pressed(state, h) for h in held_parts):
                triggered.append(name)
                threading.Thread(target=_run_macro, args=(inputs,), daemon=True).start()

    return triggered


def should_quit(key, state):
    try:
        if key == Key.__getitem__(state.quit_key):
            return True
    except KeyError:
        print("WARN:    quit_key '{}' is invalid".format(state.quit_key))

    return False
