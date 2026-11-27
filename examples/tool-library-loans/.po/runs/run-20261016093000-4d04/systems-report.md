# Systems Report — Lantern Lane Tool Library

> Fictional demo for the aidev-po worked example. This is the report as written in this run (rev 1). Rerun RR-001 later rewrote `SYS-012` and `SYS-018`; see `.po/runs/run-20261112093000-9c09/`.

- **Run ID**: `run-20261016093000-4d04`
- **Output**: `04-systems.md` (`SYS-001` to `SYS-018`)

## What I produced

- C4 Level 1 context: the loans app (`SYS-001`), the spreadsheet it replaces (`SYS-002`) and the library mailbox (`SYS-003`), with members, volunteers, the coordinator and the treasurer.
- Integration Register: the one-off import (`SYS-004`) and outbound email (`SYS-005`); retry rule is an assumption.
- EventStorming in six steps (`SYS-007` to `SYS-012`): reserve, release after 48 hours, check out, remind, check in, and the house-rule policy.
- Hotspots `SYS-013` (duplicates) and `SYS-014` (bouncing email), both in the register.
- Glossary `SYS-015` to `SYS-018`.

## Skill self-check

- c4-context-eventstorming: every arrow has an Integration Register row; events are past tense; each hotspot is a register request. Policy `SYS-012` follows the house rule in `IDEA-005` (three late returns in a year, a month without borrowing), written as an automatic policy.
- evidence-tags: Stated items cite an answer or `inputs/house-rules.md`; untagged items are Inferred.
- trace-records: one write line per item, run ID above.

## Assumptions and open questions

=== REGISTER REQUESTS ===
[QUESTION: How long should a reservation be held? Recommend: 48 hours, then release it automatically.]
[ASSUMPTION: If an email fails to send, retrying three times and then showing it to the coordinator is enough.]
[QUESTION: Who merges duplicate members before the import? Recommend: the coordinator, before import.]
[ASSUMPTION: Some members' email addresses are out of date and will bounce.]
[QUESTION: Should tools get barcode labels in Release 1? Recommend: no; park.]
=== END REGISTER REQUESTS ===
