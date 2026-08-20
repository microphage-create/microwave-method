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
  (cd "$SRC/$d" && find . -type f ! -path "./icons/*" ! -path "*/__pycache__/*" ! -name "*.pyc") | while read -r f; do
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
# Propagate the MIT license and attribution (techniques/ banks are BMAD, MIT)
for f in LICENSE NOTICE.md; do
  [ -e "$DST/$f" ] || { [ -f "$SRC/$f" ] && cp "$SRC/$f" "$DST/$f"; }
done

if git -C "$DST" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  # Wire the hook from the TRUSTED source ($SRC), never from the target tree.
  # Running $DST/hooks/install-hooks.sh (or sourcing $DST/hooks/pre-commit) would
  # execute a repo-planted script: the exact RCE the uvx path guards against.
  (cd "$DST" && bash "$SRC/hooks/install-hooks.sh")
fi

mkdir -p "$DST/wiki/agents" "$DST/wiki/adr" "$DST/wiki/projects" "$DST/wiki/_staging" "$DST/wiki/_archive"
if [ ! -e "$DST/wiki/INDEX.md" ]; then
  cat > "$DST/wiki/INDEX.md" <<'EOF'
# Registry index

One line per artifact: `- [type] id: one-line summary → path`

## Agents

- [agent] microwave: agent zero, the desktop front door that opens a context-loaded session on this repo → wiki/agents/microwave.md

## ADR (meta)

## Projects
EOF
fi

# session-start context (CLAUDE.md + AGENTS.md) + agent-zero card, additive (parity with uvx)
for ctx in CLAUDE.md AGENTS.md; do
  if [ ! -e "$DST/$ctx" ]; then
    [ -f "$SRC/$ctx" ] && cp "$SRC/$ctx" "$DST/$ctx"
  elif ! grep -q "runs on Microwave" "$DST/$ctx"; then
    { printf '\n\n---\n\n'; cat "$SRC/$ctx"; } >> "$DST/$ctx"
  fi
done
[ -e "$DST/wiki/agents/microwave.md" ] || { [ -f "$SRC/wiki/agents/microwave.md" ] && cp "$SRC/wiki/agents/microwave.md" "$DST/wiki/agents/microwave.md"; }

echo "Microwave installed into $DST (flows, templates, techniques, slop, gates, embodiment, hooks, harness, CI workflow)"
echo "Next: open your coding agent there and say 'run the Microwave welcome flow'."
echo "Hardening left to you (cannot be shipped as files):"
echo "  1. edit CODEOWNERS with your gatekeeper's handle"
echo "  2. adapt harness/claude-settings.example.json into your harness settings"
echo "  3. enable branch protection with required check 'gates', e.g.:"
echo "     gh api -X PUT repos/{owner}/{repo}/branches/main/protection -f enforce_admins=true ..."
