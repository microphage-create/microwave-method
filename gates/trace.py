"""trace: project git history into a commit-to-atom traceability view (ADR-021).

Not a fourth registry: a VIEW derived from git plus the atom files, generated
on demand, exactly as metrics.py derives the ROI report from the ledger. The
single source of truth stays git; nothing is stored in double. It answers the
"in case of trouble" walk: git blame -> SHA -> here -> the atom -> the full why.

It also enforces ADR-020 at commit granularity: a commit that ADDS an atom file
without naming that atom anywhere in its message is a decision landing with no
global trace (the cigarette butt). --check flags those. Scope is deliberately
tight so it never cries wolf: only ADDED atom files (later edits are covered by
git blame), and only atom-bearing paths (not docs, install, or gate code).

    python gates/trace.py               # recent commit -> atom view
    python gates/trace.py --atom ADR-019  # every commit that touched one atom
    python gates/trace.py --check       # exit 1 if any orphan commit exists
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, ok, repo_root

GATE = "trace"
# atom ids as they appear in a commit message and in an atom filename
ATOM_RE = re.compile(r"\b(?:ADR|LRN|BUG|FEAT|PAT|DEC)-\d+\b")
# paths that carry a decision/learning a commit message must name (ADR-020).
# other paths (docs, install, gate code) are not atom-bearing: not orphan-checked.
ATOM_PATH_RE = re.compile(r"^wiki/(?:adr|projects/[^/]+/(?:learnings|bugs|features))/")


def git(args: list[str]) -> str:
    try:
        out = subprocess.run(
            ["git", *args], capture_output=True, text=True,
            encoding="utf-8", cwd=str(repo_root()))
    except FileNotFoundError:
        fail(GATE, "git not found; trace derives the view from git history")
    if out.returncode != 0:
        fail(GATE, f"git {' '.join(args)} failed: {out.stderr.strip()}")
    return out.stdout


def atom_of_path(path: str) -> str | None:
    m = ATOM_RE.search(Path(path).name)
    return m.group(0) if m else None


def commits() -> list[dict]:
    # one call, records separated by \x1e (RS), fields by \x1f (US). The body
    # (%B) is multiline but carries no separator, so parsing stays unambiguous.
    # name-status lines ("A\tpath", "M\tpath") follow the FILES sentinel.
    raw = git(["log",
               "--format=%x1e%h\x1f%ad\x1f%s\x1f%B\x1fFILES",
               "--name-status", "--date=short"])
    recs: list[dict] = []
    for chunk in raw.split("\x1e"):
        if not chunk.strip():
            continue
        parts = chunk.split("\x1f")
        if len(parts) < 5:
            continue
        sha, date, subject, body, filesblock = parts[0], parts[1], parts[2], parts[3], parts[4]
        # message = subject + body: an atom named anywhere in the message counts
        named = sorted(set(ATOM_RE.findall(subject + "\n" + body)))
        files = []  # (status, path); status[0] is A / M / D / R
        for line in filesblock.splitlines():
            line = line.strip()
            if not line or line == "FILES" or "\t" not in line:
                continue
            status, path = line.split("\t", 1)
            files.append((status, path.strip()))
        recs.append({"sha": sha.strip(), "date": date.strip(),
                     "subject": subject.strip(), "named": named, "files": files})
    return recs


def _root_shas() -> set[str]:
    # root commits (the initial import) predate the naming rule; exempt them
    out = git(["log", "--max-parents=0", "--format=%h"])
    return {s.strip() for s in out.splitlines() if s.strip()}


def orphans(recs: list[dict]) -> list[tuple[str, str, str, str]]:
    # a commit that ADDS an atom file whose id it never names in the message;
    # root commits are exempt (the initial import predates the rule, ADR-020)
    roots = _root_shas()
    out = []
    for r in recs:
        if r["sha"] in roots:
            continue
        for status, path in r["files"]:
            if status.startswith("A") and ATOM_PATH_RE.match(path):
                aid = atom_of_path(path)
                if aid and aid not in r["named"]:
                    out.append((r["sha"], r["date"], aid, r["subject"]))
    return out


def main(argv: list[str]) -> None:
    recs = commits()
    if not recs:
        ok(GATE, "no git history yet")
        return

    if "--check" in argv:
        orph = orphans(recs)
        if orph:
            lines = "\n  ".join(f"{s} {d} {a}: {subj[:50]}"
                                for s, d, a, subj in orph)
            fail(GATE, f"{len(orph)} commit(s) added an atom without naming "
                       f"it (ADR-020/021):\n  {lines}")
        ok(GATE, f"every added atom is named by its commit ({len(recs)} scanned)")
        return

    if "--atom" in argv:
        i = argv.index("--atom")
        if i + 1 >= len(argv):
            fail(GATE, "usage: python gates/trace.py --atom <id>")
        want = argv[i + 1]
        hits = [r for r in recs
                if want in r["named"] or any(atom_of_path(p) == want
                                             for _, p in r["files"])]
        print(f"== commits touching {want} ({len(hits)}) ==")
        for r in hits:
            print(f"  {r['sha']} {r['date']}  {r['subject'][:70]}")
        return

    with_atoms = [r for r in recs if r["named"]]
    print(f"== commit -> atom view ({len(with_atoms)}/{len(recs)} commits "
          f"name an atom) ==")
    for r in with_atoms[:40]:
        print(f"  {r['sha']} {r['date']}  {', '.join(r['named'])}"
              f"  ::  {r['subject'][:56]}")
    orph = orphans(recs)
    if orph:
        print(f"\n{len(orph)} orphan commit(s) (added an atom, did not name "
              f"it): run --check for the list.")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except GateError as e:
        fail(GATE, str(e))
