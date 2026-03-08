#!/usr/bin/env bash

platform='unknown'
unamestr=$(uname)
if [[ "$unamestr" == 'Linux' ]]; then
  platform='linux'
elif [[ "$unamestr" == 'FreeBSD' ]]; then
  platform='freebsd'
elif [[ "$unamestr" == 'Darwin' ]]; then
  platform='darwin'
fi

echo "Make sure uv exists..."

if ! which uv > /dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source "$HOME/.local/bin/env"
fi

if [[ $platform == 'linux' ]]; then
  echo "Making sure required tools are installed."
  sudo apt-get install -y wmctrl
else
  echo "Not Linux, maybe OSX? Cannot install xdotool or wmctrl. Skipping."
fi

uv sync --group dev
