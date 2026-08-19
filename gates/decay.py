"""decay: flag wiki atoms that look abandoned, so a growing wiki doesn't rot.

The failure mode a governed wiki must answer: after months, hundreds of atoms,
and nobody knows which are still alive. `decay` names the dead so you can archive
them, on two signals that together avoid false positives:

- ORPHAN: no other atom references it, by wikilink `[[stem]]` OR by its short id
  in prose (ADRs are cited "ADR-008", not `[[...]]`), so nothing reheats it.
- OLD: its last git commit is older than --days (default 90).

An atom is a candidate only if BOTH hold: a referenced atom is alive even if old,
and a fresh orphan is probably just new. This REPORTS, never deletes (ADR-020:
humans delete). Move a candidate to wiki/_archive/, or refresh it and re-link it.

Not a gate: it runs on demand (or in a scheduled job), like metrics.py and
trace.py, not in the pre-commit hook. Stdlib only (ADR-007).

Usage:
    python gates/decay.py [--days N] [--json]
"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, read_text, repo_root  # noqa: E402

SKIP = {"INDEX.md", "README.md", "BACKLOG.md"}
ID_RE = re.compile(r"^([A-Za-z]{2,6}-\d+)")  # ADR-008, LRN-012, ...


def _reheat_keys(path: Path) -> set[str]:
    """What another atom would use to reheat this one: its full stem, and its
    short id (so `ADR-008` in prose counts, not only `[[ADR-008-title]]`)."""
    keys = {path.stem}
    m = ID_RE.match(path.stem)
    if m:
        keys.add(m.group(1))
    return keys


def _atoms(root: Path) -> list[Path]:
    wiki = root / "wiki"
    return [p for p in wiki.rglob("*.md")
            if p.name not in SKIP and "_archive" not in p.parts]


def _last_commit_age_days(root: Path, path: Path) -> float | None:
    r = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%ct", "--", str(path)],
        capture_output=True, text=True)
    out = r.stdout.strip()
    if r.returncode != 0 or not out:
        return None  # untracked (never committed): not our call to reap
    return (time.time() - int(out)) / 86400.0


def find_stale(root: Path, days: float) -> list[dict]:
    files = _atoms(root)
    texts = {p: read_text(p) for p in files}
    stale = []
    for p in files:
        keys = _reheat_keys(p)
        others = "\n".join(t for q, t in texts.items() if q != p)
        if any(k in others for k in keys):
            continue  # referenced by wikilink or by id in prose: alive
        age = _last_commit_age_days(root, p)
        if age is None or age < days:
            continue
        stale.append({"atom": str(p.relative_to(root)), "age_days": round(age, 1)})
    stale.sort(key=lambda d: d["age_days"], reverse=True)
    return stale


def main(argv: list[str]) -> None:
    days = 90.0
    as_json = "--json" in argv
    if "--days" in argv:
        i = argv.index("--days")
        try:
            days = float(argv[i + 1])
        except (IndexError, ValueError):
            print("usage: python gates/decay.py [--days N] [--json]")
            sys.exit(2)
    try:
        root = repo_root()
    except GateError as e:
        print(f"[decay] {e}")
        sys.exit(1)
    stale = find_stale(root, days)
    if as_json:
        print(json.dumps(stale, indent=2))
        return
    if not stale:
        print(f"[decay] no orphaned atoms older than {days:.0f} days. Wiki is warm.")
        return
    print(f"[decay] {len(stale)} atom(s) orphaned AND older than {days:.0f} days "
          f"(nothing links them, nothing reheated them):\n")
    for s in stale:
        print(f"  {s['age_days']:>6.0f}d  {s['atom']}")
    print("\nArchive them (wiki/_archive/), or refresh and re-link. decay never "
          "deletes; you decide.")


if __name__ == "__main__":
    main(sys.argv[1:])
