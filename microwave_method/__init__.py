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
import re
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
    "- [service] microwave: agent zero, the desktop front door that opens a "
    "context-loaded session on this repo → wiki/agents/microwave.md\n\n"
    "## ADR (meta)\n\n## Projects\n"
)
START_LINE = "run the Microwave welcome flow"
TAGLINE = "an agent factory with a governed memory"

try:
    from importlib.metadata import version as _pkg_version
    VERSION = _pkg_version("microwave-method")
except Exception:
    VERSION = "0.1.6"


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
        if "__pycache__" in rel.parts or ("icons" in rel.parts and "build" in rel.parts):
            continue
        for name in files:
            if name.endswith((".pyc", ".pyo")):
                continue
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


def _ask(question: str) -> str:
    """Free-text prompt. Non-interactive, piped, or MICROWAVE_NO_LAUNCH=1: return
    "" so an unattended run stays inert and takes every default."""
    if os.environ.get("MICROWAVE_NO_LAUNCH") == "1":
        return ""
    if not (sys.stdin and sys.stdin.isatty()):
        return ""
    try:
        return input(f"{question} ").strip()
    except (EOFError, KeyboardInterrupt):
        return ""


def _png_256(p: Path) -> bool:
    """True if p is a 256x256 PNG (what embody.py requires), read from the header
    with no third-party lib."""
    try:
        data = p.read_bytes()[:24]
    except OSError:
        return False
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        return False
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    return (w, h) == (256, 256)


def _patch_card(card: Path, launch: str, icon_rel: str) -> None:
    """Rewrite only the agent-zero card's launch/icon lines, in place, to the
    values the user chose. Leaves the rest of the card untouched."""
    try:
        lines = card.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError:
        return
    out = []
    for ln in lines:
        m = re.match(r"^(\s*)(launch|icon):\s", ln)
        if m and m.group(2) == "launch":
            out.append(f"{m.group(1)}launch: {launch}\n")
        elif m and m.group(2) == "icon":
            out.append(f"{m.group(1)}icon: {icon_rel}\n")
        else:
            out.append(ln)
    card.write_text("".join(out), encoding="utf-8")


def _wire_hook(target: Path, payload: Path) -> str:
    """Install the pre-commit hook FROM THE TRUSTED PAYLOAD, not target/hooks/
    which a cloned repo controls (wiring a repo-planted hook would run its code
    on the next commit). Back up any existing, different hook to
    pre-commit.pre-microwave first (never silently clobber or skip)."""
    hooks_dir = target / ".git" / "hooks"
    src_hook = payload / "hooks" / "pre-commit"
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
    # shutil.which prepends the CWD on Windows; a planted binary could sit in the
    # target OR the process cwd (they can differ via MICROWAVE_TARGET). Refuse both.
    for danger in {Path(target).resolve(), Path.cwd().resolve()}:
        try:
            agent_path.relative_to(danger)
            return None, agent_path  # inside a repo dir: could be planted, refuse
        except ValueError:
            continue
    return agent_path, None  # outside both, from a real PATH entry


def _install_plan(target: Path, payload: Path) -> list[Path]:
    """The files an install WOULD create (additive), for --dry-run. Existing
    files are never in the list, since the installer never overwrites."""
    planned: list[Path] = []

    def add(p: Path) -> None:
        if not p.exists():
            planned.append(p)

    for d in PAYLOAD_DIRS:
        src = payload / d
        if not src.is_dir():
            continue
        for root, _dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            if "icons" in rel.parts or "__pycache__" in rel.parts:
                continue
            for name in files:
                if name.endswith((".pyc", ".pyo")):
                    continue
                add(target / d / rel / name)
    add(target / ".github" / "workflows" / "gates.yml")
    for name in ("CODEOWNERS", "LICENSE", "NOTICE.md", "CLAUDE.md", "AGENTS.md"):
        add(target / name)
    add(target / "wiki" / "INDEX.md")
    add(target / "wiki" / "agents" / "microwave.md")
    return planned


def _embody_agent_zero(target: Path, payload: Path) -> None:
    """Agent zero: put the Microwave icon on the desktop (the front door).

    Additive, gated behind its own yes, never fatal. Refuses to run a target
    embody.py that differs from the shipped one (a cloned repo could have planted
    code there), mirroring the claude-binary guard."""
    card = target / "wiki" / "agents" / "microwave.md"
    embodier = target / "embodiment" / "embody.py"
    trusted = payload / "embodiment" / "embody.py"
    if not (card.is_file() and embodier.is_file()):
        return
    if trusted.is_file() and embodier.read_bytes() != trusted.read_bytes():
        print("  (skipping the desktop icon: this repo's embodiment/embody.py differs")
        print("   from the shipped one; run it yourself if you trust it)")
        return
    if not _confirm("Put a Microwave launcher on your desktop (opens this repo in a terminal)?"):
        return

    # Two quick choices, each with a safe default so pressing Enter just works.
    launch = "claude"
    if _confirm("  Start Claude with permissions pre-approved "
                "(skips the per-action prompts)?", default=False):
        launch = "claude --dangerously-skip-permissions"

    icon_rel = "embodiment/icons/microwave.png"
    want = _ask("  Icon: press Enter for the Microwave M, or paste a path to your "
                "own 256x256 .png:")
    if want:
        src = Path(want.strip('"').strip("'")).expanduser()
        if _png_256(src):
            safe = re.sub(r"[^A-Za-z0-9._-]", "-", src.stem)[:40] or "custom"
            dst = target / "embodiment" / "icons" / f"{safe}.png"
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                icon_rel = f"embodiment/icons/{safe}.png"
            except OSError as exc:
                print(f"  (couldn't use that image, keeping the Microwave M: {exc})")
        else:
            print("  (that file isn't a 256x256 PNG, keeping the Microwave M)")

    _patch_card(card, launch, icon_rel)

    try:
        r = subprocess.run([sys.executable, str(embodier), str(card)],
                           cwd=str(target), capture_output=True, text=True)
    except OSError as exc:
        print(f"  (couldn't place the launcher this time: {exc})")
        return
    if r.returncode == 0:
        extra = "  (permissions pre-approved)" if "skip-permissions" in launch else ""
        print(f"  {_c('32')}+{_c('0')} launcher on your desktop{extra}")
    else:
        tail = (r.stderr or r.stdout).strip().splitlines()
        print(f"  (couldn't place the launcher this time: {tail[-1] if tail else 'embodiment skipped'})")


def _uninstall(target: Path, payload: Path) -> None:
    """Remove Microwave files still byte-identical to what was installed: never
    touch a file you edited, never touch your own atoms. Restores a backed-up
    pre-commit hook if we made one."""
    removed = 0

    def rm_if_untouched(t: Path, s: Path) -> None:
        nonlocal removed
        if t.is_file() and s.is_file() and t.read_bytes() == s.read_bytes():
            t.unlink()
            removed += 1

    for d in PAYLOAD_DIRS:
        src = payload / d
        if not src.is_dir():
            continue
        for root, _dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            if "icons" in rel.parts or "__pycache__" in rel.parts:
                continue
            for name in files:
                if name.endswith((".pyc", ".pyo")):
                    continue
                rm_if_untouched(target / d / rel / name, src / rel / name)
    rm_if_untouched(target / ".github" / "workflows" / "gates.yml",
                    payload / ".github" / "workflows" / "gates.yml")
    for name in ("LICENSE", "NOTICE.md", "CLAUDE.md", "AGENTS.md"):
        rm_if_untouched(target / name, payload / name)
    rm_if_untouched(target / "wiki" / "agents" / "microwave.md",
                    payload / "wiki" / "agents" / "microwave.md")
    idx = target / "wiki" / "INDEX.md"
    if idx.is_file() and idx.read_text(encoding="utf-8") == WIKI_INDEX:
        idx.unlink()
        removed += 1
    co = target / "CODEOWNERS"
    co_src = payload / "CODEOWNERS"
    if co.is_file() and co_src.is_file():
        installed = co_src.read_text(encoding="utf-8").replace(
            "@microphage-create", "@your-gatekeeper")
        if co.read_text(encoding="utf-8") == installed:
            co.unlink()
            removed += 1
    hook = target / ".git" / "hooks" / "pre-commit"
    src_hook = payload / "hooks" / "pre-commit"
    backup = target / ".git" / "hooks" / "pre-commit.pre-microwave"
    if hook.is_file() and src_hook.is_file() and hook.read_bytes() == src_hook.read_bytes():
        hook.unlink()
        removed += 1
        if backup.is_file():
            shutil.copy2(backup, hook)
            backup.unlink()
            print("  restored your previous pre-commit hook")
    for d in ("flows", "templates", "techniques", "slop", "gates", "embodiment",
              "hooks", "harness", "wiki/agents", "wiki/adr", "wiki/projects",
              "wiki/_staging", "wiki/_archive", "wiki", ".github/workflows", ".github"):
        p = target / d
        if p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    print(f"\nUninstalled: removed {removed} untouched Microwave file(s) from")
    print(f"{target}")
    print("Your own atoms, your edits, and anything you changed were kept.")
    print("Embodied agents: run `python embodiment/embody.py <card> --remove` first")
    print("to also remove their desktop profiles.")


def main() -> None:
    target = Path(os.environ.get("MICROWAVE_TARGET", os.getcwd())).resolve()
    payload = _payload()

    if "--help" in sys.argv or "-h" in sys.argv:
        print("microwave-method - drop Microwave into the current repo.\n")
        print("  uvx microwave-method              install (additive, asks before side effects)")
        print("  uvx microwave-method --dry-run    show what would be written, write nothing")
        print("  uvx microwave-method --uninstall  remove what it installed (keeps your edits)")
        print("\nEnv: MICROWAVE_TARGET=<dir> targets another repo; MICROWAVE_NO_LAUNCH=1 is")
        print("     CI-safe; MICROWAVE_SHADOW=1 makes gates report without blocking.")
        return

    if "--dry-run" in sys.argv or os.environ.get("MICROWAVE_DRY_RUN") == "1":
        planned = _install_plan(target, payload)
        appends = []
        for ctx in ("CLAUDE.md", "AGENTS.md"):
            dst = target / ctx
            if (dst.exists() and (payload / ctx).is_file()
                    and "runs on Microwave" not in dst.read_text(encoding="utf-8", errors="replace")):
                appends.append(dst)
        print(f"\nMicrowave dry-run in {target}\n")
        print(f"{len(planned)} file(s) would be CREATED (an existing file is never overwritten):")
        for p in planned:
            print(f"  + {p.relative_to(target)}")
        if appends:
            print("\nand its session-start block would be APPENDED to your existing:")
            for p in appends:
                print(f"  ~ {p.relative_to(target)}  (appended, not overwritten)")
        print("\nNo files written. Run without --dry-run to install. On your yes it")
        print("would also git-init if needed, wire the pre-commit hook, offer a")
        print("desktop icon, and open the welcome flow. Uninstall: --uninstall.")
        return

    if "--uninstall" in sys.argv:
        _uninstall(target, payload)
        return

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
    # session-start context for whichever agent runs here (Claude Code reads
    # CLAUDE.md; Codex/Cursor read AGENTS.md). Append, never clobber, an existing one.
    for ctx in ("CLAUDE.md", "AGENTS.md"):
        dst = target / ctx
        src = payload / ctx
        if not src.is_file():
            continue
        if not dst.exists():
            shutil.copy2(src, dst)
        elif "runs on Microwave" not in dst.read_text(encoding="utf-8"):
            with dst.open("a", encoding="utf-8") as f:
                f.write("\n\n---\n\n" + src.read_text(encoding="utf-8"))
    zero_src = payload / "wiki" / "agents" / "microwave.md"
    zero = wiki / "agents" / "microwave.md"
    if not zero.exists() and zero_src.is_file():
        shutil.copy2(zero_src, zero)
    _ok(f"{copied} files installed: memory, quality gates, and CODEOWNERS in place")

    # Side effects (git init, hook, launching your agent) only with a yes.
    proceed = _confirm(
        "Set up git here (if needed), install the pre-commit check, and start the "
        "guided setup now?")
    if proceed:
        if not _is_git_repo(target):
            init = subprocess.run(["git", "-C", str(target), "init"],
                                  capture_output=True, text=True)
            _ok("git repo initialized" if init.returncode == 0
                else "git not found (install git so the gates can guard the repo)")
        if _is_git_repo(target):
            _ok(_wire_hook(target, payload))
        _embody_agent_zero(target, payload)
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
