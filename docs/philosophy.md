---
title: Philosophy
---

# Philosophy

aidev-po is one part of a wider way of thinking at Shravi about building with AI. These are the beliefs it is built on, and what it is trying to achieve.

## Five beliefs

### 1. AI-first

Start from what an AI team can do well and design the process around that, instead of bolting a chatbot onto the old process. Agents do the drafting, sweeping, cross-checking and write-up. People do the deciding, the talking to other people, and the judging of what matters. The coordinator pattern (one agent you talk to, many fresh-context agents doing the work) comes from [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop) and is reused here.

### 2. Evidence over invention

Language models are fluent, which makes invented requirements look like real ones. So every item aidev-po writes is tagged with where it came from (Stated, Inferred, Assumed, Simulated or Validated), and an item with no evidence is a question, not a fact. A 2026 literature review of generative AI in requirements engineering found hallucination reported in 63.4% of 238 studies (see [Research](research.md)). The answer is not to trust the model less in general; it is to make every claim checkable.

### 3. Challenge assumptions

A product owner who agrees with everything is a typist. Assistants tend to agree with the person in front of them, and to drop a correct challenge when pushed (Sharma et al. on sycophancy). aidev-po has a separate `challenger` that works in a fresh context: it asks for the last real instance, what happens if we do nothing, offers a cheaper alternative, and runs a pre-mortem. If you overrule it, that becomes a recorded decision with your reason. It never quietly changes its mind.

A stated want is rarely the need. "I want a dashboard" usually sits on top of a job someone is trying to get done, and under that, something they value. aidev-po uses root-cause questioning here, in two forms with different stopping rules. For faults, Ohno stops at a cause you can fix. For wants, the [tree essay](research/five-whys-tree.md) asks why of every answer, not only one, and stops at a value, preference or bias you can own. aidev-po uses each where it fits: the first for faults, the second for wants. Depth is not the target either way: in discovery, a need halfway down the tree may be the real requirement, not only the leaf. The limits in [Research](research.md#root-cause-questioning-the-5-whys) apply to both: a single chain misses other causes, it stops at what the asker knows, different people get different answers, and it can end on a person instead of a condition. So five is a rule of thumb, answers are checked against what people actually did, and a fresh-context reviewer reads the chain.

### 4. The human decides at the gates

ai-sdlc-loop runs on its own and comes back at the end of a cycle. Product definition is different: the answers only the user has are needed throughout. So `po` stops at every stage gate. It shows what the stage produced, what the reviewer found, and the open questions, each with a recommended answer. You approve, answer, send it back, or park. `po` never advances a stage on its own and commits to your products repo only with your OK.

### 5. Learn from every run

Feedback on any output (a requirement, an actor row, a slide) is walked back to the step where it first went wrong, not just patched. Findings become small, tested edits to skills, reviewers and templates, which a person approves. The measure is whether the same kind of feedback stops coming back. See [Learning loop](learning-loop.md).

## What we are trying to achieve

1. **A usable FSD from a rough idea.** A specification an engineering team can plan from: problem, outcome, audience, actors, systems, scope and non-goals, testable requirements, quality requirements, decisions and open questions, all traceable.
2. **Fewer wrong requirements, caught early.** Cheaper to fix in a gate review than in a build.
3. **Questions that are easy to answer.** At most five at a time, each with a recommended answer and a way to park it. The agent does the homework; you make the call.
4. **Honest uncertainty.** What we know, what we guessed and what we have not asked yet are visibly different.
5. **A process that improves.** Each run leaves the skills, reviewers and templates a little better, with a human approving every change.
6. **Private by default.** Product work lives in a separate git repo you own, never in this public repo.

## Principles for the design

- Problem before solution: no feature is recorded until the problem and outcome are agreed.
- Ask about the past, not opinions about the idea (the Mom Test).
- One producer, one adversarial reviewer per stage, each in a fresh context.
- One register for open questions, assumptions and decisions.
- Size the process to the product: a small internal tool gets a one-page PRD, a client platform gets the full FSD.
- Simulated users are hypotheses for finding gaps, never evidence.
- Keep files plain and readable.
