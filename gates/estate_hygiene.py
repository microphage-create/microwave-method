"""estate_hygiene: bring conventions and rules to the chaos of a repos folder.

The estate's guardian, one level up from scan_estate. It does not gently ask; it
DECLARES a small set of arbitrary house rules (naming, home, companions, loose
folders, families) and then judges every repo against them: this one is misnamed,
rename it to X; that one is stale, it belongs in archive/; this loose folder is
not a repo, move it out. One clear way, on purpose, so a thirty-folder estate
stays legible. Read-only, always (ADR-031: humans move and rename; the tool only
names the rule and the verdict). Stdlib only (ADR-007).

    python gates/estate_hygiene.py ~/Documents/GitHub [--stale-days 120]
"""
import re
import subprocess
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from scan_estate import classify, find_repos

# R1: a conforming repo name is lowercase-kebab: letters, digits, single hyphens.
KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# R3: doc-ish companion suffixes. The canonical one is "-docs"; the rest rename to
# it. Deploy/variant satellites (-app, -site, -staging) are legitimately distinct
# and keep their names; they only group under R5 (family), they are not renamed.
DOC_SUFFIX = re.compile(r"-(dossier|doc|docs|notes|note|wiki)$")
# suffixes that mark a satellite of a project, stripped to find the family root
# ("claria-site" and "claria-docs" both belong to "claria").
FAMILY_SUFFIXES = re.compile(
    r"-(app|site|dossier|docs|doc|notes|note|wiki|staging|main|archived|pro|"
    r"plugin|bmad|poc|old|copy|v\d+)$")


def last_commit_days(repo: Path) -> int | None:
    try:
        r = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%ct"],
                           capture_output=True, text=True)
    except OSError:
        return None
    out = r.stdout.strip()
    if r.returncode != 0 or not out:
        return None
    return int((time.time() - int(out)) / 86400)


def family_root(name: str) -> str:
    # Strip one satellite suffix (claria-docs -> claria) so a project and its
    # companions group, but do NOT collapse to the first token: that would fuse
    # unrelated repos (web-app and web-server are not one project).
    return FAMILY_SUFFIXES.sub("", name.lower()) or name.lower()


def kebab_fix(name: str) -> str:
    # The R1-conforming form of a name: accents folded, not dropped, then
    # lowercased, every run of non-[a-z0-9] collapsed to a single hyphen, edges
    # trimmed ("microphage.ai" -> "microphage-ai", "café-app" -> "cafe-app"). Falls back
    # to "repo" for a name that is all punctuation, so the output is always a valid
    # kebab name, never a still-invalid suggestion.
    folded = unicodedata.normalize("NFKD", name.lower())
    folded = "".join(c for c in folded if not unicodedata.combining(c))
    s = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", folded)).strip("-")
    return s or "repo"


def _stack_family(stack: list[str]) -> str:
    s = set(stack)
    if "Next.js" in s:
        return "next"
    if "Web/static" in s and not (s & {"Node/JS", "TypeScript"}):
        return "web"
    if s & {"Node/JS", "TypeScript"}:
        return "node"
    if "Python" in s:
        return "python"
    if "Go" in s:
        return "go"
    if "Rust" in s:
        return "rust"
    return "other"


def home_of(kind: str, stack: list[str], stale: bool) -> str:
    # R2: every repo lives in exactly one home.
    if stale:
        return "archive/"
    if kind == "content":
        return "content/"
    if kind == "code":
        return f"code/{_stack_family(stack)}/"
    return "sandbox/"  # undeclared: no stack, not content


def rename_for(name: str) -> tuple[str, str] | None:
    # The rename a repo needs to obey R3 (companion) then R1 (naming), or None if
    # its name already conforms. Returns (new_name, rule).
    target = name
    rule = ""
    m = DOC_SUFFIX.search(name.lower())
    if m and m.group(0) != "-docs":
        target = name[:m.start()] + "-docs"
        rule = "R3"
    fixed = kebab_fix(target)
    if fixed != target.lower() or (rule == "" and not KEBAB.match(name)):
        rule = rule or "R1"
        target = fixed
    if target == name:
        return None
    return target, rule


def analyse(root: Path, stale_days: int) -> dict:
    children = sorted((p for p in root.iterdir() if p.is_dir()),
                      key=lambda p: p.name.lower())
    repos = find_repos(root)
    repo_names = {p.name for p in repos}
    loose = [p.name for p in children
             if p.name not in repo_names and not p.name.startswith(".")]

    verdicts: list[dict] = []
    for r in repos:
        kind, stack = classify(r)
        days = last_commit_days(r)
        stale = days is not None and days >= stale_days
        rename = rename_for(r.name)
        verdicts.append({
            "name": r.name, "kind": kind, "stack": stack,
            "days": days, "stale": stale,
            "home": home_of(kind, stack, stale),
            "rename": rename[0] if rename else None,
            "rule": rename[1] if rename else ("R2" if stale or kind == "unknown"
                                              else "OK"),
        })

    families = defaultdict(list)
    for p in children:
        if not p.name.startswith("."):
            families[family_root(p.name)].append(p.name)
    dup_families = {r: sorted(ns) for r, ns in families.items() if len(ns) > 1}

    # R4 refined by R3/R5: a loose folder that shares a family root with a real
    # repo is that repo's companion, not a stray. The companion we name must be a
    # folder that EXISTS: the root itself when a repo is named exactly that,
    # otherwise a sibling repo in the same family (never a bare root that no folder
    # carries). Advise folding into it, not "git init".
    repo_names = {v["name"] for v in verdicts}
    root_to_repos: dict[str, list[str]] = defaultdict(list)
    for name in repo_names:
        root_to_repos[family_root(name)].append(name)
    loose_v = []
    for n in loose:
        root_ = family_root(n)
        sibs = sorted(s for s in root_to_repos.get(root_, []) if s != n)
        companion: str | None
        if root_ in repo_names and root_ != n:
            companion = root_
        else:
            companion = sibs[0] if sibs else None
        loose_v.append({"name": n, "companion": companion})

    return {
        "root": str(root), "loose": loose_v, "verdicts": verdicts,
        "families": dup_families, "stale_days": stale_days,
    }


HOUSE_RULES = [
    ("R1 naming", "repos are lowercase-kebab: [a-z0-9] and single hyphens. "
                  "no dots, underscores, capitals, spaces."),
    ("R2 home", "every repo lives in exactly ONE home: code/<stack>/, content/, "
                "archive/ (stale), or sandbox/ (undeclared: no stack, not content)."),
    ("R3 companion", "a project's docs are named <project>-docs. other doc-ish "
                     "suffixes (-dossier, -notes, -wiki) get renamed to it."),
    ("R4 loose", "a folder sitting among repos is a repo (git init) or it does "
                 "not belong here: move it to content/ or out of the estate."),
    ("R5 family", "2+ repos sharing a root are one project split across folders: "
                  "consolidate them, or the split is deliberate and you keep it."),
]


def report(a: dict) -> None:
    verdicts = a["verdicts"]
    code = sum(1 for v in verdicts if v["kind"] == "code")
    content = sum(1 for v in verdicts if v["kind"] == "content")

    print(f"Estate conventions for {a['root']}")
    print(f"  {len(verdicts)} repos ({code} code, {content} content) + "
          f"{len(a['loose'])} loose folders. The rules below are arbitrary on "
          f"purpose: one clear way, so the estate stays legible.\n")

    print("HOUSE RULES (the guardian's; not negotiable per-repo, that is the point):")
    for tag, text in HOUSE_RULES:
        print(f"  {tag:<13} {text}")

    print("\nVERDICTS (what each repo must become; nothing was touched):")
    off = [v for v in verdicts if v["rule"] != "OK"]
    ok = [v for v in verdicts if v["rule"] == "OK"]
    width = max([len(v["name"]) for v in verdicts]
                + [len(lf["name"]) for lf in a["loose"]], default=0)
    for v in sorted(off, key=lambda v: (v["rule"], v["name"].lower())):
        if v["rename"]:
            aged = f" (stale {v['days']}d)" if v["stale"] else ""
            fix = f"rename -> {v['rename']}  then home: {v['home']}{aged}"
        elif v["stale"]:
            fix = f"no commit in {v['days']}d -> {v['home']}"
        else:  # undeclared
            fix = f"undeclared (no stack) -> {v['home']}  give it a stack or a README"
        print(f"  {v['rule']:<4} {v['name']:<{width}}  {fix}")
    for lf in a["loose"]:
        if lf["companion"]:
            fix = (f"not a repo, looks like {lf['companion']}'s companion -> "
                   f"fold into {lf['companion']}, or make it a repo in its family")
        else:
            fix = "not a repo -> git init, or move to content/ or out"
        print(f"  {'R4':<4} {lf['name']:<{width}}  {fix}")
    for v in sorted(ok, key=lambda v: v["name"].lower()):
        print(f"  {'OK':<4} {v['name']:<{width}}  already conforms -> {v['home']}")

    real_dups = {r: ns for r, ns in a["families"].items() if len(ns) > 1}
    if real_dups:
        print("\nR5 FAMILIES (one project split across folders: consolidate, or "
              "keep the split deliberately):")
        for r, ns in sorted(real_dups.items()):
            print(f"  {r}: {', '.join(ns)}")

    print("\nTARGET TREE (where everything lands once the verdicts are applied):")
    tree: dict[str, list[str]] = defaultdict(list)
    for v in verdicts:
        tree[v["home"]].append(v["rename"] or v["name"])
    if a["loose"]:
        tree["review/  (loose: git init, fold, or move out)"] = [
            lf["name"] for lf in a["loose"]]
    for home in sorted(tree):
        print(f"  {home}")
        for n in sorted(tree[home]):
            print(f"      {n}")

    print("\nRead-only: nothing was moved, renamed, or deleted. These are the "
          "rules and the verdicts; you apply them by hand. The guardian brings "
          "the conventions, never touches your code.")


def main(argv: list[str]) -> None:
    args = [x for x in argv if not x.startswith("--")]
    stale_days = 120
    if "--stale-days" in argv:
        i = argv.index("--stale-days")
        try:
            stale_days = int(argv[i + 1])
        except (IndexError, ValueError):
            print("usage: python gates/estate_hygiene.py <folder> [--stale-days N]")
            sys.exit(2)
    given = args[0] if args else "."
    root = Path(given).expanduser()
    if not root.is_dir():
        print(f"not a folder: {given}")
        sys.exit(1)
    if (root / ".git").exists():
        print(f"{given} is a single repo, not a folder of repos. Point me at the "
              f"parent folder that CONTAINS your repos (e.g. its parent).")
        sys.exit(1)
    report(analyse(root, stale_days))


if __name__ == "__main__":
    main(sys.argv[1:])
