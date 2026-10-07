import enum

from pynput.keyboard import Key, KeyCode


# pynput's dummy backend aliases every Key member to the same value, so use our own enum for names.
class FakeKey(enum.Enum):
    ctrl_l = 1
    shift_r = 2
    esc = 3
    f1 = 4

from potemkeys.keys import key_to_str, parse_macro, token_to_key


def test_key_to_str():
    assert key_to_str(KeyCode.from_char('a')) == 'A'
    assert key_to_str(KeyCode.from_char(';')) == ';'
    assert key_to_str(KeyCode.from_char('\x18')) == 'X'     # ctrl+x
    assert key_to_str(KeyCode.from_vk(0x41)) == 'A'           # no char, letter vk
    assert key_to_str(KeyCode.from_vk(0x70)) == 'P'           # lowercase keysym
    assert key_to_str(KeyCode.from_vk(999)) == 'VK999'
    assert key_to_str(FakeKey.ctrl_l) == 'CTRL'
    assert key_to_str(FakeKey.shift_r) == 'SHIFT'
    assert key_to_str(FakeKey.esc) == 'ESC'
    assert key_to_str(FakeKey.f1) == 'F1'
    assert key_to_str(None) is None


def test_parse_macro():
    assert parse_macro('A 0.1 S+J') == [('keys', ['A']), ('delay', 0.1), ('keys', ['S', 'J'])]


def test_token_to_key():
    assert token_to_key('a') == KeyCode.from_char('a')
    assert token_to_key('CTRL') == Key.ctrl
    assert token_to_key('f1') == Key.f1
