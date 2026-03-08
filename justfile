default: run

setup:
    ./scripts/setup.sh

run:
    uv run python3 -m potemkeys

test:
    uv run pytest

build:
    uv build

exe:
    uv run pyinstaller ./potemkeys.spec

publish:
    uv publish

clean:
    rm -rf dist/ build/ __pycache__ .pytest_cache
