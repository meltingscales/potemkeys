@echo off
where uv >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing uv...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
)
uv sync --group dev
