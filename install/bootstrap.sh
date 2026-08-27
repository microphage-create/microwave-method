#!/usr/bin/env bash
# Microwave one-line installer (macOS / Linux):
#   curl -fsSL https://raw.githubusercontent.com/microphage-create/microwave-method/main/install/bootstrap.sh | bash
# Installs into the CURRENT directory; pass a path as $1 to target another repo.
# This clones and executes a branch at HEAD: pin it with MICROWAVE_REF=<branch|tag>,
# or download this file, read it, then run it.
set -euo pipefail

TARGET="${1:-$(pwd)}"
REF="${MICROWAVE_REF:-main}"

command -v git >/dev/null || { echo "git is required"; exit 1; }
PY="$(command -v python3 || command -v python || true)"
[ -n "$PY" ] && "$PY" -c 'import sys; sys.exit(sys.version_info < (3, 10))' || { echo "Python 3.10+ is required"; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
echo "Fetching Microwave Method ($REF)..."
git clone --quiet --depth 1 --branch "$REF" https://github.com/microphage-create/microwave-method "$TMP/microwave-method"
bash "$TMP/microwave-method/install/install.sh" "$TARGET"

echo ""
echo "Done. Next: open your coding agent in $TARGET and run /microwave"
echo "  (or say \"run the Microwave welcome flow\" - guides you, scans your existing agents)"
