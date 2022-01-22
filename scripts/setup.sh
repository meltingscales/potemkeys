#!/usr/bin/env bash

echo "Make sure poetry exists..."

which poetry
# if exit code is nonzero, it is not a command.
if [ "$?" -eq "1" ]; then
  python -m pip install poetry
fi

echo "Making sure required tools are installed."
sudo apt-get install -y xdotool wmctrl

poetry install

python3 -m poetry install --dev