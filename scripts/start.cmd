echo "Make sure pipenv exists..."
WHERE pipenv
IF %ERRORLEVEL% NEQ 0 python -m pip install pipenv

pipenv install
pipenv run python FGfGwK.py

echo "Done."

PAUSE