#!/usr/bin/env bash

echo "Make sure pipenv exists..."

which pipenv
# if exit code is nonzero, it is not a command.
if [ "$?" -eq "1" ]; then
  python -m pip install pipenv
fi

echo "Making sure required tools are installed."
sudo apt-get install xdotool wmctrl

pipenv install
pipenv run python FGfFwK.py

echo "Done."