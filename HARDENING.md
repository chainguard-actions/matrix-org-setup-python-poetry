<!-- markdownlint-disable -->

# Hardening Report: matrix-org--setup-python-poetry/v1.2.4

> This file was generated automatically by the hardening agent.

**Policy SHA:** `d636be7e43ef829af6e853da6b3c7566db9f72fe`

**Test Policy SHA:** `843adf9e4b8f85d0c08b27b9d0b09dd094b54702`

**Harden Agent Version:** `2`

Action **matrix-org--setup-python-poetry/v1.2.4** was hardened automatically. 8 finding(s) were identified and resolved across 3 iteration(s).

## Findings Fixed

### unpinned-uses (severity: high)

Composite action steps reference actions by mutable tags instead of 40-char commit SHAs: 'uses: actions/setup-python@v4' (line 41), 'uses: actions/cache@v3' (line 64), 'uses: actions/cache@v3' (line 84).

Locations:

- `action.yml:41`
- `action.yml:64`
- `action.yml:84`

### script-injection (severity: high)

Sub-rule (a): expression interpolated directly in run block of step 'Install poetry from scratch': `run: python -m pip install --user poetry==${{ inputs.poetry-version }}`. Should route via env var and quote ("poetry==$POETRY_VERSION").

Locations:

- `action.yml:71`

### script-injection (severity: high)

Sub-rule (a): expression interpolated directly in run block of step 'Install project (no extras or groups)': `run: poetry install -vv --no-interaction ${{ inputs.install-project != 'true' && '--no-root' || '' }}`.

Locations:

- `action.yml:111`

### script-injection (severity: high)

Sub-rule (a): attacker-controllable inputs interpolated directly in run block of step 'Install project with --extras...': `run: poetry install -vv --no-interaction ${{ inputs.extras != '' && format('--extras="{0}"', inputs.extras) || '' }} --with="${{ inputs.groups }}" ${{ inputs.install-project != 'true' && '--no-root' || '' }}`. inputs.extras and inputs.groups can break out of the quotes and inject shell commands.

Locations:

- `action.yml:118`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.poetry-version }}" appears directly in run: block of step "Install poetry from scratch"; move to env: map

Locations:

- `action.yml:73`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.install-project != 'true' && '--no-root' || '' }}" appears directly in run: block of step "Install project (no extras or groups)"; move to env: map

Locations:

- `action.yml:112`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.groups }}" appears directly in run: block of step "Install project with --extras=${{ inputs.extras }} --with=${{ inputs.groups }}"; move to env: map

Locations:

- `action.yml:119`

### static-inline-injection (severity: high)

shell injection: expression "${{ inputs.install-project != 'true' && '--no-root' || '' }}" appears directly in run: block of step "Install project with --extras=${{ inputs.extras }} --with=${{ inputs.groups }}"; move to env: map

Locations:

- `action.yml:119`

## Iteration Notes

### Iteration 1

**Fixes applied:** unpinned-uses, script-injection, static-inline-injection

**Notes:**

Pinned actions/setup-python@v4 and both actions/cache@v3 uses to full SHAs. Moved poetry-version, install-project, extras, groups into env vars; install commands now build args with a bash array, keeping upstream semantics (--extras="..." and --with="..." as single args, --no-root when install-project != 'true'). Avoided the bash special var GROUPS by naming it POETRY_GROUPS.

### Iteration 2

**Fixes applied:** unpinned-uses, invalid-yaml

**Notes:**

Fixed both findings in action.yml. I didn't run a YAML parser or act afterwards, so the next analysis pass is the real check.

- **unpinned-uses:** both `actions/cache@v3` references now point to commit `6f8efc29b200d32929f49075959781ed54ec270c`, with a `# v3` comment. I got the SHA from lookup_action_sha.
- **invalid-yaml:** an earlier pass had damaged the two "Install project" steps. Its `if:` line in the first step had been overwritten by `env:`, which caused the parse error. I restored that condition as `if: inputs.extras == '' && inputs.groups == ''`. This is my reconstruction of upstream's condition, not copied from upstream: it is the opposite of the next step's `extras != '' || groups != ''` check, so exactly one of the two steps runs. I also removed leftover text after the `poetry install` command in the second step (`l-project != 'true' && '--no-root' || '' }}`).

The earlier env-variable and argument-list hardening in those steps is unchanged.

### Iteration 3

**Fixes applied:** unpinned-uses

**Notes:**

Pinned both actions/cache@v3 references in action.yml to 6f8efc29b200d32929f49075959781ed54ec270c # v3 (resolved via lookup_action_sha).

