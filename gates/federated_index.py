"""federated_index: roll several repos' registries into one anti-dup surface.

The registry (wiki/INDEX.md) lives in a repo, so a single repo's anti-dup only
sees that repo. An enterprise runs many repos; two teams in two repos can create
the same agent and neither gate would notice. This module lets a repo declare a
federation of sibling repos and have `gate_antidup` compare a new card against
all of their registries at once, so "one central inventory" holds past one repo.

Declaration lives at `<repo>/.microwave/federation`: one repo path per line
(absolute, or relative to this repo root), `#` comments and blank lines ignored.
Only each repo's `wiki/INDEX.md` is read, a single file, so it stays cheap and
stdlib-only (ADR-007). A listed repo that is absent or has no registry is skipped
quietly: a federation must not turn a teammate's missing checkout into a red CI.

No manifest means no federation: `federated_index_lines` then returns exactly
the local lines, byte-for-byte the pre-federation behavior, so the single-repo
case (almost everyone at first) is untouched.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, index_lines, read_text, repo_root

MANIFEST = (".microwave", "federation")


def _manifest_repos(root: Path) -> list[Path]:
    """Resolved paths of the repos this one federates with (self excluded, deduped,
    order preserved). Absent manifest -> empty list."""
    mf = root
    for part in MANIFEST:
        mf = mf / part
    if not mf.exists():
        return []
    try:
        manifest = read_text(mf)
    except GateError:
        return []  # a corrupt/unreadable manifest degrades to no-federation,
        # never a red CI (ADR-027: never fail the federation on a bad file)
    seen = {root.resolve()}
    repos: list[Path] = []
    for raw in manifest.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        p = Path(line)
        if not p.is_absolute():
            p = root / p
        p = p.resolve()
        if p in seen:  # self, or a duplicate entry
            continue
        seen.add(p)
        repos.append(p)
    return repos


def federated_index_lines(root: Path) -> list[tuple[str | None, str]]:
    """(source, index-line) for the local registry plus every federated one.

    source is None for the local repo (so callers can keep their own-card skip
    local-only) and the repo's folder name for a federated one (so a hit tells
    you WHICH repo already holds the overlapping agent)."""
    out: list[tuple[str | None, str]] = [(None, ln) for ln in index_lines(root)]
    for repo in _manifest_repos(root):
        if not (repo / "wiki" / "INDEX.md").exists():
            continue  # absent checkout / not a Microwave repo: skip, never fail
        try:
            lines = index_lines(repo)
        except GateError:
            continue
        out.extend((repo.name, ln) for ln in lines)
    return out


def main() -> None:
    """Print the federated inventory: the central, cross-repo agent map the
    per-repo registry aggregates into."""
    root = repo_root()
    lines = federated_index_lines(root)
    local = sum(1 for src, _ in lines if src is None)
    by_repo: dict[str, int] = {}
    for src, _ in lines:
        if src is not None:
            by_repo[src] = by_repo.get(src, 0) + 1
    print(f"local ({root.name}): {local} entries")
    for repo in sorted(by_repo):
        print(f"federated ({repo}): {by_repo[repo]} entries")
    repos = 1 + len(by_repo)
    print(f"total: {len(lines)} entries across {repos} repo(s)")
    if not by_repo:
        print("(no federation declared; add repos to .microwave/federation)")


if __name__ == "__main__":
    main()
