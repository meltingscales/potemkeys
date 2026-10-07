"""Entry point: wires the keyboard listener, the engine and the pygame window."""
from __future__ import annotations

import argparse
import queue
import sys
from typing import List, Tuple

import pygame

from potemkeys import __version__
from potemkeys.config import Options, candidate_option_paths, load_options, resource_path
from potemkeys.engine import Engine
from potemkeys.keys import Event, run_macro, start_listener

FPS = 60


def parse_args(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog='potemkeys', description='On-screen keyboard-to-button map for fighting games.')
    p.add_argument('-c', '--config', help='path to potemkeysoptions.jsonc (default: search cwd, exe dir, bundle)')
    p.add_argument('-k', '--keymap', help='keymap name to start with (skips the menu)')
    p.add_argument('--list-keymaps', action='store_true', help='print keymap names and exit')
    p.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    return p.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        options = load_options(args.config)
    except (FileNotFoundError, ValueError, KeyError) as e:
        print(f'error: {e}', file=sys.stderr)
        return 2
    print(f'[config] {options.path}')
    print('[config] searched: ' + ', '.join(str(p) for p in candidate_option_paths()))

    if args.list_keymaps:
        print('\n'.join(options.keymaps))
        return 0
    if args.keymap:
        options.default_keymap = args.keymap

    try:
        engine = Engine(options, run_macro=run_macro)
    except KeyError as e:
        print(f'error: {e}', file=sys.stderr)
        return 2

    events: 'queue.Queue[Event]' = queue.Queue()
    listener = start_listener(events)
    try:
        run_window(options, engine, events)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
    return 0


def run_window(options: Options, engine: Engine, events: 'queue.Queue[Event]') -> None:
    pygame.init()
    window = pygame.Window(options.title, (options.window_width, options.window_height),
                           resizable=True, always_on_top=options.window_always_on_top)
    icon = resource_path(options.icon_path)
    if icon.is_file():
        window.set_icon(pygame.image.load(str(icon)))
    font = load_font(options)
    clock = pygame.time.Clock()

    while not engine.quit_requested:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                engine.quit_requested = True
        drain_events(engine, events)
        render_frame(window.get_surface(), font, options, engine)
        window.flip()
        clock.tick(FPS)

    pygame.quit()


def load_font(options: Options):
    """Bundled TTF (has the arrow glyphs everywhere) unless disabled, else a system font."""
    if options.font_file:
        path = resource_path(options.font_file)
        if path.is_file():
            return pygame.font.Font(str(path), options.font_size)
        print(f'[font] {path} not found, falling back to system font {options.font_type!r}')
    return pygame.font.SysFont(options.font_type, options.font_size)


def render_frame(surface, font, options: Options, engine: Engine) -> None:
    line_h = font.get_linesize() + options.font_margin
    surface.fill(options.background_color)
    width = surface.get_width()
    y = options.font_margin
    for line in engine.lines:
        draw_text(surface, font, line, options.text_color, y, width, options.center_text)
        y += line_h

    if options.show_cheat_sheet and engine.keymap is not None:
        y += line_h // 2
        pygame.draw.line(surface, options.dim_color, (0, y), (width, y))
        y += line_h // 2
        draw_cheat_sheet(surface, font, options, engine, y, width, line_h)


def drain_events(engine: Engine, events: 'queue.Queue[Event]') -> None:
    while True:
        try:
            kind, key, injected = events.get_nowait()
        except queue.Empty:
            return
        if kind == 'press':
            engine.on_press(key, injected)
        else:
            engine.on_release(key, injected)


def draw_text(surface, font, text: str, color, y: int, width: int, center: bool) -> None:
    if not text:
        return
    img = font.render(text, True, color)
    x = (width - img.get_width()) // 2 if center else 8
    surface.blit(img, (x, y))


def draw_cheat_sheet(surface, font, options: Options, engine: Engine, y: int, width: int, line_h: int) -> None:
    """Every mapped key in columns; keys currently held are highlighted."""
    entries: List[Tuple[str, str]] = [(k, kd.short + ' ' + kd.description if kd.notation else kd.description)
                                      for k, kd in engine.keymap.keys.items()]
    if not entries:
        return
    labels = [f'{k:>5} {desc}' for k, desc in entries]
    col_w = max(font.size(label)[0] for label in labels) + 3 * font.size(' ')[0]
    cols = max(1, (width - 8) // col_w)
    for i, ((key, _), label) in enumerate(zip(entries, labels)):
        held = key in engine.held
        color = options.highlight_color if held else options.dim_color
        img = font.render(label, True, color)
        x = 8 + (i % cols) * col_w
        row_y = y + (i // cols) * line_h
        if held:
            pad = 2
            pygame.draw.rect(surface, options.highlight_color,
                             (x - pad, row_y - pad, img.get_width() + 2 * pad, img.get_height() + 2 * pad), 1)
        surface.blit(img, (x, row_y))


if __name__ == '__main__':
    sys.exit(main())
