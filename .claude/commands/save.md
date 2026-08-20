# /save — session checkpoint

```
  save  v1
  session checkpoint: write one atomic, gated resume point
```

Run `flows/save.md`. Bare `/save` scans the whole session and writes ONE
coherent, gated batch:

- the session save under `wiki/sessions/<id>.md` (id `S-YYYYMMDD-NN-slug`), from
  `templates/session-save.md`: task in progress, done, decisions, files, next
  steps;
- the untraced atoms the session produced (ADR / learning / bug into the project
  wiki, plus their `wiki/INDEX.md` lines);
- the register line in `wiki/sessions/REGISTER.md` and the governance events in
  `wiki/metrics/LEDGER.md`.

A save that does not pass the gates does not enter the register: atomicity is
enforced by validation, versioning is git's job. The discipline lives in the
flow; this command is the door to it. Resume a save with `/re`.
