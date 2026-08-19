"""microwave-method: `uvx microwave-method` drops Microwave into your repo.

Stdlib only (ADR-007). This is the single install command. It copies the
framework files into the current repo (additive, never overwrites) and seeds the
wiki. Then, with your confirmation, it sets up git if needed, wires the
pre-commit hook, and opens the guided welcome in your coding agent. Decline and
it just prints the one line to start: nothing touches your machine without a yes.
The guided welcome itself is played by the agent (flows/welcome.md), because
Microwave is a method, not a runtime.
"""
from __future__ import annotations

import importlib.resources as resources
import os
import shutil
import subprocess
import sys
from pathlib import Path

PAYLOAD_DIRS = ["flows", "templates", "techniques", "slop", "gates",
                "embodiment", "hooks", "harness"]
WIKI_SPACES = ["agents", "adr", "projects", "_staging", "_archive"]
WIKI_INDEX = (
    "# Registry index\n\n"
    "One line per artifact: `- [type] id: one-line summary -> path`\n\n"
    "## Agents\n\n## ADR (meta)\n\n## Projects\n"
)
START_LINE = "run the Microwave welcome flow"


def _payload() -> Path:
    return Path(str(resources.files("microwave_method"))) / "_payload"


def _copy_tree(src: Path, dst: Path) -> int:
    copied = 0
    if not src.is_dir():
        return 0
    for root, _dirs, files in os.walk(src):
        rel = Path(root).relative_to(src)
        if "icons" in rel.parts:
            continue
        for name in files:
            out = dst / rel / name
            if not out.exists():
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(Path(root) / name, out)
                copied += 1
    return copied


def _is_git_repo(target: Path) -> bool:
    try:
        r = subprocess.run(["git", "-C", str(target), "rev-parse",
                            "--is-inside-work-tree"],
                           capture_output=True, text=True)
        return r.returncode == 0
    except FileNotFoundError:
        return False


def _confirm(question: str, default: bool = True) -> bool:
    """Yes/no prompt. In a non-interactive context (no tty) or with
    MICROWAVE_NO_LAUNCH=1, never assume yes for a side effect: return False, so
    a piped or CI run stays inert and predictable."""
    if os.environ.get("MICROWAVE_NO_LAUNCH") == "1":
        return False
    if not (sys.stdin and sys.stdin.isatty()):
        return False
    suffix = "[Y/n]" if default else "[y/N]"
    try:
        answer = input(f"{question} {suffix} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    if not answer:
        return default
    return answer in ("y", "yes", "o", "oui")


def _wire_hook(target: Path) -> str:
    """Install the pre-commit hook, backing up any existing, different hook to
    pre-commit.pre-microwave first (never silently clobber or skip)."""
    hooks_dir = target / ".git" / "hooks"
    src_hook = target / "hooks" / "pre-commit"
    if not (hooks_dir.is_dir() and src_hook.is_file()):
        return "pre-commit hook not wired (no .git/hooks or payload hook found)"
    dest = hooks_dir / "pre-commit"
    if dest.exists():
        if dest.read_bytes() == src_hook.read_bytes():
            return "pre-commit hook already current"
        shutil.copy2(dest, hooks_dir / "pre-commit.pre-microwave")
        print("  backed up your existing pre-commit hook to pre-commit.pre-microwave")
    shutil.copy2(src_hook, dest)
    try:
        os.chmod(dest, 0o755)
    except OSError:
        pass
    return "pre-commit hook wired"


def main() -> None:
    target = Path(os.environ.get("MICROWAVE_TARGET", os.getcwd())).resolve()
    payload = _payload()

    banner = payload / "banner.txt"
    if banner.is_file():
        print(banner.read_text(encoding="utf-8"))
    print(f"Installing Microwave into {target}")

    # Copy files and seed the wiki: always safe, additive, never overwrites.
    copied = sum(_copy_tree(payload / d, target / d) for d in PAYLOAD_DIRS)
    gh = target / ".github" / "workflows"
    gh.mkdir(parents=True, exist_ok=True)
    ci = gh / "gates.yml"
    if not ci.exists():
        shutil.copy2(payload / ".github" / "workflows" / "gates.yml", ci)
    co = target / "CODEOWNERS"
    if not co.exists():
        text = (payload / "CODEOWNERS").read_text(encoding="utf-8")
        co.write_text(text.replace("@microphage-create", "@your-gatekeeper"),
                      encoding="utf-8", newline="\n")
    wiki = target / "wiki"
    for space in WIKI_SPACES:
        (wiki / space).mkdir(parents=True, exist_ok=True)
    index = wiki / "INDEX.md"
    if not index.exists():
        index.write_text(WIKI_INDEX, encoding="utf-8", newline="\n")
    print(f"Done. {copied} files installed.")

    # Side effects (git init, hook, launching your agent) only with a yes.
    proceed = _confirm(
        "Set up git here (if needed), wire the hook, and open the welcome flow now?")
    if proceed:
        if not _is_git_repo(target):
            init = subprocess.run(["git", "-C", str(target), "init"],
                                  capture_output=True, text=True)
            print("  git repo initialized." if init.returncode == 0
                  else "  could not run git init (install git for the gates).")
        if _is_git_repo(target):
            print("  " + _wire_hook(target))
        agent = shutil.which("claude")
        if agent:
            agent_path = Path(agent).resolve()
            # shutil.which prepends the CWD on Windows, so a claude.exe planted in
            # this repo would resolve before the real one on PATH. Refuse a binary
            # that resolves inside the folder we are installing into.
            try:
                agent_path.relative_to(target)
                print(f"\nRefusing to auto-launch: 'claude' resolved to a binary inside\n"
                      f"this folder ({agent_path}), which a malicious repo could have\n"
                      f"planted. Open your own coding agent and say:\n    {START_LINE}")
                agent = None
            except ValueError:
                pass  # resolved outside the repo, from a real PATH entry
        if agent:
            print(f"\nStarting {agent_path} on the welcome flow...\n")
            try:
                subprocess.run([str(agent_path), START_LINE], cwd=str(target))
                return
            except OSError as exc:
                print(f"(could not launch the agent: {exc})")

    print("\nTo start: open your coding agent in this folder and say\n")
    print(f"    {START_LINE}\n")
    if not _is_git_repo(target):
        print("First run `git init` here so the gates can guard the repo.")
    print("It adapts to you, and nothing changes until you say so.")


if __name__ == "__main__":
    main()
