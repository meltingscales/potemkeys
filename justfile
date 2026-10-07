default: run

setup:
    ./scripts/setup.sh

run *ARGS:
    uv run python -m potemkeys {{ARGS}}

test:
    uv run pytest

build:
    uv build

exe:
    uv run pyinstaller ./potemkeys.spec

publish:
    uv publish

clean:
    rm -rf dist/ build/ .pytest_cache
    find . -name __pycache__ -type d -prune -exec rm -rf {} +
