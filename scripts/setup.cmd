echo "Make sure poetry exists..."
WHERE poetry
IF %ERRORLEVEL% NEQ 0 python -m pip install poetry

python3 -m poetry install --dev