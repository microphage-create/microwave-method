# Technique bank

Six data files, adapted from BMAD-METHOD and its creative-intelligence-suite
module (MIT, see NOTICE.md), consumed by the flows. This is a bank to PICK FROM, never a checklist to run
through: a flow draws 2-3 techniques, applies them, moves on. Running more
techniques is not more rigor, it is ceremony.

## Files

- `brainstorming-methods.csv`: 108 ideation techniques, 13 categories,
  tagged by `good_for` (novel, feature, strategy, diagnosis, unstuck,
  planning, personal) and audience (solo/group).
- `elicitation-methods.csv`: 71 reasoning/elicitation methods, tagged by
  category (core, risk, competitive, framing, technical, ...) with an
  explicit `output_pattern`.
- `solving-methods.csv`: 30 problem-solving methods with facilitation
  prompts (diagnosis rows shine when migrating archive entries).
- `design-methods.csv`: 30 design-thinking methods by phase (empathize →
  test), for product-plane feature work.
- `innovation-frameworks.csv`: 30 strategy frameworks (JTBD, disruption),
  product-plane.
- `story-types.csv`: 25 narrative structures, product-plane (docs,
  launches, demos).

## How the flows pick

| Flow moment | Pick from |
|---|---|
| `create-agent` step 1 (elicit a NEW agent) | brainstorming `good_for: novel\|feature` (e.g. First Principles, How Might We, Job to Be Done) + elicitation `framing` (Reframe the Question, Abstraction Laddering) |
| `create-agent` step 1, scope cutting | brainstorming `constraint` category (One Feature Only, Kill the Crown Jewel, Ship in 60 Minutes): the fastest known cure for agent scope creep |
| `create-agent` migrating from the archive (`adopt`) | brainstorming `good_for: diagnosis` (Five Whys, Failure Analysis, Question Storming) + `solving-methods.csv` diagnosis rows on the inventory entry |
| `create-feature` (product plane) | `design-methods.csv` by phase, `innovation-frameworks.csv` (JTBD) when the feature's job is unclear, `story-types.csv` for docs/launch narratives |
| `devil-review` | elicitation `risk` + `competitive` (Pre-mortem, Assumption Audit, Red Team vs Blue Team), plus Inversion Analysis (`core`) and Boundary & Edge Case Sweep (`technical`) |
| `create-feature` when stuck | brainstorming `good_for: unstuck` (2 picks max, timebox) |
| `amend-rule` (constitution) | elicitation Second-Order Thinking + Steelmanning: an amendment must steelman the rule it attacks |

Selection rule (the consumption test applied to creativity): a technique is
picked because its output feeds the next step of the flow, not because it is
fun. If the output of a technique run feeds nothing, it was ceremony.
