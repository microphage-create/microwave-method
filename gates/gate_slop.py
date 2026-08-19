"""gate_slop: durable artifacts do not read like slop.

Mechanically detectable LLM tells (em dashes, filler openers, buzzwords,
hedging stacks, placeholders) are rejected or warned per `slop/slop-rules.csv`.
The shipped bank is a generic STARTER: organizations append their own
proprietary rules to the CSV (or replace it), the mechanism does not change.
Proprietary rule corpora stay private; the gate only needs the CSV rows.

Scope: wiki atoms, i.e. what the agents write durably. Templates
(placeholders are the point), techniques/ (imported banks), and this
mechanism's own files are excluded.

Usage:
    python gates/gate_slop.py <file.md>     # one artifact (run_gates path)
    python gates/gate_slop.py               # sweep wiki/ (the produced atoms)
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, ok, read_text, repo_root

GATE = "gate_slop"
EXCLUDED_PARTS = {"templates", "techniques", "slop", "_archive"}
REQUIRED_COLUMNS = {"id", "pattern", "severity", "message"}


def load_rules(root: Path) -> list[dict]:
    rules_file = root / "slop" / "slop-rules.csv"
    if not rules_file.exists():
        fail(GATE, f"rules bank not found: {rules_file}")
    rules = []
    with rules_file.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            fail(GATE, f"{rules_file}: missing columns {', '.join(sorted(missing))}")
        for row in reader:
            rid = row.get("id") or "?"
            pattern = row.get("pattern")
            if not pattern or not pattern.strip():
                fail(GATE, f"rule '{rid}': empty pattern (a stray comma often "
                           f"shifts the columns; quote the pattern)")
            if row["severity"] not in ("reject", "warn"):
                fail(GATE, f"rule '{rid}': severity must be reject|warn "
                           f"(got {row['severity']!r}); a stray comma in the "
                           f"pattern often shifts the columns, quote the pattern")
            try:
                row["_re"] = re.compile(pattern, re.I | re.M)
            except (re.error, TypeError) as e:
                fail(GATE, f"invalid regex in rule '{rid}': {e}")
            rules.append(row)
    return rules


def _blank_quoted(text: str) -> str:
    # Blank out fenced code, inline code and blockquote lines (keeping line
    # positions intact) so an atom can CITE the very slop it documents without
    # tripping the gate. The prose around them is still scanned.
    def blank(m: "re.Match") -> str:
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", blank, text)
    return "\n".join(" " * len(line) if line.lstrip().startswith(">") else line
                     for line in text.split("\n"))


def scan(path: Path, rules: list[dict]) -> tuple[list[str], list[str]]:
    rejects, warns = [], []
    text = _blank_quoted(read_text(path))
    for rule in rules:
        for m in rule["_re"].finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            entry = (f"{path.name}:{line_no} [{rule['id']}] "
                     f"{m.group(0)[:40]!r} -> {rule['message']}")
            (rejects if rule["severity"] == "reject" else warns).append(entry)
    return rejects, warns


def targets(root: Path) -> list[Path]:
    # Only the GOVERNED content the agents produce: wiki/ atoms. Never the
    # host repo's own files (its CLAUDE.md, README, docs): Microwave installs
    # onto existing repos and must not police what it did not produce
    # (LRN-010). Scan a single file explicitly to check a doc on demand.
    out = []
    for p in (root / "wiki").rglob("*.md"):
        if not EXCLUDED_PARTS.intersection(p.parts):
            out.append(p)
    return out


def main(arg: str | None) -> None:
    root = repo_root(Path(arg).parent if arg else None)
    rules = load_rules(root)
    files = [Path(arg)] if arg else targets(root)
    files = [f for f in files if not EXCLUDED_PARTS.intersection(f.parts)]

    all_rejects, all_warns = [], []
    for f in files:
        try:
            r, w = scan(f, rules)
        except GateError as e:
            fail(GATE, str(e))
        all_rejects += r
        all_warns += w

    for w in all_warns:
        print(f"[{GATE}] warn: {w}")
    if all_rejects:
        fail(GATE, "slop detected:\n  " + "\n  ".join(all_rejects))
    ok(GATE, f"{len(files)} artifact(s) clean"
             + (f" ({len(all_warns)} warnings)" if all_warns else ""))


if __name__ == "__main__":
    try:
        main(sys.argv[1] if len(sys.argv) > 1 else None)
    except GateError as e:
        fail(GATE, str(e))
