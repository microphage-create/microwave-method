"""gate_wiki: the wiki is linked, indexed, and its atoms carry their contract.

- every [[wikilink]] resolves to an existing atom filename (stem match)
- every atom under wiki/ has its line in wiki/INDEX.md
- every path referenced by an index line exists
- every atom that declares a frontmatter `type` carries that type's required
  fields (templates are the contract, ADR-007)

Run without argument: checks the whole wiki. With a card path: also checks
that card's links.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, index_lines, ok, read_frontmatter, read_text, repo_root

GATE = "gate_wiki"
WIKILINK = re.compile(r"\[\[([^\]|#]+)\]\]")
SKIP_NAMES = {"README.md", "INDEX.md", "REGISTER.md", "BACKLOG.md", "LEDGER.md", "RULES.md"}
TYPE_REQUIRED = {
    "adr": ["id", "title", "status", "date"],
    "learning": ["id", "title", "date"],
    "bug": ["id", "title", "date", "status"],
    "story": ["project", "agent", "status"],
    "devil-report": ["artifact", "result", "date"],
    "inventory-entry": ["name", "provenance", "kind", "disposition", "scanned"],
    "session-save": ["id", "date", "agent", "scope", "status"],
    # agent-card is validated in depth by gate_schema
}


def rel(root: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return p.name


def main(card: str | None) -> None:
    root = repo_root(Path(card).parent if card else None)
    wiki = root / "wiki"
    atoms = [p for p in wiki.rglob("*.md") if p.name not in SKIP_NAMES]
    stems = {p.stem for p in atoms} | {p.stem for p in (root / "templates").glob("*.md")}

    problems: list[str] = []

    # 1. wikilinks resolve. Two exemptions, both ADR-013 "quoted history":
    #    the archive (inventory entries quote a foreign estate, ADR-010) and
    #    converted artifacts (their body is byte-preserved legacy content;
    #    neutralizing its links would break the lossless guarantee).
    targets = [Path(card).resolve()] if card else atoms
    for p in targets:
        if "_archive" in p.parts:
            continue
        text = read_text(p)
        if text.startswith("---") and "\nconverted_from:" in text.split("---", 2)[1]:
            continue
        for link in WIKILINK.findall(text):
            if link.strip() not in stems:
                problems.append(f"{rel(root, p)}: broken wikilink [[{link}]]")

    # 2. every atom is indexed (except staging: candidates are not registry
    #    entries; the archive and the session saves have their own local
    #    indexes, BACKLOG.md and REGISTER.md: ADR-010, ADR-012)
    idx_text = "\n".join(index_lines(root))
    for p in atoms:
        rp = rel(root, p)
        if "/_staging/" in f"/{rp}" or "/_archive/" in f"/{rp}" \
                or "/sessions/" in f"/{rp}" \
                or "/adr/" in f"/{rp}" or "/learnings/" in f"/{rp}":
            continue  # ADR/learnings are archived rationale; RULES.md is the
                      # live index (wiki/adr/ IS the archive; distilled = has a RULES.md line)
        text = read_text(p)
        if text.startswith("---") and "\nconverted_from:" in text.split("---", 2)[1]:
            continue  # legacy wraps live under their local register (ADR-013)
        if rp not in idx_text:
            problems.append(f"{rp}: not indexed in wiki/INDEX.md")

    # 3. typed atoms carry their contract
    for p in atoms:
        try:
            text = read_text(p)
        except GateError as e:
            problems.append(str(e))
            continue
        if not text.startswith("---"):
            if "/adr/" in p.as_posix():
                problems.append(f"{rel(root, p)}: ADR atoms require frontmatter")
            continue
        try:
            fm, _ = read_frontmatter(p)
        except GateError as e:
            problems.append(str(e))
            continue
        required = TYPE_REQUIRED.get(str(fm.get("type", "")))
        if required:
            miss = [k for k in required if fm.get(k) in (None, "", [])]
            if miss:
                problems.append(f"{rel(root, p)}: type '{fm['type']}' "
                                f"missing fields: {', '.join(miss)}")

    # 4. index lines point at real files
    for line in index_lines(root):
        if "→" not in line:
            problems.append(f"index line without a path arrow: {line}")
            continue
        target = line.split("→", 1)[1].strip()
        if not (root / target).exists():
            problems.append(f"index points at a missing file: {target}")

    if problems:
        fail(GATE, "wiki inconsistencies:\n  " + "\n  ".join(problems))
    ok(GATE, f"{len(atoms)} atoms linked and indexed, index paths all resolve")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
