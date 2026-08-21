# <Agent name>: <one line, what it does>

A definition is the agent's operating instructions: what it actually does when
invoked. The card is the contract (metadata, blast radius, done-criteria); this
file is the behaviour. It is the file the card's `definition_path` points at.

This is a starting shape, not a cage. Definitions vary a lot (a guided flow, a
one-shot verb, a prompt); adapt or drop sections freely. For a real model, open
the `definition_path` file of an agent that already exists (e.g. a `flows/*.md`).

## When this runs

The trigger: a command the user types, a situation, a schedule. One or two lines.

## Steps

1. <what it does> -> <what it produces, or how you know the step worked>
2. <next> -> <check>

## Done when

The observable end state. Mirror the card's `success_criteria` so the same
signal that activates the agent also tells `flows/improve.md` a change improved
it (the done-criteria are the improvement oracle).

## Never

The refusals: what is out of scope, what it must not touch. Mirror the card's
scope cut so the agent does not drift into its neighbours' work.
