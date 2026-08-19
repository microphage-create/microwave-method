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
    "One line per artifact: `- [type] id: one-line summary → path`\n\n"
    "## Agents\n\n"
    "- [agent] microwave: agent zero, the desktop front door that opens a "
    "context-loaded session on this repo → wiki/agents/microwave.md\n\n"
    "## ADR (meta)\n\n## Projects\n"
)
START_LINE = "run the Microwave welcome flow"
TAGLINE = "an agent factory with a governed memory"

try:
    from importlib.metadata import version as _pkg_version
    VERSION = _pkg_version("microwave-method")
except Exception:
    VERSION = "0.1.3"


def _enable_ansi() -> bool:
    if os.environ.get("NO_COLOR") or not sys.stdout.isatty():
        return False
    if os.name == "nt":
        try:
            import ctypes
            k = ctypes.windll.kernel32
            k.SetConsoleMode(k.GetStdHandle(-11), 7)  # VT processing
        except Exception:
            return False
    return True


_COLOR = _enable_ansi()
_ANSI_RE = __import__("re").compile(r"\033\[[0-9;]*m")


def _c(code: str) -> str:
    return f"\033[{code}m" if _COLOR else ""


def _vlen(s: str) -> int:
    """Visible length: strip ANSI (braille glyphs are single-width)."""
    return len(_ANSI_RE.sub("", s))


def _welcome(target: Path, payload: Path) -> None:
    """Boxed splash in the Grok/Claude-Code spirit: the M centered, product
    name + version + path bottom-left. Plain box if the terminal has no color."""
    cols = shutil.get_terminal_size((80, 24)).columns
    inner = max(46, min(cols - 2, 96))
    dim, accent, reset, bold = _c("2"), _c("38;2;120;170;170"), _c("0"), _c("1")
    tl, tr, bl, br, h, v = ("╭", "╮", "╰", "╯", "─", "│") if _COLOR else ("+", "+", "+", "+", "-", "|")

    def row(content: str = "") -> None:
        print(dim + v + reset + content + " " * max(0, inner - _vlen(content)) + dim + v + reset)

    art = []
    b = payload / "banner.txt"
    if b.is_file():
        art = b.read_text(encoding="utf-8").rstrip("\n").split("\n")
    art_w = max((len(l) for l in art), default=0)
    pad = " " * max(0, (inner - art_w) // 2)

    print()
    print(dim + tl + h * inner + tr + reset)
    row(); row()
    for l in art:
        row(accent + pad + l + reset)
    row(); row()
    row("  " + bold + "Microwave Method" + reset + dim + "   v" + VERSION + reset)
    row("  " + dim + str(target) + reset)
    row("  " + dim + TAGLINE + reset)
    row()
    print(dim + bl + h * inner + br + reset)
    print()


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


def _resolve_agent(target: Path) -> tuple[Path | None, Path | None]:
    """Resolve the 'claude' binary for auto-launch, refusing an untrusted one.

    Returns (trusted, refused). `trusted` is a claude binary safe to launch, or
    None. `refused` is set when a claude binary was found but resolves INSIDE
    `target`: shutil.which prepends the CWD on Windows, so a claude.exe planted
    at a repo's root would resolve before the real one on PATH (an RCE on
    `uvx microwave-method`). This is the security guard; keep it covered.
    """
    found = shutil.which("claude")
    if not found:
        return None, None
    agent_path = Path(found).resolve()
    try:
        agent_path.relative_to(Path(target).resolve())
    except ValueError:
        return agent_path, None  # outside the repo, from a real PATH entry
    return None, agent_path  # inside the repo: could be planted, refuse


def _embody_agent_zero(target: Path) -> None:
    """Agent zero: put the Microwave icon on the desktop (the front door).

    Additive, gated behind its own yes, and never fatal: an OS with no Windows
    Terminal / Desktop to write to just prints why and moves on."""
    card = target / "wiki" / "agents" / "microwave.md"
    embodier = target / "embodiment" / "embody.py"
    if not (card.is_file() and embodier.is_file()):
        return
    if not _confirm("Put a Microwave icon on your desktop (opens this repo in a terminal)?"):
        return
    try:
        r = subprocess.run([sys.executable, str(embodier), str(card)],
                           cwd=str(target), capture_output=True, text=True)
    except OSError as exc:
        print(f"  (no desktop icon: {exc})")
        return
    if r.returncode == 0:
        print(f"  {_c('32')}+{_c('0')} Microwave icon on your desktop")
    else:
        tail = (r.stderr or r.stdout).strip().splitlines()
        print(f"  (no desktop icon this time: {tail[-1] if tail else 'embodiment skipped'})")


def main() -> None:
    target = Path(os.environ.get("MICROWAVE_TARGET", os.getcwd())).resolve()
    payload = _payload()

    _welcome(target, payload)

    green, reset = _c("32"), _c("0")

    def _ok(msg: str) -> None:
        print(f"  {green}+{reset} {msg}")

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
    # propagate the MIT license and attribution (the techniques/ banks are from
    # BMAD, MIT) alongside the copied files
    for name in ("LICENSE", "NOTICE.md"):
        out = target / name
        if not out.exists() and (payload / name).is_file():
            shutil.copy2(payload / name, out)
    wiki = target / "wiki"
    for space in WIKI_SPACES:
        (wiki / space).mkdir(parents=True, exist_ok=True)
    index = wiki / "INDEX.md"
    if not index.exists():
        index.write_text(WIKI_INDEX, encoding="utf-8", newline="\n")
    # CLAUDE.md (session-start context) and the agent-zero card, additive
    claude = target / "CLAUDE.md"
    src_claude = payload / "CLAUDE.md"
    if src_claude.is_file():
        if not claude.exists():
            shutil.copy2(src_claude, claude)
        elif "runs on Microwave" not in claude.read_text(encoding="utf-8"):
            # host already has a CLAUDE.md: append our session-start block, never clobber
            with claude.open("a", encoding="utf-8") as f:
                f.write("\n\n---\n\n" + src_claude.read_text(encoding="utf-8"))
    zero_src = payload / "wiki" / "agents" / "microwave.md"
    zero = wiki / "agents" / "microwave.md"
    if not zero.exists() and zero_src.is_file():
        shutil.copy2(zero_src, zero)
    _ok(f"{copied} files copied, wiki seeded, CI + CODEOWNERS dropped")

    # Side effects (git init, hook, launching your agent) only with a yes.
    proceed = _confirm(
        "Set up git here (if needed), wire the hook, and open the welcome flow now?")
    if proceed:
        if not _is_git_repo(target):
            init = subprocess.run(["git", "-C", str(target), "init"],
                                  capture_output=True, text=True)
            _ok("git repo initialized" if init.returncode == 0
                else "git not found (install git so the gates can guard the repo)")
        if _is_git_repo(target):
            _ok(_wire_hook(target))
        _embody_agent_zero(target)
        agent_path, refused = _resolve_agent(target)
        if refused is not None:
            print(f"\nRefusing to auto-launch: 'claude' resolved to a binary inside\n"
                  f"this folder ({refused}), which a malicious repo could have\n"
                  f"planted. Open your own coding agent and say:\n    {START_LINE}")
        if agent_path is not None:
            print(f"\nStarting {agent_path} on the welcome flow...\n")
            try:
                subprocess.run([str(agent_path), START_LINE], cwd=str(target))
                return
            except OSError as exc:
                print(f"(could not launch the agent: {exc})")

    dim, bold, reset = _c("2"), _c("1"), _c("0")
    print(f"{dim}Hardening left to you (cannot be shipped as files):{reset}")
    print(f"  1. put your gatekeeper's handle in {bold}CODEOWNERS{reset}")
    print(f"  2. adapt {bold}harness/claude-settings.example.json{reset} into your harness")
    print(f"  3. enable branch protection with the required check {bold}gates{reset}")
    print(f"\nTo start: open your coding agent here and say")
    print(f"    {bold}{START_LINE}{reset}")
    if not _is_git_repo(target):
        print(f"{dim}First run `git init` here so the gates can guard the repo.{reset}")
    print(f"{dim}It adapts to you, and nothing changes until you say so.{reset}")


if __name__ == "__main__":
    main()
