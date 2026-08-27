# Limits

What Microwave does not do, what is not proven yet, and when not to install it.
The README sells the method; this page is the counter-argument, kept in the repo
so a reader does not have to reconstruct it. If a claim elsewhere in the docs
contradicts this page, this page is right and the other one is a bug.

## 1. The guaranteed perimeter is three files wide

Everything the method can enforce without anyone's goodwill:

- `hooks/pre-commit`, which runs the gates locally and is bypassable with
  `git commit --no-verify`,
- `.github/workflows/gates.yml`, which re-runs them on the protected space,
- `CODEOWNERS` plus branch protection, which decide who may merge a red one.

That is the floor. The factory flow, the elicitation, the devil pass, the
gatekeeper's judgment and the "the check ran" report are conventions: they
produce better agents when followed and nothing at all when skipped, and no
exit code notices the difference. Adopt Microwave for the floor plus the
discipline, not for the discipline alone.

## 2. The gates check form, redundancy is semantic

`gate_antidup` compares words. Two agents that overlap eighty percent in what
they actually do, written with different vocabulary, pass it. `gate_slop` is a
regex bank, not a quality score. `gate_testable` checks that a criterion names a
check, not that the check exists, runs, or bites.

The structural answer to sprawl is not the gate, it is the taxonomy: one context
agent per repo is a cardinality a machine can count, and services are declared
and resolved by `gate_uses`. Inside that shape, semantic duplication is caught by
the devil pass and the gatekeeper, which are cooperative (see 1).

## 3. What "reheated at cache price" is worth

Prompt caching cuts the cost of re-reading the same prefix inside the provider's
cache window, which is measured in minutes to an hour. Two sessions a day apart
share no cache. The durable win is the other one: the context is distilled once
into atoms and reopened by id, so the next session loads a smaller, already-sorted
context instead of rediscovering it. Smaller and pre-sorted, not free. Measure
your own token spend before and after on the same task rather than trusting the
metaphor.

## 4. What is not proven

The repo has no external adopter, no fork, and a history that was squashed before
release. The private system it was extracted from is real but invisible from
here, so it is provenance, not evidence. What this repo demonstrates on its own is
narrow and checkable: it self-hosts (its own cards pass its own gates), its CI is
green on Linux, macOS and Windows across Python 3.10 to 3.13, and the gates plus
the hand-rolled YAML parser have a test suite including property tests. Everything
beyond that is a bet you are taking early.

## 5. Platform status

| Surface | Status |
|---|---|
| Gates, flows, registry, wiki | exercised on Linux, macOS and Windows in CI |
| Windows embodiment adapter | tested on a real machine, the reference adapter |
| macOS and Linux embodiment adapters | written, never run on a real machine |
| `install.sh` | run end to end in CI on the Linux and macOS runners (`test_install_sh_end_to_end`), never on a fresh personal machine |
| `bootstrap.sh` / `bootstrap.ps1` | not covered by any test: they clone, then hand off to the installers above |

Running an experimental adapter once and opening an issue with what happened is
the single most useful contribution available today (`docs/embodiment.md`).

## 6. One harness, and it is Claude Code

Not a gap, a decision (ADR-032). The repo used to advertise Codex and Cursor and
ship an `AGENTS.md` for them; nobody ran a session in either, so the claim was
dropped rather than carried. What ships is one context file (`CLAUDE.md`), one
deny-rule example (`harness/claude-settings.example.json`, and read
`docs/governance.md` for what deny-rules do and do not protect), and flows that
are exercised in Claude Code.

Nothing blocks another harness: the gates are standard-library Python you shell
out to, the flows are plain markdown, the registry and the wiki are files. You
write your own context file and point it at the same flows. That is a port you
own, unsupported and unproven here.

## 7. Scope is one repository

The problem the README opens with (everyone creates agents, nobody maps them) is
an organizational problem. Microwave governs one repo at a time. Federation
(`.microwave/federation`) extends anti-dup and service resolution across sibling
repos that are present on disk, declared on both sides, and checked out in CI.
That covers a person or a small team with a handful of repos. It does not cover
an org where nobody knows which repos exist, and the org-wide aggregation
described in the manifesto is a direction, not shipped code.

## 8. When it is not worth it

The gates, the registry and the gatekeeper have a fixed cost per creation
(minutes) and a fixed cost to keep honest (the wiki, the decay pass). That cost
is repaid by the second or third agent you would otherwise have rewritten from
memory, and by the first one you avoid duplicating.

Skip it if you run one or two agents you can hold in your head, if your agents
are throwaway per task, or if you want a runtime that intercepts what an agent
does. Microwave governs how agents get made and what they remember; it never sits
between the agent and your machine.

## 9. The install line runs unpinned code

`uvx microwave-method` resolves a published version and can be pinned
(`uvx microwave-method==0.1.23`). The shell bootstrap, by default, clones the
default branch at HEAD and executes it, which means whatever landed on `main` an
hour ago. Pin it with `MICROWAVE_REF`, or download it, read it, then run it. Both
forms are in `docs/install.md`.
