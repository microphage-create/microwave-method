# Session save register

Append-only lookup table for `flows/save.md` / `flows/resume.md`. One line
per save, most recent last:

`- S-YYYYMMDD-NN-slug | YYYY-MM-DD | agent | scope | one-line summary`

An id is all a human needs to resume from any machine that has this repo.
Saves live beside this file; this register is their local index (ADR-012).
