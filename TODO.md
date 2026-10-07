# Ideas

- [ ] Per-keymap cheat sheet layout (rows that mirror the physical keyboard)
- [ ] Macro steps that hold a key for a duration (`S(0.2)`), not only tap/together
- [ ] Wayland always-on-top (no SDL/compositor protocol for it yet; XWayland works on most compositors)
- [ ] Gamepad input display alongside keyboard

# Done

- [x] choose keymap at startup, switch at runtime (F1)
- [x] capture CTRL/ALT/etc, including ctrl+letter on Windows
- [x] parse `[notation] (modifier) description [category]` from mapping values
- [x] macros triggered by key combinations
- [x] input history strip + live cheat sheet with held keys highlighted
- [x] chord time window
- [x] poetry -> uv, pygame -> pygame-ce, no more wmctrl / ctypes for always-on-top
