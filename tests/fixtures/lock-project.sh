#!/usr/bin/env bash
# Generate a poetry.lock for the given project directory using an isolated
# poetry install (so it does not pollute ~/.local, which the action caches).
set -euo pipefail
PROJECT_DIR="$1"
POETRY_VERSION="${2:-2.1.1}"
VENV=/tmp/lock-poetry-venv

if [ ! -x "$VENV/bin/poetry" ]; then
  if python3 -m venv "$VENV" 2>/dev/null && [ -x "$VENV/bin/pip" ]; then
    "$VENV/bin/pip" install -q "poetry==$POETRY_VERSION"
  else
    rm -rf "$VENV"
    python3 -m venv --without-pip "$VENV" 2>/dev/null || python3 -m virtualenv "$VENV"
    if [ ! -x "$VENV/bin/pip" ]; then
      curl -sSfL https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
      "$VENV/bin/python" /tmp/get-pip.py -q
    fi
    "$VENV/bin/python" -m pip install -q "poetry==$POETRY_VERSION"
  fi
fi

cd "$PROJECT_DIR"
rm -f poetry.lock
"$VENV/bin/poetry" lock --no-interaction
test -f poetry.lock
echo "Generated $PROJECT_DIR/poetry.lock"
