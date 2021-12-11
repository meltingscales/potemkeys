echo "Make sure pipenv exists..."
WHERE pipenv
IF %ERRORLEVEL% NEQ 0 python -m pip install pipenv

python3 -m pipenv install --dev