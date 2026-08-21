"""gate_antidup: no unjustified overlap with the registry.

Compares the card's mission + synonyms against every index line (Jaccard
similarity on content words). A close hit without `anti_dup_rationale` fails:
extend the existing agent, or justify the difference in the card.

The threshold is a tripwire, not the guard: it catches word-level overlap
cheaply and forces a written rationale. Purpose-level duplication is judged
by the devil review (flows/devil-review.md, attack surface #1) and, on the
full path, by the gatekeeper.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root, tokenize
from federated_index import federated_index_lines

GATE = "gate_antidup"
THRESHOLD = 0.34


def main(card: str) -> None:
    path = Path(card)
    try:
        fm, _ = read_frontmatter(path)
    except GateError as e:
        fail(GATE, str(e))
    root = repo_root(path.parent)
    slug = str(get(fm, "slug"))
    words = tokenize(str(get(fm, "mission") or "")) | tokenize(
        " ".join(str(s) for s in (get(fm, "synonyms") or []))
    )
    if not words:
        fail(GATE, f"{path.name}: empty mission/synonyms, nothing to compare")

    hits = []
    for src, line in federated_index_lines(root):
        if src is None and (
            f"] {slug}:" in line or f"] {slug} " in line or line.endswith(f"/{path.name}")
        ):
            continue  # the card's own line (local only; a same-slug line in a
            # federated repo is the cross-repo duplicate we want to surface)
        line_words = tokenize(line)
        if not line_words:
            continue
        jaccard = len(words & line_words) / len(words | line_words)
        if jaccard >= THRESHOLD:
            shown = line if src is None else f"[{src}] {line}"
            hits.append((round(jaccard, 2), shown))

    if hits:
        rationale = str(get(fm, "anti_dup_rationale") or "").strip()
        listing = "\n  ".join(f"similarity {j} (threshold {THRESHOLD}) :: {line}"
                              for j, line in sorted(hits, reverse=True))
        if len(rationale) < 20:
            fail(GATE, f"{path.name}: overlaps with existing registry entries and "
                       f"anti_dup_rationale is empty/too short.\n  {listing}\n"
                       f"Extend the existing agent, or justify the difference in the card.")
        ok(GATE, f"{path.name}: {len(hits)} overlap(s) found, rationale present")
        return
    ok(GATE, f"{path.name}: no overlap above {THRESHOLD} in the registry")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/gate_antidup.py <agent-card.md>")
    try:
        main(sys.argv[1])
    except GateError as e:
        fail(GATE, str(e))
