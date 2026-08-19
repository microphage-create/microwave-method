"""embody: give an agent its body (ADR-004).

Reads the embodiment block of an agent card, compiles it into native OS
artifacts through one adapter, then flips `embodied: true` in the card.

Usage:
    python embodiment/embody.py <agent-card.md> [--os windows|macos|linux]
                                [--dry-run] [--remove]

Stdlib only. Icon pipeline: one source PNG (256x256 recommended) per agent;
.ico and .icns containers are written around the PNG bytes directly (both
formats accept embedded PNG), no imaging library required.
"""
from __future__ import annotations

import argparse
import platform
import struct
import sys
import uuid
from pathlib import Path

import re

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "gates"))
from _lib import GateError, get, read_frontmatter  # noqa: E402
import gate_schema as schema  # noqa: E402  (SLUG_RE / NAME_RE / LAUNCH_FORBIDDEN)

NAMESPACE = uuid.UUID("6d1c706f-7761-7665-6d65-74686f640000")  # stable per slug


class Identity:
    """Reads and REVALIDATES the identity fields it consumes.

    embody.py can be run standalone, so it must not assume gate_schema ran
    first: slug/name/palette/launch feed file paths and shell commands, and
    are re-checked here with the same rules (defense in depth)."""

    def __init__(self, card_path: Path):
        fm, _ = read_frontmatter(card_path)
        self.card_path = card_path
        self.slug = str(get(fm, "slug"))
        if not schema.SLUG_RE.match(self.slug):
            raise GateError(f"{card_path.name}: slug {self.slug!r} must match "
                            f"{schema.SLUG_RE.pattern} (it names files and profiles)")
        self.name = str(get(fm, "embodiment.display_name"))
        if not schema.NAME_RE.match(self.name):
            raise GateError(f"{card_path.name}: display_name {self.name!r} must "
                            f"match {schema.NAME_RE.pattern}")
        self.icon_src = ROOT / str(get(fm, "embodiment.icon"))
        self.bg = str(get(fm, "embodiment.palette.bg"))
        self.fg = str(get(fm, "embodiment.palette.fg"))
        self.accent = str(get(fm, "embodiment.palette.accent"))
        for label, val in (("bg", self.bg), ("fg", self.fg), ("accent", self.accent)):
            if not re.match(r"^#[0-9a-fA-F]{6}$", val):
                raise GateError(f"{card_path.name}: palette.{label}={val!r} is not #rrggbb")
        self.launch = str(get(fm, "embodiment.launch") or "").strip()
        if self.launch and schema.LAUNCH_FORBIDDEN.search(self.launch):
            raise GateError(f"{card_path.name}: embodiment.launch contains a shell "
                            f"metacharacter; keep it to a bare command and arguments")
        self.repo = ROOT
        self.guid = str(uuid.uuid5(NAMESPACE, self.slug))
        self.build_dir = ROOT / "embodiment" / "icons" / "build"

    # ---- color helpers -------------------------------------------------
    @staticmethod
    def _rgb(hexstr: str) -> tuple[int, int, int]:
        h = hexstr.lstrip("#")
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    @staticmethod
    def _hex(rgb: tuple[int, int, int]) -> str:
        return "#%02X%02X%02X" % rgb

    def mix(self, a: str, b: str, t: float) -> str:
        ra, rb = self._rgb(a), self._rgb(b)
        return self._hex(tuple(round(x + (y - x) * t) for x, y in zip(ra, rb)))

    def scheme(self) -> dict:
        """Derive a 16-color terminal scheme from the 3-color palette."""
        m = self.mix
        return {
            "name": self.name,
            "background": self.bg, "foreground": self.fg,
            "cursorColor": self.accent, "selectionBackground": m(self.bg, self.accent, 0.25),
            "black": self.bg, "white": self.fg,
            "brightBlack": m(self.bg, self.fg, 0.35), "brightWhite": m(self.fg, "#FFFFFF", 0.6),
            "red": m("#C05B4D", self.accent, 0.15), "brightRed": m("#E07A6B", self.accent, 0.15),
            "green": m("#4E9A6E", self.accent, 0.15), "brightGreen": m("#6FC08F", self.accent, 0.15),
            "yellow": m("#C7A94F", self.accent, 0.2), "brightYellow": m("#E0C878", self.accent, 0.2),
            "blue": m("#5B7FA6", self.accent, 0.25), "brightBlue": m("#7FA3C8", self.accent, 0.25),
            "purple": m("#8B7AA6", self.accent, 0.25), "brightPurple": m("#AC9CC8", self.accent, 0.25),
            "cyan": m(self.accent, self.fg, 0.15), "brightCyan": m(self.accent, "#FFFFFF", 0.3),
        }

    # ---- icon containers (stdlib only) ---------------------------------
    def png_bytes(self) -> bytes:
        if not self.icon_src.exists():
            raise GateError(f"icon source not found: {self.icon_src}")
        data = self.icon_src.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            raise GateError(f"{self.icon_src} is not a PNG")
        w = int.from_bytes(data[16:20], "big")
        h = int.from_bytes(data[20:24], "big")
        if (w, h) != (256, 256):
            raise GateError(f"{self.icon_src} is {w}x{h}; the source icon must be "
                            f"exactly 256x256 (the .ico/.icns containers declare it)")
        return data

    def write_ico(self) -> Path:
        png = self.png_bytes()
        out = self.build_dir / f"{self.slug}.ico"
        out.parent.mkdir(parents=True, exist_ok=True)
        # ICONDIR + one ICONDIRENTRY wrapping the PNG (0 = 256px)
        header = struct.pack("<HHH", 0, 1, 1)
        entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(png), 22)
        out.write_bytes(header + entry + png)
        return out

    def write_icns(self) -> Path:
        png = self.png_bytes()
        out = self.build_dir / f"{self.slug}.icns"
        out.parent.mkdir(parents=True, exist_ok=True)
        body = b"ic08" + struct.pack(">I", 8 + len(png)) + png  # 256x256 PNG
        out.write_bytes(b"icns" + struct.pack(">I", 8 + len(body)) + body)
        return out

    def set_embodied(self, value: bool) -> None:
        """Flip the flag inside the frontmatter block only."""
        lines = self.card_path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        delims = [i for i, l in enumerate(lines) if l.strip() == "---"]
        if len(delims) < 2:
            raise GateError(f"{self.card_path}: no frontmatter block")
        flag = "true" if value else "false"
        for i in range(delims[0] + 1, delims[1]):
            if lines[i].strip().startswith("embodied:"):
                indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
                lines[i] = f"{indent}embodied: {flag}\n"
                self.card_path.write_text("".join(lines), encoding="utf-8")
                return
        raise GateError(f"{self.card_path}: 'embodied' key not found in frontmatter")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("card")
    ap.add_argument("--os", dest="os_name",
                    choices=["windows", "macos", "linux"], default=None)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--remove", action="store_true")
    args = ap.parse_args()

    os_name = args.os_name or {
        "Windows": "windows", "Darwin": "macos", "Linux": "linux",
    }.get(platform.system())
    if os_name is None:
        print(f"[embody] FAIL: unsupported platform: {platform.system()}")
        sys.exit(1)

    if os_name == "windows":
        from adapters import windows as adapter
    elif os_name == "macos":
        from adapters import macos as adapter
    else:
        from adapters import linux as adapter

    try:
        ident = Identity(Path(args.card).resolve())
        if args.remove:
            adapter.remove(ident, dry_run=args.dry_run)
            if not args.dry_run:
                ident.set_embodied(False)
            print(f"[embody] removed body of '{ident.name}'")
        else:
            adapter.apply(ident, dry_run=args.dry_run)
            if not args.dry_run:
                ident.set_embodied(True)
            print(f"[embody] '{ident.name}' embodied"
                  + (" (dry-run, no flag written)" if args.dry_run else ""))
    except (GateError, OSError, ValueError, RuntimeError) as e:
        print(f"[embody] FAIL: {e}")
        sys.exit(1)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
