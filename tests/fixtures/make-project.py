#!/usr/bin/env python3
"""Create a minimal Poetry project (no dependencies) with a matching poetry.lock.

Usage: make-project.py DIR [--group NAME ...] [--no-lock]

The content-hash is computed the same way Poetry 1.x does:
sha256(json.dumps(relevant_content, sort_keys=True)) where relevant_content
contains the legacy keys (dependencies, source, extras, dev-dependencies; None
if absent) plus "group" if present.
"""
import hashlib
import json
import os
import sys

args = sys.argv[1:]
target = args.pop(0)
groups = []
no_lock = False
while args:
    a = args.pop(0)
    if a == "--group":
        groups.append(args.pop(0))
    elif a == "--no-lock":
        no_lock = True
    else:
        raise SystemExit("unknown arg: " + a)

os.makedirs(os.path.join(target, "test_project"), exist_ok=True)
with open(os.path.join(target, "test_project", "__init__.py"), "w") as f:
    f.write('VALUE = "hello"\n')

lines = [
    "[tool.poetry]",
    'name = "test-project"',
    'version = "0.1.0"',
    'description = "Test project"',
    'authors = ["Test <test@example.com>"]',
    'packages = [{ include = "test_project" }]',
    "",
    "[tool.poetry.dependencies]",
    'python = "^3.8"',
    "",
]
for g in groups:
    lines += ["[tool.poetry.group.%s.dependencies]" % g, ""]
lines += [
    "[build-system]",
    'requires = ["poetry-core>=1.0.0"]',
    'build-backend = "poetry.core.masonry.api"',
    "",
]
with open(os.path.join(target, "pyproject.toml"), "w") as f:
    f.write("\n".join(lines))

relevant = {
    "dependencies": {"python": "^3.8"},
    "source": None,
    "extras": None,
    "dev-dependencies": None,
}
if groups:
    relevant["group"] = {g: {"dependencies": {}} for g in groups}
content_hash = hashlib.sha256(
    json.dumps(relevant, sort_keys=True).encode()
).hexdigest()

if not no_lock:
    with open(os.path.join(target, "poetry.lock"), "w") as f:
        f.write(
            "package = []\n\n"
            "[metadata]\n"
            'lock-version = "1.1"\n'
            'python-versions = "^3.8"\n'
            'content-hash = "%s"\n\n'
            "[metadata.files]\n" % content_hash
        )
print("created project in", target, "content-hash", content_hash)
