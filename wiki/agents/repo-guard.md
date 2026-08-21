---
type: agent-card
kind: context
name: Repo Guard
slug: repo-guard
repo: microwave-method
status: active
blast_radius: read
mission: Guard the microwave-method repo's own conventions when an agent works on it, reading and reporting violations without writing.
inputs: [the working tree, a staged change]
outputs: [a pass or a list of convention violations to fix]
definition_path: flows/repo-guard.md
owner: "@microphage-create"
synonyms: [repo guard, codebase context, conventions, house style, self-governance]
anti_dup_rationale: "A context agent bound to the microwave-method repo, not a transversal service: it carries THIS repo's conventions (stdlib-only runtime, the gate discipline, the no-em-dash style) and is never a duplicate of factory (which makes agents) or librarian (which curates the wiki), which are services with no repo (LRN-007)."
created_in_minutes: 0
brief:
  success_criteria:
    - criterion: The shipped tool declares no runtime dependency (stdlib only, ADR-007)
      check: "python -c \"import tomllib,sys; d=tomllib.load(open('pyproject.toml','rb')); sys.exit(0 if d['project']['dependencies']==[] else 1)\""
    - criterion: The wiki gates pass on the estate
      check: "python gates/gate_wiki.py && python gates/gate_slop.py && python gates/gate_docs.py"
    - criterion: The code is lint and type clean
      check: "ruff check . && mypy"
    - criterion: The working tree carries no em-dash in prose or code (house style), the fixture and imported zones aside
      check: "python -c \"import sys,pathlib; ex={'.git','tests','templates','techniques','slop','_archive'}; bad=[str(p) for p in pathlib.Path('.').rglob('*') if p.suffix in ('.md','.py') and not ex & set(p.parts) and '\\u2014' in p.read_text(encoding='utf-8', errors='ignore')]; sys.exit(1 if bad else 0)\""
  volume_cap: "1 working tree per run"
  abort_conditions:
    - a check names a tool that is not installed; report the missing tool, do not guess a pass
---

# Repo Guard

## Mission

The context agent for the microwave-method repo. When any agent (or the
maintainer) works on this repo, Repo Guard carries the repo's conventions and
checks a change against them before it ships. It reads and reports; it never
writes the fix itself (that stays the author's, or another agent's, job).

## Scope

**In**: the conventions that make THIS repo what it is, and that a gate does not
already enforce end to end: the stdlib-only runtime (ADR-007), the wiki gates
staying green, the code staying lint and type clean, and the house style (no
em-dash). Reporting which of these a working tree violates.

**Out**: making agents (that is the factory), curating the wiki (the librarian),
or governing any repo other than microwave-method. A context agent guards one
repo and only that repo.

## Interfaces

Reads the working tree and runs the checks in `brief.success_criteria`. Writes
nothing. Calls no other agent; its checks are self-contained shell commands.

## Notes

This is the repo's own context agent: the "one guard per repo" the method sells,
pointed at the method's own repo. It is the smallest honest demonstration that a
context agent is a real, gate-passing artifact, not only a slide.
