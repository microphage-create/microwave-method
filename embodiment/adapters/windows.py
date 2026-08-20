"""Windows adapter: Windows Terminal profile + color scheme + desktop .lnk.

Additive and idempotent. Timestamped backup of settings.json before any edit.
Override the settings path with the MICROWAVE_WT_SETTINGS env var if needed.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

WT_SETTINGS = Path(os.environ.get(
    "MICROWAVE_WT_SETTINGS",
    Path(os.environ.get("LOCALAPPDATA", "")) /
    "Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/settings.json",
))


def _strip_jsonc(text: str) -> str:
    """Windows Terminal ships settings.json as JSONC: strip // and /* */
    comments (outside strings) and trailing commas so json can parse it.
    Comments are NOT preserved on rewrite; the timestamped backup keeps the
    original."""
    out, i, in_str, esc = [], 0, False, False
    pending = None  # index in `out` of a comma that may be trailing (outside strings)
    while i < len(text):
        ch = text[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str, esc, pending = True, False, None  # a value ends any trailing comma
            out.append(ch)
            i += 1
        elif text.startswith("//", i):
            i = text.find("\n", i)
            i = len(text) if i == -1 else i
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = len(text) if j == -1 else j + 2
        elif ch == ",":
            out.append(ch)
            pending = len(out) - 1
            i += 1
        elif ch in "}]":
            if pending is not None:
                out[pending] = ""  # drop a genuine trailing comma
            out.append(ch)
            pending = None
            i += 1
        elif ch.isspace():
            out.append(ch)  # whitespace keeps a pending comma alive
            i += 1
        else:
            out.append(ch)
            pending = None
            i += 1
    # trailing commas are handled in-scan (string-aware); a comma inside a string
    # value like "Solarized, ]" is never touched.
    return "".join(out)


def _load() -> dict:
    if not WT_SETTINGS.exists():
        raise RuntimeError(f"Windows Terminal settings not found: {WT_SETTINGS} "
                           f"(set MICROWAVE_WT_SETTINGS to override)")
    raw = WT_SETTINGS.read_text(encoding="utf-8-sig")
    try:
        data = json.loads(_strip_jsonc(raw))
    except json.JSONDecodeError as e:
        raise RuntimeError(f"cannot parse {WT_SETTINGS}: {e}. "
                           f"Fix the file or point MICROWAVE_WT_SETTINGS elsewhere.")
    profiles = data.get("profiles")
    if isinstance(profiles, list):  # legacy schema: profiles was a bare list
        data["profiles"] = {"list": profiles}
    return data


def _save(data: dict) -> Path:
    bak = WT_SETTINGS.with_name(WT_SETTINGS.name + ".bak." + str(int(time.time())))
    shutil.copyfile(WT_SETTINGS, bak)
    WT_SETTINGS.write_text(json.dumps(data, indent=4, ensure_ascii=False),
                           encoding="utf-8")
    return bak


def _psq(s: object) -> str:
    """Escape for a PowerShell single-quoted string ('' = literal ')."""
    return str(s).replace("'", "''")


def _profile(ident, ico: Path) -> dict:
    launch = ident.launch or ""
    # defense in depth: launch is interpolated into a PowerShell command, so it
    # must carry no shell metacharacter. gate_schema (LAUNCH_FORBIDDEN) enforces
    # this on the card; re-check here in case embodiment runs on an ungated card.
    if launch and set(";&|`$<>(){}[]\"'\\\n\r").intersection(launch):
        raise RuntimeError("embodiment.launch has a shell metacharacter; it must "
                           "pass gate_schema before embodiment")
    inner = f"cd '{_psq(ident.repo)}'" + (f"; {launch}" if launch else "")
    return {
        "name": ident.name,
        "guid": "{" + ident.guid + "}",
        "colorScheme": ident.name,
        "icon": str(ico),
        "cursorShape": "bar",
        "commandline": f"pwsh.exe -NoExit -Command \"{inner}\"",
    }


def _desktop_lnk(ident, ico: Path) -> Path:
    # ident.name is revalidated by Identity (no quotes); everything else is
    # escaped anyway: defense in depth.
    lnk = Path.home() / "Desktop" / f"{ident.name}.lnk"
    # wt.exe is a Windows App Execution Alias: a .lnk with TargetPath='wt.exe'
    # saves fine but launches NOTHING from Explorer. Point at the real stub under
    # WindowsApps so a double-click actually opens the terminal.
    local = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
    wt = Path(local) / "Microsoft" / "WindowsApps" / "wt.exe"
    target = str(wt) if wt.exists() else "wt.exe"
    ps = (
        f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{_psq(lnk)}');"
        f"$s.TargetPath='{_psq(target)}';"
        f"$s.Arguments='-p \"{_psq(ident.name)}\"';"
        f"$s.IconLocation='{_psq(ico)}';"
        f"$s.Save()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return lnk


def apply(ident, dry_run: bool = False) -> None:
    if dry_run:
        ident.png_bytes()  # validate the icon source, write nothing
        print(f"[windows] would write {ident.build_dir / (ident.slug + '-' + ident.icon_src.stem + '.ico')}")
        print(f"[windows] would add scheme+profile '{ident.name}' to {WT_SETTINGS}")
        print(f"[windows] would create desktop shortcut '{ident.name}.lnk'")
        return

    ico = ident.write_ico()
    scheme = ident.scheme()
    profile = _profile(ident, ico)

    data = _load()
    schemes = data.setdefault("schemes", [])
    schemes[:] = [s for s in schemes if s.get("name") != scheme["name"]]
    schemes.append(scheme)
    plist = data.setdefault("profiles", {}).setdefault("list", [])
    plist[:] = [p for p in plist if p.get("guid") != profile["guid"]]
    plist.append(profile)
    bak = _save(data)
    print(f"[windows] scheme+profile '{ident.name}' written (backup: {bak.name})")

    lnk = _desktop_lnk(ident, ico)
    print(f"[windows] desktop shortcut: {lnk}")


def remove(ident, dry_run: bool = False) -> None:
    if dry_run:
        print(f"[windows] would remove scheme/profile/shortcut '{ident.name}'")
        return
    data = _load()
    data["schemes"] = [s for s in data.get("schemes", []) if s.get("name") != ident.name]
    plist = data.get("profiles", {}).get("list", [])
    plist[:] = [p for p in plist if p.get("guid") != "{" + ident.guid + "}"]
    bak = _save(data)
    lnk = Path.home() / "Desktop" / f"{ident.name}.lnk"
    if lnk.exists():
        lnk.unlink()
    print(f"[windows] removed (backup: {bak.name})")
