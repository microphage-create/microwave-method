"""Linux adapter: freedesktop .desktop entry + icon, terminal auto-detected.

Supported terminals: kitty, wezterm, gnome-terminal; generic fallback via
$TERMINAL. The PNG icon is used natively (no conversion needed).
"""
from __future__ import annotations

import shlex
import shutil
from pathlib import Path

APPS = Path.home() / ".local/share/applications"
ICONS = Path.home() / ".local/share/icons"


def _terminal_cmd(ident) -> str:
    """Exec= lines get no shell expansion (freedesktop spec), so only
    concrete binaries found on PATH are usable; $TERMINAL would be run
    literally and can never work."""
    launch = ident.launch or "exec $SHELL"
    inner = f"cd {shlex.quote(str(ident.repo))} && {launch}"
    if shutil.which("kitty"):
        return f"kitty --title '{ident.name}' bash -lc \"{inner}\""
    if shutil.which("wezterm"):
        return f"wezterm start -- bash -lc \"{inner}\""
    if shutil.which("gnome-terminal"):
        return f"gnome-terminal --title='{ident.name}' -- bash -lc \"{inner}\""
    for candidate in ("x-terminal-emulator", "xdg-terminal-exec", "konsole", "xterm"):
        if shutil.which(candidate):
            return f"{candidate} -e bash -lc \"{inner}\""
    raise RuntimeError(
        "no known terminal found (kitty, wezterm, gnome-terminal, "
        "x-terminal-emulator, xdg-terminal-exec, konsole, xterm): "
        "install one or open an issue naming yours")


def apply(ident, dry_run: bool = False) -> None:
    ident.png_bytes()  # same icon contract as the other adapters
    desktop_file = APPS / f"microwave-{ident.slug}.desktop"
    icon_dst = ICONS / f"microwave-{ident.slug}.png"
    entry = (
        "[Desktop Entry]\n"
        "Type=Application\n"
        f"Name={ident.name}\n"
        f"Comment=Microwave agent: {ident.slug}\n"
        f"Exec={_terminal_cmd(ident)}\n"
        f"Icon={icon_dst}\n"
        "Terminal=false\n"
        "Categories=Development;\n"
    )
    if dry_run:
        print(f"[linux] would write {desktop_file} and {icon_dst}")
        return
    APPS.mkdir(parents=True, exist_ok=True)
    ICONS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ident.icon_src, icon_dst)
    desktop_file.write_text(entry, encoding="utf-8")
    desktop_file.chmod(0o755)
    desktop_dir = Path.home() / "Desktop"
    if desktop_dir.is_dir():
        desktop_copy = desktop_dir / desktop_file.name
        shutil.copyfile(desktop_file, desktop_copy)
        desktop_copy.chmod(0o755)
    print(f"[linux] desktop entry: {desktop_file}")


def remove(ident, dry_run: bool = False) -> None:
    targets = [
        APPS / f"microwave-{ident.slug}.desktop",
        ICONS / f"microwave-{ident.slug}.png",
        Path.home() / "Desktop" / f"microwave-{ident.slug}.desktop",
    ]
    if dry_run:
        print("[linux] would remove: " + ", ".join(str(t) for t in targets))
        return
    for t in targets:
        if t.exists():
            t.unlink()
    print("[linux] removed")
