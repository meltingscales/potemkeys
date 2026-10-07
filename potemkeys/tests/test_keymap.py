import pytest

from potemkeys.keymap import Keymap, KeyDisplay, parse_key_display, resolve_inherits, split_combo


@pytest.mark.parametrize('raw, expected', [
    ('[HS]  HSlash', KeyDisplay('[HS]', None, 'HSlash', None)),
    ('[HS] (p) foo [bar]', KeyDisplay('[HS]', '(p)', 'foo', '[bar]')),
    ('[1] (X) Left Punch', KeyDisplay('[1]', '(X)', 'Left Punch', None)),
    ('Start', KeyDisplay('', None, 'Start', None)),
    ('[Pause]', KeyDisplay('[Pause]', None, '', None)),
])
def test_parse_key_display(raw, expected):
    assert parse_key_display(raw) == expected


def test_key_display_str_and_short():
    kd = parse_key_display('[HS] (p) foo [bar]')
    assert str(kd) == '[HS] (p) foo [bar]'
    assert kd.short == '[HS]'
    assert parse_key_display('Start').short == 'Start'


@pytest.mark.parametrize('raw, expected', [
    ('CTRL-X', ['CTRL', 'X']),
    ('ALT D', ['ALT', 'D']),
    ('s-k', ['S', 'K']),
    ('-', ['-']),
])
def test_split_combo(raw, expected):
    assert split_combo(raw) == expected


@pytest.fixture
def ggs():
    return Keymap.from_dict('GG', {
        'keys': {'a': '[←] Left', 'K': '[HS] HSlash'},
        'chords': {'A A': 'dash', 'S W': 'super jump'},
        'combinations': {'S-K': '[2H] crouching HS', 'CTRL-X': 'cut'},
        'macros': [{'buster': {'inputs': 'A 0.1 D', 'trigger': {'type': 'combination', 'sequence': 'ALT D'}}}],
    })


def test_keys_are_uppercased(ggs):
    assert ggs.describe('a').notation == '[←]'
    assert ggs.describe('A') is ggs.describe('a')
    assert ggs.describe('Z') is None


def test_matching_chords_uses_history_tail(ggs):
    assert ggs.matching_chords(['D', 'A', 'A']) == [(('A', 'A'), 'dash')]
    assert ggs.matching_chords(['A']) == []
    assert ggs.matching_chords(['S', 'W']) == [(('S', 'W'), 'super jump')]


def test_matching_combos_requires_held_keys(ggs):
    assert ggs.matching_combos('K', {'S', 'K'}) == [(('S', 'K'), '[2H] crouching HS')]
    assert ggs.matching_combos('K', {'K'}) == []
    assert ggs.matching_combos('S', {'S', 'K'}) == []


def test_macros_parse_and_trigger(ggs):
    (m,) = ggs.macros
    assert (m.name, m.inputs, m.held, m.trigger) == ('buster', 'A 0.1 D', ('ALT',), 'D')
    assert ggs.triggered_macros('D', {'ALT', 'D'}) == [m]
    assert ggs.triggered_macros('D', {'D'}) == []


def test_macros_accept_dict_and_string_trigger():
    km = Keymap.from_dict('x', {'macros': {'m': {'inputs': 'A', 'trigger': 'CTRL-A'}}})
    assert km.macros[0].held == ('CTRL',)
    assert km.macros[0].trigger == 'A'


def test_resolve_inherits_merges_child_over_parent():
    raw = {
        'base': {'keys': {'A': 'left', 'B': 'b'}, 'chords': {'A A': 'dash'},
                 'macros': [{'m1': {'inputs': 'A', 'trigger': 'ALT A'}}]},
        'child': {'inherit': 'base', 'keys': {'B': 'override', 'C': 'c'},
                  'macros': [{'m2': {'inputs': 'B', 'trigger': 'ALT B'}}]},
        'grandchild': {'inherit': 'child', 'keys': {'D': 'd'}},
    }
    out = resolve_inherits(raw)
    assert out['child']['keys'] == {'A': 'left', 'B': 'override', 'C': 'c'}
    assert out['child']['chords'] == {'A A': 'dash'}
    assert [list(m)[0] for m in out['child']['macros']] == ['m1', 'm2']
    assert out['grandchild']['keys'] == {'A': 'left', 'B': 'override', 'C': 'c', 'D': 'd'}
    assert 'inherit' not in out['grandchild']
    assert out['base'] == raw['base']


def test_resolve_inherits_errors():
    with pytest.raises(KeyError):
        resolve_inherits({'a': {'inherit': 'nope'}})
    with pytest.raises(ValueError):
        resolve_inherits({'a': {'inherit': 'b'}, 'b': {'inherit': 'a'}})
