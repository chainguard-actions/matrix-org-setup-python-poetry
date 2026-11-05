<!-- markdownlint-disable -->

# Hardening Report: matrix-org--setup-python-poetry/v1.2.5

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **matrix-org--setup-python-poetry/v1.2.5** was hardened automatically. 8 finding(s) were identified and resolved across 2 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

The composite action's uses: lines point to version tags, not full 40-character commit SHAs: `uses: actions/setup-python@v4` (line 51), `uses: actions/cache@v3` (line 74) and `uses: actions/cache@v3` (line 95).

Locations:

- `action.yml:51`
- `action.yml:74`
- `action.yml:95`

### script-injection (severity: high)

Sub-rule (a): an expression is placed directly inside a run: script in step 'Install poetry from scratch': `run: python -m pip install --user poetry==${{ inputs.poetry-version }}`. Shell metacharacters in the poetry-version input would run as commands.

Locations:

- `action.yml:81`

### script-injection (severity: high)

Sub-rule (a): an expression is placed directly inside a run: script in step 'Install project (no extras or groups)': `run: poetry install -vv --no-interaction ${{ inputs.install-project != 'true' && '--no-root' || '' }}`. It reads from inputs.*.

Locations:

- `action.yml:121`

### script-injection (severity: high)

Sub-rule (a): expressions are placed directly inside a run: script in step 'Install project with --extras...': `run: poetry install -vv --no-interaction ${{ inputs.extras != '' && format('--extras="{0}"', inputs.extras) || '' }} --with="${{ inputs.groups }}" ${{ inputs.install-project != 'true' && '--no-root' || '' }}`. A crafted extras or groups input could break out of the quotes and inject commands.

Locations:

- `action.yml:128`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.poetry-version }}" appears directly in run: block of step "Install poetry from scratch"; move to env: map

Locations:

- `action.yml:82`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.install-project != 'true' && '--no-root' || '' }}" appears directly in run: block of step "Install project (no extras or groups)"; move to env: map

Locations:

- `action.yml:122`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.groups }}" appears directly in run: block of step "Install project with --extras=${{ inputs.extras }} --with=${{ inputs.groups }}"; move to env: map

Locations:

- `action.yml:129`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.install-project != 'true' && '--no-root' || '' }}" appears directly in run: block of step "Install project with --extras=${{ inputs.extras }} --with=${{ inputs.groups }}"; move to env: map

Locations:

- `action.yml:129`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python@v4 and actions/cache@v3 (both uses) to their full commit SHAs, keeping the tag as a comment. In the 'Install poetry from scratch' step, poetry-version now comes in through env as POETRY_VERSION and is used as "poetry==$POETRY_VERSION". In both 'Install project' steps, extras, groups and install-project now come in through env. Each run: builds a bash array that matches what upstream passed: --extras=<value> only when extras is set, kept as one argument as in upstream's quoted form; --with=<value> always passed, as upstream did; and --no-root when install-project is not 'true'. Nothing was run to test these changes.

### Iteration 2

**Fixes applied:** script-injection, invalid-yaml

**Notes:**

Repaired the corrupted 'Install project (no extras or groups)' step (restored if: inputs.extras == '' && inputs.groups == '', removed trailing garbage). Moved extras/groups/install-project into env in the extras step and built an args array preserving upstream semantics (--extras="<list>" and --with="<list>" as single args, --no-root when install-project != true).

