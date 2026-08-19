# Flow: resume (pick up where you left off)

resume is a RARE verb, so it defaults to the obvious thing instead of
asking for an argument (LRN-005: frequent verbs stay short, rare verbs get
a smart default). Three forms, cheapest first.

## Bare `resume` (the default, zero friction)

Inside a context (a project/agent is loaded), `resume` with no argument
jumps straight to the MOST RECENT active save of THIS scope:

1. From `wiki/sessions/REGISTER.md`, take the last line whose `scope`
   matches the current context and whose save is `status: active`.
2. Read that `wiki/sessions/<id>.md`, follow its wikilinks (atoms, brief,
   agent card), load context as pass 2 prescribes, continue from "Next
   steps", top of the list.

No id typed, no menu. This is the common case.

## `resume <id>` (the rare, precise case)

`resume S-20260819-02-example`: jump to that exact save, from any context,
any machine that has the repo. The id is all a human needs to dictate.

## `resume --list` (browse)

Show the active saves (id, date, scope, subject, next step), most recent
last; the human picks. Only when the default is not what they want.

## Rules

- Resuming does not edit the save: the resumed session will write its OWN
  save at its end. Saves are append-only history.
- A save whose "Next steps" no longer make sense is a finding: flip it to
  `done` with a one-line note rather than silently ignoring it.
