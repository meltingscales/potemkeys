#!/usr/bin/env bash

echo "Make sure pipenv exists..."

which pipenv
# if exit code is nonzero, it is not a command.
if [ "$?" -eq "1" ]; then
  python -m pip install pipenv
fi

pipenv install
pipenv run python main.py

echo "Done."