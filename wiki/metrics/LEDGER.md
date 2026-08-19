# Governance ledger (append-only)

One line per governance event, logged at the moment it happens (ADR-014).
Format: `DATE | event | subject | detail | author` (author = agent+human).

Events: created (agent activated, detail = minutes) - intercepted (defect
caught before activation, detail = source:severity) - deduped (creation
blocked as duplicate) - purged (agent/atom retired, detail = why).

`gates/metrics.py` aggregates this into the ROI report; `--digest` breaks it
down per author. Never edit past lines: the ledger is history.
