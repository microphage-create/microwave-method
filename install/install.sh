#!/usr/bin/env bash
# Microwave Method installer (macOS / Linux)
# Copies flows, templates, gates and embodiment tooling into a target repo
# and seeds the wiki. Additive: never overwrites existing files.
set -euo pipefail

TARGET="${1:?usage: install.sh <target-repo>}"
SRC="$(cd "$(dirname "$0")/.." && pwd)"
DST="$(cd "$TARGET" && pwd)"

git -C "$DST" rev-parse --is-inside-work-tree >/dev/null 2>&1 || echo "warning: $DST is not a git repository (gates rely on repo protection)"

for d in flows templates techniques slop gates embodiment hooks harness; do
  mkdir -p "$DST/$d"
  (cd "$SRC/$d" && find . -type f ! -path "./icons/*") | while read -r f; do
    out="$DST/$d/${f#./}"
    if [ ! -e "$out" ]; then
      mkdir -p "$(dirname "$out")"
      cp "$SRC/$d/${f#./}" "$out"
    fi
  done
done

# CI + CODEOWNERS (placeholder to edit) + git hook wiring
mkdir -p "$DST/.github/workflows"
[ -e "$DST/.github/workflows/gates.yml" ] || cp "$SRC/.github/workflows/gates.yml" "$DST/.github/workflows/gates.yml"
if [ ! -e "$DST/CODEOWNERS" ]; then
  sed 's/@microphage-create/@your-gatekeeper/' "$SRC/CODEOWNERS" > "$DST/CODEOWNERS"
  echo "CODEOWNERS created: replace @your-gatekeeper with your gatekeeper's handle"
fi
if git -C "$DST" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  (cd "$DST" && bash hooks/install-hooks.sh)
fi

mkdir -p "$DST/wiki/agents" "$DST/wiki/adr" "$DST/wiki/projects" "$DST/wiki/_staging" "$DST/wiki/_archive"
if [ ! -e "$DST/wiki/INDEX.md" ]; then
  cat > "$DST/wiki/INDEX.md" <<'EOF'
# Registry index

One line per artifact: `- [type] id: one-line summary → path`

## Agents

## ADR (meta)

## Projects
EOF
fi

echo "Microwave installed into $DST (flows, templates, gates, embodiment, hooks, harness, CI workflow)"
echo "Next: open your coding agent there and say 'run the Microwave adopt flow'."
echo "Hardening left to you (cannot be shipped as files):"
echo "  1. edit CODEOWNERS with your gatekeeper's handle"
echo "  2. adapt harness/claude-settings.example.json into your harness settings"
echo "  3. enable branch protection with required check 'gates', e.g.:"
echo "     gh api -X PUT repos/{owner}/{repo}/branches/main/protection -f enforce_admins=true ..."
