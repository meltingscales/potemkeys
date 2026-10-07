from pathlib import Path

import pytest

from potemkeys import config
from potemkeys.config import Options, load_options

BUNDLED = Path(config.__file__).parent / config.OPTIONS_FILE_NAME


def test_bundled_options_load():
    opts = load_options(str(BUNDLED))
    assert opts.path == BUNDLED
    assert 'GG:S Default' in opts.keymaps
    custom = opts.keymaps['GG:S HenryFBP Custom (E+R=RC,PB)']
    assert custom.describe('E').notation == '[RC]'
    assert custom.describe('U').notation == '[P]'      # inherited
    assert custom.chords                                 # inherited
    assert custom.macros[0].trigger == 'D'


def test_defaults_and_normalization():
    opts = Options.from_dict({'quit_key': 'esc', 'text_color': [1, 2, 3], 'bogus': 1,
                              'keymaps': {'k': {'keys': {'a': 'x'}}}})
    assert opts.quit_key == 'ESC'
    assert opts.text_color == (1, 2, 3)
    assert opts.menu_key == 'F1'
    assert opts.input_history_length == 10


def test_no_keymaps_is_error():
    with pytest.raises(ValueError):
        Options.from_dict({})


def test_find_options_prefers_cwd(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert config.find_options_file() == BUNDLED
    local = tmp_path / config.OPTIONS_FILE_NAME
    local.write_text('{"keymaps": {"k": {"keys": {}}}}')
    assert config.find_options_file() == local
    with pytest.raises(FileNotFoundError):
        config.find_options_file('/nonexistent/file.jsonc')
