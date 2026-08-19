# Project: {name}

Seed of the product-plane wiki for this domain. Created by pass 1 (the Seed guard of the full path)
when an agent opens a new domain.

## Brief

Use `templates/brief.md`: success criteria, volume cap, abort conditions.

## Structure

```
wiki/projects/{slug}/
├── brief.md
├── adr/        # decisions of this project
├── learnings/
├── bugs/
└── stories/
```

Every atom created here gets one line in `wiki/INDEX.md`. Atoms with
cross-project value are candidates for promotion to the meta plane: move them
to `wiki/_staging/` and request gatekeeper judgment. Never copy them upward
yourself.
