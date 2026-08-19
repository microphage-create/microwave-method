"""Shared helpers for Microwave gates. Python stdlib only (ADR-007).

Parses the YAML subset defined for card frontmatter:
- scalar `key: value` (bare, "quoted", 'quoted', numbers, booleans)
- nested maps by 2-space indentation (tabs are rejected)
- block lists of scalars (`- item`) and of maps (`- key: value` + indented keys)
- inline lists `[a, b, c]` (quoted items may contain commas)

Duplicate keys are rejected, not silently overwritten.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import NoReturn

FM_DELIM = "---"

# Make gate output safe on non-UTF-8 consoles (Windows cp1252): a rejection
# message that quotes a fancy character must not itself crash with
# UnicodeEncodeError instead of printing the FAIL line.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass


class GateError(Exception):
    pass


def fail(gate: str, msg: str) -> NoReturn:
    print(f"[{gate}] FAIL: {msg}")
    sys.exit(1)


def ok(gate: str, msg: str = "green") -> None:
    print(f"[{gate}] OK: {msg}")


def read_text(path: Path) -> str:
    """Read a file as UTF-8 (BOM-tolerant), turning IO and encoding errors
    into an actionable GateError instead of a raw traceback."""
    try:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        raise GateError(f"{path}: file not found")
    except OSError as e:
        raise GateError(f"{path}: cannot read file ({e.strerror or e})")
    except UnicodeDecodeError:
        raise GateError(f"{path}: not valid UTF-8 (re-save the file as UTF-8)")


def read_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body) of a markdown file."""
    text = read_text(path)
    lines = text.splitlines()
    if not lines or lines[0].strip() != FM_DELIM:
        raise GateError(f"{path}: no frontmatter (file must start with ---)")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == FM_DELIM)
    except StopIteration:
        raise GateError(f"{path}: unterminated frontmatter")
    fm = parse_yaml_subset(lines[1:end])
    body = "\n".join(lines[end + 1 :])
    return fm, body


def _split_inline(inner: str) -> list[str]:
    """Split an inline-list body on commas that are not inside quotes."""
    items, buf, quote = [], [], ""
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            buf.append(ch)
        elif ch == ",":
            items.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if quote:
        raise GateError(f"unterminated quote in inline list: [{inner}]")
    items.append("".join(buf))
    return items


def _scalar(raw: str):
    raw = raw.strip()
    if raw.startswith("["):
        if not raw.endswith("]"):
            raise GateError(f"malformed inline list (no closing ]): {raw!r}")
        inner = raw[1:-1].strip()
        return [] if not inner else [_scalar(x) for x in _split_inline(inner)]
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if raw in ("true", "True"):
        return True
    if raw in ("false", "False"):
        return False
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    return raw


def _set(container: dict, key: str, value, line: str) -> None:
    if key in container:
        raise GateError(f"duplicate key {key!r} in frontmatter: {line!r}")
    container[key] = value


def parse_yaml_subset(lines: list[str]) -> dict:
    """Indentation-driven recursive descent over the documented subset."""
    root: dict = {}
    stack: list[tuple[int, object]] = [(-1, root)]

    def top_for(indent: int):
        while stack and stack[-1][0] >= indent:
            stack.pop()
        return stack[-1][1]

    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.strip().startswith("#"):
            continue
        lead = line[: len(line) - len(line.lstrip())]
        if "\t" in lead:
            raise GateError(f"tab indentation not allowed, use 2 spaces: {line!r}")
        indent = len(lead)
        stripped = line.strip()
        container = top_for(indent)

        if stripped.startswith("- "):
            item_raw = stripped[2:].strip()
            if not isinstance(container, list):
                raise GateError(f"list item outside a list context: {line!r}")
            if ":" in item_raw and not item_raw.startswith("["):
                key, _, val = item_raw.partition(":")
                entry: dict = {}
                container.append(entry)
                entry[key.strip()] = _scalar(val) if val.strip() else ""
                stack.append((indent + 1, entry))
            else:
                container.append(_scalar(item_raw))
            continue

        key, sep, val = stripped.partition(":")
        if not sep:
            raise GateError(f"unparseable line in frontmatter: {line!r}")
        key = key.strip()
        val = val.strip()
        if not isinstance(container, dict):
            raise GateError(f"map key inside a scalar list: {line!r}")
        if val:
            _set(container, key, _scalar(val), line)
        else:
            j = i
            while j < len(lines) and not lines[j].strip():
                j += 1
            nxt = lines[j].strip() if j < len(lines) else ""
            child: object = [] if nxt.startswith("- ") else {}
            _set(container, key, child, line)
            stack.append((indent, child))
    return root


def get(fm: dict, dotted: str):
    """fm['a']['b'] via 'a.b', returns None when absent."""
    cur: object = fm
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def repo_root(start: Path | None = None) -> Path:
    p = (start or Path.cwd()).resolve()
    for cand in (p, *p.parents):
        if (cand / "wiki" / "INDEX.md").exists():
            return cand
    raise GateError("cannot locate repo root (wiki/INDEX.md not found)")


def index_lines(root: Path) -> list[str]:
    idx = read_text(root / "wiki" / "INDEX.md")
    return [l.strip() for l in idx.splitlines() if l.strip().startswith("- [")]


def tokenize(text: str) -> set[str]:
    stop = {
        "the", "a", "an", "of", "for", "and", "or", "with", "to", "in", "on",
        "its", "it", "is", "are", "that", "this", "by", "one", "per", "et",
        "de", "la", "le", "les", "un", "une", "des", "du",
    }
    return {w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in stop}
