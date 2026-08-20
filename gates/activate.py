"""activate: tooled, re-validated activation of a staged agent card.

Fast path (blast_radius: read): run by the creator once gates are green.
Full path: run by the gatekeeper as the act of judgment.

Does, in order:
1. run the full gate pipeline on the staged card (pre-check)
2. move the card from wiki/_staging/ to wiki/agents/, set `status: active`
3. append the registry line to wiki/INDEX.md
4. re-run the full gate pipeline on the ACTIVATED card (post-check):
   the state that ships is the state that was validated

Steps 2-4 are wrapped so that ANY failure (a failed post-check, an IO error, a
missing heading) rolls the whole thing back to staging. Writes are atomic
(temp + rename) so a crash mid-write cannot leave a half-written file.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _lib import GateError, fail, get, ok, read_frontmatter, repo_root

GATE = "activate"


def run_pipeline(card: Path) -> bool:
    res = subprocess.run([sys.executable, str(Path(__file__).parent / "run_gates.py"), str(card)])
    return res.returncode == 0


def _atomic_write(path: Path, text: str) -> None:
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main(card_arg: str) -> None:
    src = Path(card_arg).resolve()
    root = repo_root(src.parent)
    if "_staging" not in src.parts:
        fail(GATE, f"{src.name}: activation starts from wiki/_staging/ (got {src})")
    try:
        fm, _ = read_frontmatter(src)
    except GateError as e:
        fail(GATE, str(e))
    slug = str(get(fm, "slug"))
    mission = str(get(fm, "mission") or "").rstrip(".")

    if os.environ.get("MICROWAVE_SHADOW") == "1":
        # fail() is report-only in shadow, so exit directly: the gates are not
        # actually validating, so activating on them cannot be trusted.
        print(f"[{GATE}] shadow mode is on: gates are report-only, so activation is "
              f"not safe. Unset MICROWAVE_SHADOW to validate and activate.")
        sys.exit(1)
    if not run_pipeline(src):
        fail(GATE, "pre-check failed: fix the gates before activating")

    dst = root / "wiki" / "agents" / f"{slug}.md"
    if dst.exists():
        fail(GATE, f"{dst} already exists")

    src_text = src.read_text(encoding="utf-8")
    new_text, n = re.subn(r"^status: staging$", "status: active", src_text,
                          count=1, flags=re.M)
    if n != 1:
        fail(GATE, f"{src.name}: could not flip 'status: staging' to active")

    index = root / "wiki" / "INDEX.md"
    idx_before = index.read_text(encoding="utf-8-sig")
    line = f"- [agent] {slug}: {mission} → wiki/agents/{slug}.md"

    dst_created = idx_changed = src_removed = False

    def rollback() -> None:
        if dst_created and dst.exists():
            dst.unlink()
        if idx_changed:
            _atomic_write(index, idx_before)
        if src_removed and not src.exists():
            _atomic_write(src, src_text)

    try:
        _atomic_write(dst, new_text)
        dst_created = True

        if line not in idx_before:
            if "## Agents\n" not in idx_before:
                raise GateError("wiki/INDEX.md has no '## Agents' section: "
                                "restore the heading before activating")
            _atomic_write(index, idx_before.replace(
                "## Agents\n", f"## Agents\n\n{line}\n", 1))
            idx_changed = True

        src.unlink()
        src_removed = True

        if not run_pipeline(dst):
            raise GateError("post-check failed on the activated card")
    except BaseException as exc:
        rollback()
        msg = str(exc) if isinstance(exc, GateError) else f"{type(exc).__name__}: {exc}"
        fail(GATE, f"activation rolled back to staging ({msg})")

    ok(GATE, f"{slug} activated, registered, and re-validated in its final state")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        fail(GATE, "usage: python gates/activate.py wiki/_staging/<slug>.md")
    main(sys.argv[1])
