# Trace of <FB-ID>: <one-line summary of what is wrong>

Attribution: <AT-ID>. Feedback: <severity> <category>, on <item IDs and revs>.

## What is wrong

<One sentence.>

## The chain

| Step | Item, rev | Agent, step, run | Evidence | Verdict |
|------|-----------|------------------|----------|---------|
| 1 | <REQ-001 r1> | <fsd-producer, 4-write-requirements, run-...> | <Inferred> | carrier: input already wrong |
| 2 | <US-001 r1> | <scope-producer, 3-slice-stories, run-...> | <Inferred> | carrier |
| 3 | <ACT-003 r1> | <actors-producer, 2-actor-sweep, run-...> | <Inferred; relied on r-...: "..."> | **origin**: input right, output wrong |
| 4 | <ACT-001 r1> | <...> | <Stated> | clean |

## Where it began

<Origin step.> Cause: `<cause>`. <Explanation as conditions, not blame.>

Should have caught it: <reviewer, and which check applied, or none>.

Confidence: <0.0 to 1.0>, <high / medium / low>, because <basis>.

Replay to confirm: <which step, with which corrected input, and what output would confirm it>.

## Alternatives

1. <Origin, cause, confidence: why it fits.>

## Question for the user

<Only at low confidence or not-sure: the one question.>

## Suggested surface

<skill / reviewer-check / lint / template / question-bank / agent-brief / client-preference / product-decision / none>: <a phrase>. A hint for /po-retro, not a decision.

## Assumptions and open questions

=== REGISTER REQUESTS ===
None.
=== END REGISTER REQUESTS ===
