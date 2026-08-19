#!/usr/bin/env bash
# Installs the Microwave pre-commit hook into the current repo.
# Handles worktrees, submodules and core.hooksPath via git rev-parse.
# Never silently overwrites an existing hook: it is backed up first.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
  echo "install-hooks: not inside a git repository" >&2
  exit 1
}
HOOKS_DIR="$(git rev-parse --git-path hooks)"
mkdir -p "$HOOKS_DIR"

TARGET="$HOOKS_DIR/pre-commit"
if [ -e "$TARGET" ] && ! cmp -s "$HERE/pre-commit" "$TARGET"; then
  cp "$TARGET" "$TARGET.pre-microwave"
  echo "existing pre-commit hook backed up to $TARGET.pre-microwave"
  echo "(chain it by calling it from the new hook if you still need it)"
fi
cp "$HERE/pre-commit" "$TARGET"
chmod +x "$TARGET"
echo "pre-commit hook installed at $TARGET: gates run on staged agent cards"
