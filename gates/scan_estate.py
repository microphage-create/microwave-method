"""scan_estate: read a folder of repos and propose a context/service map.

The onboarding takes the user by the hand from THEIR estate, not a blank page:
this scans a directory of repositories, detects each repo's stack, and prints a
proposal: one context agent per repo (the guard that carries its conventions) plus
the transversal services to wire (ADR-028). It writes nothing; the propose-estate
flow drives creation with the user, one at a time. Stdlib only (ADR-007).

    python gates/scan_estate.py ~/Documents/GitHub
"""
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
]
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


def slugify(name: str) -> str:
    s = SLUG_BAD.sub("-", name.lower()).strip("-")[:32].rstrip("-")
    return s or "repo"


def already_microwaved(repo: Path) -> bool:
    return (repo / "wiki" / "INDEX.md").exists() or (repo / ".microwave").exists()


def propose(root: Path) -> dict:
    repos = find_repos(root)
    contexts = [{
        "slug": slugify(r.name),
        "repo": r.name,
        "stack": detect_stack(r),
        "microwaved": already_microwaved(r),
    } for r in repos]
    return {"root": str(root), "contexts": contexts, "services": SUGGESTED_SERVICES}


def main(argv: list[str]) -> None:
    root = Path(argv[0]).expanduser() if argv else Path.cwd()
    plan = propose(root)
    contexts = plan["contexts"]
    if not contexts:
        print(f"No git repos found directly under {plan['root']}.")
        if (root / ".git").exists():
            print("This looks like a single repo. Pass the folder that CONTAINS "
                  "your repos, e.g. its parent.")
        return
    print(f"Scanned {plan['root']}: {len(contexts)} repo(s).\n")
    print("Proposed context agents (one guard per repo):")
    width = max(len(c["repo"]) for c in contexts)
    for c in contexts:
        stack = ", ".join(c["stack"]) or "stack not detected"
        note = "  [already has Microwave]" if c["microwaved"] else ""
        print(f"  - {c['repo']:<{width}}  [{stack}]  -> context, slug: {c['slug']}{note}")
    print("\nSuggested transversal services (shared, create once):")
    print("  " + ", ".join(plan["services"]))
    print("\nNext: run the propose-estate flow to create these with you, one at a "
          "time (it asks before every write).")


if __name__ == "__main__":
    main(sys.argv[1:])
