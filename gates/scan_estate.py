"""scan_estate: read a folder of repos and propose a context/service map.

The onboarding takes the user by the hand from THEIR estate, not a blank page:
this scans a directory of repositories, detects each repo's stack, and prints a
proposal: one context agent per repo (the guard that carries its conventions) plus
the transversal services to wire (ADR-028). It writes nothing; the propose-estate
flow drives creation with the user, one at a time. Stdlib only (ADR-007).

    python gates/scan_estate.py ~/Documents/GitHub
"""
import os
import re
import sys
from pathlib import Path

# marker file -> stack label, most specific first (first match wins per label)
STACK_MARKERS = [
    ("next.config.js", "Next.js"), ("next.config.ts", "Next.js"),
    ("next.config.mjs", "Next.js"),
    ("package.json", "Node/JS"), ("tsconfig.json", "TypeScript"),
    ("pyproject.toml", "Python"), ("setup.py", "Python"),
    ("requirements.txt", "Python"),
    ("go.mod", "Go"), ("Cargo.toml", "Rust"), ("Gemfile", "Ruby"),
    ("composer.json", "PHP"), ("pom.xml", "Java/Maven"),
    ("build.gradle", "Gradle"), ("Dockerfile", "Docker"),
    ("index.html", "Web/static"),  # a vanilla HTML/JS site with no package.json
]
# Extensions that mark a file as code (vs prose), for the content-repo heuristic.
CODE_EXT = {".js", ".mjs", ".ts", ".jsx", ".tsx", ".py", ".go", ".rs", ".rb",
            ".php", ".java", ".html", ".css", ".vue", ".svelte", ".c", ".cpp"}
WALK_SKIP = {".git", "node_modules", ".next", "dist", "build", "__pycache__",
             ".obsidian", "_legacy", "_raw", "_archive"}
# a starter catalog of transversal services worth having across repos
SUGGESTED_SERVICES = ["code-review", "copywriter", "release-notes", "test-writer"]
SLUG_BAD = re.compile(r"[^a-z0-9-]+")


def find_repos(root: Path) -> list[Path]:
    """Direct child directories that are git repos, sorted by name."""
    if not root.is_dir():
        return []
    return sorted((p for p in root.iterdir() if p.is_dir() and (p / ".git").exists()),
                  key=lambda p: p.name.lower())


def detect_stack(repo: Path) -> list[str]:
    labels: list[str] = []
    for marker, label in STACK_MARKERS:
        if (repo / marker).exists() and label not in labels:
            labels.append(label)
    return labels


def _markdown_dominant(repo: Path) -> bool:
    """A repo of prose, not code: markdown files clearly outnumber code files.
    Walks a bounded tree (heavy/vendored dirs pruned) so it stays fast."""
    md = code = seen = 0
    for _dirpath, dirnames, filenames in os.walk(repo):
        dirnames[:] = [d for d in dirnames if d not in WALK_SKIP]
        for f in filenames:
            seen += 1
            ext = Path(f).suffix.lower()
            if ext == ".md":
                md += 1
            elif ext in CODE_EXT:
                code += 1
        # bounded by TOTAL entries too, so a repo with a huge assets/data tree
        # (which grows neither counter) is not crawled in full every scan.
        if seen > 2000 or md + code > 400:
            break
    return md >= 3 and md >= 3 * code


def classify(repo: Path) -> tuple[str, list[str]]:
    """(kind, stack). kind is 'code' (a code stack was found), 'content' (an
    Obsidian vault or a markdown-dominant corpus, where a code-conventions guard
    does not fit), or 'unknown' (no code stack and not obviously content)."""
    stack = detect_stack(repo)
    if stack:
        return "code", stack
    if (repo / ".obsidian").is_dir() or _markdown_dominant(repo):
        return "content", []
    return "unknown", []


def slugify(name: str) -> str:
    s = SLUG_BAD.sub("-", name.lower()).strip("-")[:32].rstrip("-")
    return s or "repo"


def already_microwaved(repo: Path) -> bool:
    return (repo / "wiki" / "INDEX.md").exists() or (repo / ".microwave").exists()


def propose(root: Path) -> dict:
    repos = find_repos(root)
    contexts = []
    for r in repos:
        kind, stack = classify(r)
        contexts.append({
            "slug": slugify(r.name),
            "repo": r.name,
            "kind": kind,
            "stack": stack,
            "microwaved": already_microwaved(r),
        })
    return {"root": str(root), "contexts": contexts, "services": SUGGESTED_SERVICES}


def _duplicate_slugs(contexts: list[dict]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for c in contexts:
        (dupes if c["slug"] in seen else seen).add(c["slug"])
    return sorted(dupes)


def _nested_repo_dirs(root: Path) -> list[str]:
    """Child dirs that are not repos themselves but CONTAIN repos one level down,
    so a nested estate (GitHub/org/repo) is not silently reported as empty."""
    if not root.is_dir():
        return []
    return sorted(child.name for child in root.iterdir()
                  if child.is_dir() and not (child / ".git").exists()
                  and find_repos(child))


def main(argv: list[str]) -> None:
    given = argv[0] if argv else "."
    root = Path(given).expanduser()
    plan = propose(root)
    contexts = plan["contexts"]
    if not contexts:
        print(f"No git repos found directly under {given}.")
        if (root / ".git").exists():
            print("This looks like a single repo. Pass the folder that CONTAINS "
                  "your repos, e.g. its parent.")
        else:
            nested = _nested_repo_dirs(root)
            if nested:
                print("Repos seem nested one level deeper, under: "
                      + ", ".join(nested) + ". Point me at one of those folders.")
        return
    print(f"Scanned {given}: {len(contexts)} repo(s) (direct children).\n")
    width = max(len(c["repo"]) for c in contexts)
    content = [c for c in contexts if c["kind"] == "content"]
    guarded = [c for c in contexts if c["kind"] != "content"]

    print("Proposed context agents (one guard per code repo):")
    for c in guarded:
        stack = ", ".join(c["stack"]) or "no stack detected, confirm this is a code repo"
        note = "  [already has Microwave]" if c["microwaved"] else ""
        print(f"  - {c['repo']:<{width}}  [{stack}]  -> context, slug: {c['slug']}{note}")

    if content:
        print("\nContent/knowledge repos (a code-conventions guard does not fit "
              "these vaults and prose corpora; govern their content another way, "
              "or skip):")
        for c in content:
            note = "  [already has Microwave]" if c["microwaved"] else ""
            print(f"  - {c['repo']:<{width}}{note}")
    dupes = _duplicate_slugs(contexts)
    if dupes:
        print("\nWARNING: repos collide on one agent slug: " + ", ".join(dupes)
              + ". Rename a repo or give them distinct slugs before creating both.")
    nested = _nested_repo_dirs(root)
    if nested:
        print("\nNote: more repos are nested under " + ", ".join(nested)
              + " (scanned direct children only).")
    print("\nSuggested transversal services (shared, create once):")
    print("  " + ", ".join(plan["services"]))
    print("\nNext: run the propose-estate flow to create these with you, one at a "
          "time (it asks before every write).")


if __name__ == "__main__":
    main(sys.argv[1:])
