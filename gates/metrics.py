"""metrics: aggregate the governance ledger into a ROI report (ADR-014).

Deterministic, stdlib only. Reads wiki/metrics/LEDGER.md, prints counts.
The interception count is the point: it is the invisible benefit
(defects prevented, duplicates blocked) made visible.

    python gates/metrics.py            # full report
    python gates/metrics.py --since 2026-08-01
    python gates/metrics.py --digest   # per-author activity digest (ADR-018)

The digest reports CONTRIBUTIONS, attributed and factual, never a verdict
on people. Used for transparency and recognition it is healthy; turned
into a ranking to punish it poisons adoption (Grudin's law). The tool
counts; the judging of people is not its job and must not become one.
"""
from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, ok, read_text, repo_root

GATE = "metrics"


def parse(root: Path, since: str | None) -> list[tuple[str, str, str, str, str]]:
    # DATE | event | subject | detail | author  (author optional, ADR-018)
    text = read_text(root / "wiki" / "metrics" / "LEDGER.md")
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("20"):  # ledger lines start with a date
            continue
        parts = [p.strip() for p in line.lstrip("- ").split("|")]
        if len(parts) < 3:
            continue
        date, event, subject = parts[0], parts[1], parts[2]
        if not event:  # a malformed line (empty event) is not an event
            print(f"[{GATE}] warn: skipped malformed ledger line: {line!r}",
                  file=sys.stderr)
            continue
        detail = parts[3] if len(parts) > 3 else ""
        author = parts[4] if len(parts) > 4 else ""
        if since and date < since:
            continue
        rows.append((date, event, subject, detail, author))
    return rows


def digest(rows) -> None:
    from collections import defaultdict
    per = defaultdict(Counter)
    for date, event, subject, detail, author in rows:
        per[author or "unattributed"][event] += 1
    print("== Contribution digest ==")
    print("Factual, attributed contributions. NOT a verdict on people:")
    print("recognition and learning, never a ranking to punish (ADR-018).\n")
    for author, c in sorted(per.items()):
        line = ", ".join(f"{n} {ev}" for ev, n in c.most_common())
        print(f"  {author}: {line}")


def main(since: str | None, mode: str) -> None:
    root = repo_root()
    rows = parse(root, since)
    if not rows:
        ok(GATE, "ledger empty (no governance events logged yet)")
        return
    if mode == "digest":
        digest(rows)
        return

    events = Counter(r[1] for r in rows)
    created = [r for r in rows if r[1] == "created"]
    minutes = [int(r[3]) for r in created if r[3].isdigit()]
    intercepted = [r for r in rows if r[1] == "intercepted"]

    # detail is "source:count" (a batch, e.g. gate_slop:74) or "source:sev"
    # (a single defect, e.g. devil-r1:high). Sum the counts, count the rest.
    def weight(detail: str) -> int:
        tail = detail.split(":", 1)[1] if ":" in detail else ""
        return int(tail) if tail.isdigit() else 1

    total_defects = sum(weight(r[3]) for r in intercepted)
    by_source = Counter()
    for r in intercepted:
        by_source[r[3].split(":")[0]] += weight(r[3])

    span = f" since {since}" if since else ""
    print(f"== Microwave governance report{span} ==")
    print(f"window: {rows[0][0]} -> {rows[-1][0]}, {len(rows)} events\n")
    print(f"VISIBLE")
    print(f"  agents created:   {events['created']}")
    print(f"  agents/atoms purged: {events['purged']}")
    if minutes:
        print(f"  method cost:      {sum(minutes)} min total, "
              f"{sum(minutes) / len(minutes):.0f} min median-ish per agent")
    print(f"\nINVISIBLE (prevention, the reason to run this)")
    print(f"  defects intercepted before activation: {total_defects} "
          f"(in {events['intercepted']} events)")
    for src, n in by_source.most_common():
        print(f"    via {src}: {n}")
    print(f"  duplicates blocked: {events['deduped']}")
    print(f"\nnote: reuse and compute savings need your provider dashboard; "
          f"this ledger measures what the loop itself can see (ADR-014).")


if __name__ == "__main__":
    since = None
    if "--since" in sys.argv:
        i = sys.argv.index("--since")
        if i + 1 >= len(sys.argv):
            fail(GATE, "usage: python gates/metrics.py --since <YYYY-MM-DD>")
        since = sys.argv[i + 1]
    mode = "digest" if "--digest" in sys.argv else "report"
    try:
        main(since, mode)
    except GateError as e:
        fail(GATE, str(e))
