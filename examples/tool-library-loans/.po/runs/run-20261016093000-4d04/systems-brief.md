# Brief: Systems — Lantern Lane Tool Library

> Fictional demo for the aidev-po worked example.

- **Run ID**: `run-20261016093000-4d04`
- **Product goal**: replace paper loan cards and the shared spreadsheet with a loans app that shows availability, holds tools and reminds borrowers (`IDEA-009`, `DEC-001`).
- **Stage**: `systems`

## Acceptance criteria

- Given the actors and permissions in `03-actors.md`, When the system context is drawn, Then every arrow has an owner and a row in the Integration Register, and unknown cells are register questions, not guesses.
- Given the flows a loan goes through, When they are written as EventStorming, Then every event is past tense and linked to a command, an aggregate or invariant, and any policy.
- Given any hotspot, When it is written, Then it is also a register request.
- Given any new or rewritten item, When it is written, Then it has a trace record (skill `trace-records`) with this run ID.

## Upstream and locked decisions

- `01-idea.md`, `02-audience.md`, `03-actors.md`.
- Binding: `DEC-001` (Release 1 is loans, reservations and reminders), `DEC-002` (members primary, volunteers operate), `DEC-003` (own logins).

## Skills

- `skills/c4-context-eventstorming/SKILL.md`
- `skills/evidence-tags/SKILL.md`
- `skills/register-ops/SKILL.md`
- `skills/trace-records/SKILL.md`

## Paths

- Template: `templates/04-systems.md`
- Output: `tool-library-loans/04-systems.md`
- Report: `tool-library-loans/.po/runs/run-20261016093000-4d04/systems-report.md`
- Register: `tool-library-loans/.po/register.jsonl`
- Traces: `tool-library-loans/.po/traces.jsonl`

## Answers already given this stage

- `r-20261016090000-202b`: "We have a mailbox on our own domain; I log in to it."
- `r-20261016090100-202c`: "About 120 loans a month in summer, 70 in winter."
