#!/usr/bin/env python

# links that make me want to `git commit -m 'fortnite battle royale'`
# https://stackoverflow.com/questions/25381589/pygame-set-window-on-top-without-changing-its-position

from typing import List

from pynput.keyboard import Key, KeyCode

from potemkeys.GlobalState import GlobalState


def is_modifier_key(k: Key):
    try:
        _ = k.char
        return False
    except AttributeError:
        return True




class KeyEvent:
    def __init__(self) -> None:
        raise Exception("lol todo :p")


def prompt_choose_keymap(state) -> None:
    """Returns true if a user picks a keymap successfully."""
    print("Keymap is not chosen yet! Asking them to choose...")

    state.add_message("[{:^10s}] Choose a keymap:".format(str(state.get_key())))
    all_keymap_names = list(state.get_all_keymaps().keys())

    i = 0
    for keymapname in all_keymap_names:
        state.add_message("[{}]: {}".format(i, keymapname), i + 1)
        i += 1

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

                state.add_message("Current keymap:  {}".format(
                    chosen_keymap_name
                ), mi)
                mi += 1

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

                # clear the key log, they've chosen
                state.clear_key_log()

                return

        except ValueError:
            pass

    # not successful
    return


def process_mashing(state: GlobalState) -> str:
    """Return a status string if mashing is detected."""
    if state.key_log_length() >= 2:
        # if they've pressed at least 2 keys

        prev_key = state.get_key(-2)

        if prev_key == state.get_key():
            # they mashin', show it
            state.repeats += 1
            return f' (x{state.repeats})'
        else:
            # not mashin', reset
            state.repeats = 1

    return ""


def process_key_press(state: GlobalState, msg: str = "") -> str:
    if not is_modifier_key(state.get_key()):
        key_char = state.get_key().char
        normalized_key_char = key_char.upper()

        print('alphanumeric key {0} pressed'.format(key_char))
        msg += "{}".format(key_char)

        if normalized_key_char in state.current_keymap_mapped_keys():
            msg += ' = {:2s}'.format(
                state.current_keymap_keys_map()[normalized_key_char])
        else:
            msg += ' = ?'

        # print("pressed {} keys".format(state.total_keys_pressed()))

        msg += process_mashing(state)

    else:
        print('special key {0} pressed'.format(state.get_key()))

    return msg


def process_key_chords(state: GlobalState) -> List[List[KeyCode]]:
    results: List[List[KeyCode]] = []

    # for all chords patterns,
    for chord_str in state.current_keymap_chords_map():

        splitchord: List[str] = chord_str.split(' ')
        splitchord = [s.upper() for s in splitchord]

        chordlen = len(splitchord)

        # too short
        if chordlen > state.key_log_length():
            break  # on to next chord

        key_log_slice = []

        for i in range(state.key_log_length() - 1, -1, -1):
            key_log_slice.append(state.get_key(i))
            # print("i={},key={}".format(i, key_log_slice[-1]))
            if len(key_log_slice) >= chordlen:
                break

        key_log_slice.reverse()

        # print("Looking for {} aka {}".format(chord_str,splitchord))
        # print("Inside of {}".format(key_log_slice))

        matching_keys: List[Key] = []
        # for all keys in the chord,
        for i in range(0, len(splitchord)):
            # print('i=           {}'.format(i))

            currentKey = key_log_slice[i]
            current_chord_member = splitchord[i]
            currentKeyCharCode: str = None
            if not is_modifier_key(currentKey):
                currentKeyCharCode = currentKey.char.upper()
            else:
                break  # on to next chord... TODO, NYI for modifiers...
            # print('looking for {}'.format(i))
            #
            # print('current_chord_member={}'.format(current_chord_member))
            # print('current_key_pressed= {}'.format(currentKeyCharCode))

            if not (current_chord_member.upper() == currentKeyCharCode.upper()):
                break  # on to next chord... Not a full chord
            else:
                matching_keys.append(currentKey)

            if i == (len(splitchord) - 1):
                # if we're at the end of the chord,

                results.append(matching_keys)
                break  # not necessary but more readable

    # print("Returning {}".format(results))
    return results


def format_chord_results(state: GlobalState, chordResults: List[List[KeyCode]]) -> str:
    chordmsg = ""

    for i in range(0, len(chordResults)):
        chordResult: List[KeyCode] = chordResults[i]
        keycode: KeyCode

        for j in range(0, len(chordResult)):
            keycode = chordResult[j]
            chordmsg += keycode.char

            if j < (len(chordResult) - 1):
                chordmsg += "-"

        chordmsg += " [{0}]".format(state.chordResult_to_message(chordResult))

        if i < (len(chordResults) - 1):
            chordmsg += ','

    return chordmsg


def process_key_combos(state: GlobalState):
    pass



def should_quit(key, state):
    try:
        if key == Key.__getitem__(state.quit_key):  # TODO is this a security risk? __getitem__ with user input?
            return True
    except KeyError:  # Means no key called state.quit_key exists...
        print("WARN:    quit_key '{}' is invalid".format(state.quit_key))

    return False

