import pytest

from potemkeys.config import Options
from potemkeys.engine import Engine


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


@pytest.fixture
def options():
    return Options.from_dict({
        'input_history_length': 4,
        'chord_window_ms': 400,
        'keymaps': {
            'GG': {
                'keys': {'A': '[←] Left', 'D': '[→] Right', 'K': '[HS] HSlash', 'S': '[↓] Crouch'},
                'chords': {'A A': 'dash'},
                'combinations': {'S-K': '[2H] cHS'},
                'macros': [{'buster': {'inputs': 'A D', 'trigger': 'ALT D'}}],
            },
            'Tekken': {'keys': {'U': '[1] LP'}},
        },
    })


@pytest.fixture
def make_engine(options):
    def _make(**kw):
        clock = FakeClock()
        ran = []
        eng = Engine(options, run_macro=ran.append, clock=clock, **kw)
        return eng, clock, ran
    return _make


def test_starts_in_menu_and_selects_by_key(make_engine):
    eng, _, _ = make_engine()
    assert eng.in_menu
    assert eng.lines[1:] == ['  [1] GG', '  [2] Tekken']
    eng.on_press('x')
    assert eng.in_menu
    eng.on_press('2')
    assert eng.keymap.name == 'Tekken'
    assert eng.lines[0] == 'Input: -'


def test_default_keymap_skips_menu(options):
    options.default_keymap = 'GG'
    assert Engine(options).keymap.name == 'GG'
    options.default_keymap = 'nope'
    with pytest.raises(KeyError):
        Engine(options)


def test_menu_key_returns_to_menu(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('1')
    eng.on_press('A')
    eng.on_press('F1')
    assert eng.in_menu
    assert not eng.history


def test_press_shows_mapping_and_history(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('1')
    eng.on_press('a')
    assert eng.lines[0] == 'Input: A = [←] Left'
    eng.on_press('K')
    assert eng.lines[0] == 'Input: [←]  |  K = [HS] HSlash'
    eng.on_press('Z')
    assert eng.lines[0] == 'Input: [←] [HS]  |  Z = ?'


def test_history_is_bounded(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('1')
    for k in 'ADADAD':
        eng.on_press(k)
    assert len(eng.history) == 4
    assert eng.lines[0] == 'Input: [←] [→] [←]  |  D = [→] Right'


def test_repeat_counter(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('1')
    eng.on_press('K'); eng.on_press('K'); eng.on_press('K')
    assert eng.lines[0].endswith('K = [HS] HSlash (x3)')
    eng.on_press('A')
    assert '(x' not in eng.lines[0]


def test_chord_respects_time_window(make_engine):
    eng, clock, _ = make_engine()
    eng.on_press('1')
    eng.on_press('A')
    clock.t += 0.2
    eng.on_press('A')
    assert eng.lines[1] == 'Chord: A-A = dash'
    clock.t += 1.0
    eng.on_press('A')
    assert eng.lines[1] == 'Chord: -'


def test_combo_needs_held_key(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('1')
    eng.on_press('S')
    eng.on_press('K')
    assert eng.lines[2] == 'Combo: S-K = [2H] cHS'
    eng.on_release('S')
    eng.on_press('K')
    assert eng.lines[2] == 'Combo: -'


def test_macro_runs_once_and_ignores_injected(make_engine):
    eng, _, ran = make_engine()
    eng.on_press('1')
    eng.on_press('ALT')
    eng.on_press('D')
    assert ran == ['A D']
    assert eng.lines[3] == 'Macro: buster'
    eng.on_press('D', injected=True)
    assert ran == ['A D']
    assert eng.lines[3] == 'Macro: -'


def test_quit_key_on_release(make_engine):
    eng, _, _ = make_engine()
    eng.on_press('ESC')
    assert not eng.quit_requested
    eng.on_release('ESC')
    assert eng.quit_requested
