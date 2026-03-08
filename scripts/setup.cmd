echo "Make sure uv exists..."
WHERE uv
IF %ERRORLEVEL% NEQ 0 (
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
)

uv sync --group dev
