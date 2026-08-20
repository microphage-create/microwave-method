# /re — resume where you left off

```
  re  v1
  resume: jump to the most recent active save of this scope
```

Run `flows/resume.md`. `re` is the short verb for the rare resume gesture, so it
defaults to the obvious thing instead of asking for an argument (LRN-005). Three
forms, cheapest first:

- **`/re`** (bare, the common case): from `wiki/sessions/REGISTER.md`, jump to the
  most recent `active` save whose scope matches the current context, read that
  `wiki/sessions/<id>.md`, follow its wikilinks, continue from "Next steps". No
  id, no menu.
- **`/re <id>`**: jump to that exact save (`/re S-20260819-02-example`), from any
  context or machine that has the repo.
- **`/re --list`**: browse the active saves (id, date, scope, subject, next step)
  and pick.

Resuming never edits the save (saves are append-only history); the resumed
session writes its own with `/save` at its end. A save whose next steps no longer
make sense is flipped to `done` with a one-line note, not silently ignored.
