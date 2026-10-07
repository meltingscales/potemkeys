import os

# pynput needs a display on Linux; the dummy backend lets key_to_str tests run headless.
os.environ.setdefault('PYNPUT_BACKEND', 'dummy')
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
