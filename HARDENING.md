<!-- markdownlint-disable -->

# Hardening Report: matrix-org--setup-python-poetry/v2.0.0

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **matrix-org--setup-python-poetry/v2.0.0** was hardened automatically. 3 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

These composite action steps reference actions by a mutable tag instead of a full 40-character commit SHA: 'uses: actions/setup-python@v4' (line 51), 'uses: actions/cache@v3' (line 74) and 'uses: actions/cache@v3' (line 95).

Locations:

- `action.yml:51`
- `action.yml:74`
- `action.yml:95`

### script-injection (severity: high)

Sub-rule (a): a GitHub expression is placed directly inside a run: script in the 'Install poetry from scratch' step: 'run: python -m pip install --user poetry==${{ inputs.poetry-version }}'. Whoever calls the action controls inputs.poetry-version and can inject shell commands. Fix: pass it through an env var (e.g. POETRY_VERSION) and use "poetry==$POETRY_VERSION" with double quotes.

Locations:

- `action.yml:81`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.poetry-version }}" appears directly in run: block of step "Install poetry from scratch"; move to env: map

Locations:

- `action.yml:82`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python@v4 to commit 7f4fc3e22c37d6ff65e88745f38bd3157c663f7c and both actions/cache@v3 references to commit 6f8efc29b200d32929f49075959781ed54ec270c, keeping the tag in a trailing comment. In the 'Install poetry from scratch' step, inputs.poetry-version now goes through the POETRY_VERSION env var and is used as "poetry==$POETRY_VERSION".

### Iteration 2

**Fixes applied:** script-injection, static-inline-injection

**Notes:**

Moved inputs.poetry-version into the env var POETRY_VERSION in the 'Install poetry from scratch' step. The command now runs: python -m pip install --user "poetry==$POETRY_VERSION".

