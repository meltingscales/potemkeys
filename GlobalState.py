from shutil import which
from typing import Dict, List, Set, Union

from mergedeep import mergedeep, merge
from pynput.keyboard import Key, KeyCode

from Utils import resource_path, not_windows


class GlobalState:
    def __init__(self, options: dict) -> None:
        self.optionsJson: dict = options
        self.keymap: Dict[str, Dict[str, str]] = None
        self.keymap_is_chosen = False
        self.key_log: List[Key] = []
        self.message_array_log: List[List[str]] = self.optionsJson['default_messages']
        self.quit_key = self.optionsJson['quit_key']
        self.repeats: int = 0
        self.title: str = \
            self.optionsJson.get('title')
        self.icon_path: str = resource_path(self.optionsJson.get('icon_path'))
        self.running: bool = True
        self.required_linux_tools = {
            'xdotool': 'apt install xdotool',
            'wmctrl': 'apt install wmctrl',
        }

        self.currently_pressed_keys: Set[Key] = set()

        self.process_keymap_inherits()

    def process_keymap_inherits(self):
        """Processing "inherit" value for keymaps/other attributes..."""
        name: str
        keymap: Dict[str, str]
        for name, keymap in self.get_all_keymaps().items():
            if 'inherit' in keymap.keys():

                inheritFrom: str = keymap['inherit']

                print("[i] Processing keymap inherit -- {:20s} <= {:20s}".format(name, inheritFrom))

                if inheritFrom in self.get_all_keymaps():
                    merge(
                        self.get_all_keymaps()[name],
                        self.get_all_keymaps()[inheritFrom],
                        strategy=mergedeep.Strategy.TYPESAFE_ADDITIVE
                    )
                else:
                    raise KeyError("You have specified a keymap that does not exist: {}".format(inheritFrom))

    def choose_keymap(self, name: str):
        if name in self.get_all_keymaps().keys():
            self.keymap_is_chosen = True
            self.keymap = self.get_all_keymaps()[name]
        else:
            raise ValueError("No keymap called {}!".format(name))
        return self.keymap

    def current_keymap(self) -> Dict[str, Dict[str, str]]:
        return self.keymap

    def get_all_keymaps(self) -> Dict[str, Union[dict, str]]:
        return self.optionsJson.get('keymaps', dict())

    def set_all_keymaps(self, d: dict) -> Dict[str, str]:
        self.optionsJson['keymaps'] = d

        return self.get_all_keymaps()

    def current_keymap_keys_map(self) -> Dict[str, str]:
        return self.keymap.get('keys', dict())

    def current_keymap_chords_map(self) -> Dict[str, str]:
        return self.keymap.get('chords', dict())

    def current_keymap_combinations_map(self) -> Dict[str, str]:
        return self.keymap.get('combinations', dict())

    def current_keymap_mapped_keys(self) -> List[str]:
        return list(self.current_keymap_keys_map().keys())

    def current_keymap_mapped_chords(self) -> List[str]:
        return list(self.current_keymap_chords_map().keys())

    def current_keymap_mapped_combinations(self) -> List[str]:
        return list(self.current_keymap_combinations_map().keys())

    def chordResult_to_message(self, chordResult: List[KeyCode]) -> str:
        key: str = ' '.join(x.char.upper() for x in chordResult)

        return self.current_keymap_chords_map()[key]

    def enforce_linux_x11_dependencies(self):

        if not_windows():

            # os.environ['DISPLAY'] = ':0'
            # print(os.environ['DISPLAY'])

            for toolname in self.required_linux_tools.keys():
                packagename = self.required_linux_tools[toolname]
                if not which(toolname):
                    errormsg = (
                        ("Executable '{}' is missing. \n"
                         "Please install the package by running '{}'.").format(
                            toolname, packagename))
                    input(errormsg)
                    raise FileNotFoundError(errormsg)

    def is_key_pressed(self, k: Key):
        return k in self.currently_pressed_keys

    def get_all_pressed_keys(self) -> Set[Key]:
        return self.currently_pressed_keys

    def press_key(self, k: Key):
        """Log that a key was pressed."""
        self.add_key(k)
        self.currently_pressed_keys.add(k)

    def release_key(self, k: Key):
        """Log that a key was released."""
        try:
            self.currently_pressed_keys.remove(k)
        except KeyError as ke:
            print(
                """ERROR: Probably a threading issue ;_;"
Failed to 'release' this key because it was already released: {}
Stack trace:"
""".format(k))
            print(ke)

    def add_key(self, k: Key):
        """Log that a key was pressed."""
        self.key_log.append(k)

    def get_key(self, i=-1) -> Key:
        """Get a key that was pressed. Defaults to most recent."""
        return self.key_log[i]

    def clear_key_log(self) -> None:
        self.key_log = list()

    def key_log_length(self) -> int:
        return len(self.key_log)

    def add_message(self, m: str, i=0):
        # ensure log is large enough
        while i >= len(self.message_array_log):
            self.message_array_log.append(list())

        self.message_array_log[i].append(m)

    def blank_message_log(self):
        for i in range(0, len(self.message_array_log)):
            self.add_message("", i)

    def get_message(self, j=-1, i=0) -> str:
        return self.message_array_log[i][j]

    def get_message_log(self, i=0) -> List[str]:
        return self.message_array_log[i]

