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

echo "Make sure poetry exists..."

which poetry
# if exit code is nonzero, it is not a command.
if [ "$?" -eq "1" ]; then
  python3 -m pip install poetry
fi

if [[ $platform == 'linux' ]]; then
  echo "Making sure required tools are installed."
  sudo apt-get install -y xdotool wmctrl
else
  echo "Not Linux, maybe OSX? Cannot install xdotool or wmctrl. Skipping."
fi

poetry install

python3 -m poetry install
