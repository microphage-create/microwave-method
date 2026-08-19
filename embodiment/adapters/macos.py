"""macOS adapter: iTerm2 Dynamic Profile (additive, zero-risk) + minimal
.app bundle launcher with .icns, so the agent exists in Dock/Spotlight.

Falls back to Terminal.app in the launcher script when iTerm2 is absent.
"""
from __future__ import annotations

import json
import plistlib
import shlex
import shutil
import stat
from pathlib import Path

DYNAMIC = Path.home() / "Library/Application Support/iTerm2/DynamicProfiles"
APPS = Path.home() / "Applications"


def _hexpair(c: str) -> dict:
    r, g, b = (int(c.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return {"Red Component": r, "Green Component": g, "Blue Component": b}


def _dynamic_profile(ident) -> dict:
    launch = ident.launch or ""
    cmd = f"cd '{ident.repo}'" + (f" && {launch}" if launch else "; exec $SHELL")
    return {"Profiles": [{
        "Name": ident.name,
        "Guid": ident.guid,
        "Custom Command": "Yes",
        "Command": f"/bin/zsh -lc \"{cmd}\"",
        "Background Color": _hexpair(ident.bg),
        "Foreground Color": _hexpair(ident.fg),
        "Cursor Color": _hexpair(ident.accent),
        "Badge Text": ident.name,
    }]}


def _bundle(ident, icns: Path) -> Path:
    app = APPS / f"{ident.name}.app"
    macos_dir = app / "Contents/MacOS"
    res_dir = app / "Contents/Resources"
    macos_dir.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)
    plistlib.dump({
        "CFBundleName": ident.name,
        "CFBundleIdentifier": f"dev.microwave.{ident.slug}",
        "CFBundleExecutable": "run",
        "CFBundleIconFile": "icon.icns",
        "CFBundlePackageType": "APPL",
    }, (app / "Contents/Info.plist").open("wb"))
    shutil.copyfile(icns, res_dir / "icon.icns")

    # Fallback launch script for Terminal.app: a plain .command file, so no
    # nested AppleScript quoting is ever needed.
    launch = ident.launch or "exec $SHELL"
    command_file = res_dir / "launch.command"
    command_file.write_text(f"#!/bin/zsh\ncd {shlex.quote(str(ident.repo))}\n{launch}\n",
                            encoding="utf-8")
    command_file.chmod(command_file.stat().st_mode | stat.S_IEXEC)

    runner = macos_dir / "run"
    runner.write_text(app_script(ident, command_file), encoding="utf-8")
    runner.chmod(runner.stat().st_mode | stat.S_IEXEC)
    return app


def app_script(ident, command_file: Path) -> str:
    # ident.name is constrained by gate_schema (letters, digits, space, _.-):
    # safe inside AppleScript double quotes. The Terminal fallback opens the
    # .command file instead of inlining any shell string.
    return f"""#!/bin/zsh
# Launcher for agent '{ident.name}': open its themed terminal profile.
if [ -d "/Applications/iTerm.app" ]; then
  osascript -e 'tell application "iTerm" to create window with profile "{ident.name}"' \\
            -e 'tell application "iTerm" to activate'
else
  open -b com.apple.Terminal {shlex.quote(str(command_file))}
fi
"""


def apply(ident, dry_run: bool = False) -> None:
    profile_path = DYNAMIC / f"microwave-{ident.slug}.json"
    if dry_run:
        ident.png_bytes()  # validate the icon source, write nothing
        print(f"[macos] would write dynamic profile {profile_path}")
        print(f"[macos] would create {APPS / (ident.name + '.app')}")
        return
    icns = ident.write_icns()
    DYNAMIC.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(_dynamic_profile(ident), indent=2),
                            encoding="utf-8")
    print(f"[macos] iTerm2 dynamic profile: {profile_path}")
    app = _bundle(ident, icns)
    print(f"[macos] launcher bundle: {app}")


def remove(ident, dry_run: bool = False) -> None:
    profile_path = DYNAMIC / f"microwave-{ident.slug}.json"
    app = APPS / f"{ident.name}.app"
    if dry_run:
        print(f"[macos] would remove {profile_path} and {app}")
        return
    if profile_path.exists():
        profile_path.unlink()
    if app.exists():
        shutil.rmtree(app)
    print("[macos] removed")
