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


def _wt_launch_args(name: str) -> str:
    """The exact 'open Windows Terminal on this profile' command line, shared
    by the desktop shortcut and the live verification launch so testing one
    genuinely tests the other."""
    return f'/c start "" wt.exe -p "{name}"'


def _desktop_lnk(ident, ico: Path) -> Path:
    # ident.name is revalidated by Identity (no quotes); everything else is
    # escaped anyway: defense in depth.
    lnk = Path.home() / "Desktop" / f"{ident.name}.lnk"
    # wt.exe is a Windows App Execution Alias (a reparse-point stub). Pointing a
    # .lnk's TargetPath directly at it - even at the real stub under WindowsApps -
    # launches nothing from Explorer for some users: a known Windows quirk where
    # shell shortcut resolution doesn't reliably follow App Execution Aliases.
    # cmd.exe is a real binary; Explorer launches it fine, and cmd's own PATH
    # lookup resolves the wt.exe alias correctly. `start ""` detaches the
    # terminal so cmd exits immediately instead of lingering.
    ps = (
        f"$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{_psq(lnk)}');"
        f"$s.TargetPath='{_psq(_cmd_exe())}';"
        f"$s.Arguments='{_psq(_wt_launch_args(ident.name))}';"
        f"$s.IconLocation='{_psq(ico)}';"
        f"$s.WindowStyle=7;"  # minimized: hides the flash of the cmd.exe window
        f"$s.Save()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    return lnk


def _cmd_exe() -> str:
    root = os.environ.get("SystemRoot") or r"C:\Windows"
    return str(Path(root) / "System32" / "cmd.exe")


def _visible_windows() -> set:
    """Top-level visible window handles, right now. stdlib-only (ctypes), used
    to detect 'did a new window just appear' without extra dependencies."""
    import ctypes
    user32 = ctypes.windll.user32
    hwnds: list = []
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)

    def _collect(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            hwnds.append(hwnd)
        return True

    user32.EnumWindows(WNDENUMPROC(_collect), 0)
    return set(hwnds)


def verify_launch(ident, timeout: float = 6.0) -> bool:
    """Actually open the shortcut's target command and watch for a new
    top-level window within `timeout` seconds. This is the same command the
    desktop .lnk runs, so a pass here means the .lnk works too, not a guess."""
    try:
        before = _visible_windows()
    except OSError:
        return False
    try:
        # shell=True on Windows runs this through cmd.exe (COMSPEC) itself, so
        # the string is parsed exactly as cmd.exe parses it from a shortcut's
        # Arguments field: no argv-splitting mismatch between the two paths.
        subprocess.Popen(_wt_launch_args(ident.name)[len("/c "):], shell=True,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        return False
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.3)
        try:
            if _visible_windows() - before:
                return True
        except OSError:
            continue
    return False


def apply(ident, dry_run: bool = False) -> bool | None:
    """Returns True/False once the launcher has been live-tested, None in
    dry-run (nothing was created, so nothing to test)."""
    if dry_run:
        ident.png_bytes()  # validate the icon source, write nothing
        print(f"[windows] would write {ident.build_dir / (ident.slug + '-' + ident.icon_src.stem + '.ico')}")
        print(f"[windows] would add scheme+profile '{ident.name}' to {WT_SETTINGS}")
        print(f"[windows] would create desktop shortcut '{ident.name}.lnk'")
        return None

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

    verified = verify_launch(ident)
    print(f"[windows] launcher {'verified: a new window opened' if verified else 'could not be verified: no new window detected'}")
    return verified


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
