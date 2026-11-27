---
title: Research and references
---

# Research and references

aidev-po's design comes from a research pass over product discovery and requirements techniques, what current AI-for-requirements work shows (and where it fails), and how to trace feedback back to the step that caused it. This page summarises it and lists the sources.

Two caveats. The research was a desk study; it has not been tested against real engagements yet. And the "outliner" question pattern (at most five questions, a recommended answer and Park) is taken from a description of Shravi's existing practice, not from the private aidev-platform repo, which was not read.

## What the research says

### Techniques that fit each stage

This is what the research recommends. The stage templates use a subset of it; the [Stages](stages.md) page says exactly what each stage file contains.

| Stage | Techniques chosen | Why |
|-------|-------------------|-----|
| Idea | Double Diamond, Lean Canvas, Opportunity Solution Tree, assumption mapping | Forces the problem to be stated before any solution, and shows gaps on one page |
| Audience | Jobs to be Done, the Mom Test, Value Proposition Canvas | Jobs are more stable and testable than demographics; past behaviour beats opinions |
| Actors | Actor modelling, power/interest map | A systematic sweep finds forgotten actors and says whom to involve |
| Systems | C4 context, integration register, EventStorming, bounded contexts | A shared picture plus a timeline that exposes disagreements early |
| Scope | Impact mapping, story mapping, MoSCoW, non-goals and appetite | Ties every deliverable to a goal and writes down what is out |
| Workshops | Design Sprint, EventStorming, Liberating Structures, Example Mapping, pre-mortem | Small, timed formats that hear every voice and make risks safe to raise |
| Presentations | PR/FAQ, narrative memo, decision-led decks, one-page PRD | Prose and one-decision decks expose weak reasoning |
| FSD | ISO/IEC/IEEE 29148, INVEST, Given/When/Then, EARS, ISO 25010 | Standard skeleton with testable requirement formats |

### What current AI requirements work teaches

| Work | Finding | Use in aidev-po |
|------|---------|-----------------|
| MARE (2024) | Specialised agents sharing a workspace beat baselines on model correctness | Shared artefact store; a checker role |
| iReDev (2025) | Knowledge-driven agents with a human in the loop work well | Encode product-owner know-how as skills; the register is the archive |
| Elicitron (2024) | Simulated users surfaced more latent needs than standard interviews | Optional simulated users, labelled Simulated, for finding gaps |
| LLMREI (2025) | An interview bot made about as many errors as humans and recalled up to about 74% of requirements | Never the only source; coverage checks per stage |
| Follow-up question generation (2025) | Questions guided by a taxonomy of interviewer mistakes beat human ones | Build the mistake taxonomy into interview skills |
| ClarifyGPT, Ambig-SWE | Models often miss underspecification unless prompted to look | Explicit ambiguity scan |
| GitHub Spec Kit | Clarify asks at most five questions with a recommended option | Close match to the outliner pattern |
| Kiro specs | Requirements in EARS, then design, then tasks | EARS in the FSD |

### Known pitfalls and the guard for each

| Pitfall | Guard |
|---------|-------|
| Hallucinated requirements | Evidence tag on every item; `evidence-auditor` fails untraced items |
| Sycophancy (agrees with the founder, drops a correct challenge) | `challenger` in a fresh context; overruled challenges recorded as decisions |
| Leading questions | Mom Test rules applied to every question bank |
| Premature solutioning | Problem and outcome gate before features |
| Simulated users treated as evidence | Simulated tag; Validated needs a real person |
| Question overload | Rounds of at most five, each with a recommended answer and Park |
| Spec bloat | One-pager and PR/FAQ first; FSD depth sized to the product |
| Drift between artefacts | Decision sheets, upstream IDs on every item, and the reviewer and evidence audit at each gate |

### Learning and attribution

- Attribution from raw logs is hard: on the Who&When benchmark the best method found the responsible agent about half the time and the exact step about a quarter. So aidev-po records upstream IDs as items are written and does not guess later.
- Work on failure attribution separates the **origin** of an error from where it was only **passed on** (earliest decisive error, error-propagation modelling), and some confirm a suspect by **replaying** the step with the fix. The tracer does the same and reports a confidence.
- Prompt optimisers (DSPy, GEPA, Reflexion, TextGrad) can propose wording, but in aidev-po they stay proposers inside the held-out test and human approval gate that ai-sdlc-loop already uses.
- The trace model follows W3C PROV and OpenTelemetry GenAI fields so it can be exported to Langfuse or LangSmith later.

## Sources

### Idea and Audience

- [Know your customers' jobs to be done](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done), HBR. Jobs to be Done.
- [Opportunity Solution Tree](https://www.producttalk.org/glossary-discovery-opportunity-solution-tree/), Product Talk. One outcome, opportunities, solutions.
- [Lean Canvas](https://leanstack.com/lean-canvas), LEANSTACK. One-page problem, customer, value proposition.
- [Value Proposition Canvas](https://www.strategyzer.com/library/the-value-proposition-canvas), Strategyzer. Jobs, pains, gains.
- [The Double Diamond](https://www.designcouncil.org.uk/our-resources/the-double-diamond/), Design Council. Diverge and converge on the problem first.
- [The Mom Test](https://www.momtestbook.com/), momtestbook.com. Non-leading interview rules.
- [Personas vs jobs to be done](https://www.nngroup.com/articles/personas-jobs-be-done/), NN/g. Personas and JTBD are complementary.
- [Synthetic users: if, when and how](https://www.nngroup.com/articles/synthetic-users/), NN/g. Why simulated users cannot replace real research.

### Actors, Systems and Scope

- [C4 System Context diagram](https://c4model.com/diagrams/system-context), c4model.com.
- [EventStorming](https://www.eventstorming.com/), eventstorming.com.
- [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html), Martin Fowler.
- [DDD Reference](https://www.domainlanguage.com/ddd/reference/), Domain Language. Ubiquitous language.
- [Impact Mapping](https://www.impactmapping.org/), impactmapping.org.
- [User Story Mapping](https://jpattonassociates.com/story-mapping/), Jeff Patton.
- [MoSCoW prioritisation](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html), Agile Business Consortium.
- [Shape Up: write the pitch](https://basecamp.com/shapeup/1.5-chapter-06), Basecamp. Appetite and no-gos.
- [Kano model guide](https://foldingburritos.com/blog/kano-model/), Folding Burritos.

### Workshops and Presentations

- [The Design Sprint](https://www.gv.com/sprint/), GV.
- [Liberating Structures](https://www.liberatingstructures.com/), liberatingstructures.com.
- [Example Mapping](https://cucumber.io/blog/bdd/example-mapping-introduction/), Cucumber.
- [Performing a project premortem](https://hbr.org/2007/09/performing-a-project-premortem), HBR.
- [Working Backwards PR/FAQ process](https://workingbackwards.com/concepts/the-amazon-working-backwards-pr-faq-process/), workingbackwards.com.
- [PRD and 1-pager templates](https://www.lennysnewsletter.com/p/prds-1-pagers-examples), Lenny's Newsletter.

### FSD and requirements quality

- [ISO/IEC/IEEE 29148 SRS example](https://www.reqview.com/doc/iso-iec-ieee-29148-srs-example/), ReqView. Outline for the FSD.
- [INVEST in good stories](https://xp123.com/invest-in-good-stories-and-smart-tasks/), XP123.
- [Gherkin reference](https://cucumber.io/docs/gherkin/reference/), Cucumber. Given/When/Then.
- [EARS](https://alistairmavin.com/ears/), Alistair Mavin. Easy Approach to Requirements Syntax.
- [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010), iso25000.com. Quality model.

### AI for requirements, and its pitfalls

- [MARE: multi-agent requirements engineering (2024)](https://arxiv.org/abs/2405.03256), arXiv. Shared artefact store, a checker role.
- [iReDev: multi-agent requirements development (2025)](https://arxiv.org/abs/2507.13081), arXiv. Knowledge-driven agents, human in the loop.
- [Elicitron: simulated users for elicitation (2024)](https://arxiv.org/abs/2404.16045), arXiv. Simulated users surface latent needs.
- [LLMREI: automating elicitation interviews (2025)](https://arxiv.org/abs/2507.02564), arXiv. Never the only source.
- [Elicitation follow-up question generation (2025)](https://arxiv.org/abs/2507.02858), arXiv. Taxonomy of interviewer mistakes.
- [ClarifyGPT](https://dl.acm.org/doi/10.1145/3660810), ACM. Models miss underspecification unless prompted.
- [Ambig-SWE: agents and underspecification (2026)](https://proceedings.iclr.cc/paper_files/paper/2026/hash/ed4deb2ba9d4640fb6a000c688c2972e-Abstract-Conference.html), ICLR.
- [Generative AI for requirements engineering: a systematic literature review (2026)](https://onlinelibrary.wiley.com/doi/full/10.1002/spe.70029), Wiley, Software: Practice and Experience. Hallucination reported in 63.4% of 238 studies.
- [Towards understanding sycophancy in language models](https://arxiv.org/abs/2310.13548), arXiv. Assistants drop correct answers when challenged.
- [Spec Kit: agentic spec-driven development](https://github.github.com/spec-kit/reference/agentic-sdd.html), GitHub. Clarify asks at most five questions with a recommended option.
- [Kiro specs](https://kiro.dev/docs/specs/), kiro.dev. Requirements in EARS, then design, then tasks.

### Learning loop, tracing and attribution

- [W3C PROV overview](https://www.w3.org/TR/prov-overview/), W3C. Entity, activity, agent.
- [OpenTelemetry GenAI agent spans](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md), OpenTelemetry.
- [Langfuse annotation and scores](https://langfuse.com/docs/evaluation/evaluation-methods/annotation), Langfuse.
- [Attach user feedback to traces](https://docs.langchain.com/langsmith/attach-user-feedback), LangSmith.
- [Which agent causes task failures and when? (Who&When, 2025)](https://arxiv.org/abs/2505.00212), arXiv. Earliest decisive error.
- [Why do multi-agent LLM systems fail? (MAST, 2025)](https://arxiv.org/abs/2503.13657), arXiv. Failure taxonomy.
- [GraphTracer: graph-guided failure tracing (2025)](https://arxiv.org/abs/2510.10581), arXiv. Dependency graphs.
- [AgenTracer: who is inducing failure (2025)](https://arxiv.org/abs/2509.03312), arXiv.
- [Causal Agent Replay: counterfactual attribution for LLM-agent failures (2026)](https://arxiv.org/abs/2606.08275), arXiv. Check by replay.
- [Error-propagation modeling for failure attribution in LLM-based multi-agent systems (EMFA, 2026)](https://arxiv.org/abs/2610.11600), arXiv. Origin versus propagation.
- [DSPy](https://dspy.ai/), dspy.ai. Prompt optimisers can propose edits; they stay inside the approval gate.
- [GEPA: reflective prompt evolution (2025)](https://arxiv.org/abs/2507.19457), arXiv.
- [Reflexion (2023)](https://arxiv.org/abs/2303.11366), arXiv.
- [TextGrad (2024)](https://arxiv.org/abs/2406.07496), arXiv.
- [Postmortem culture: learning from failure](https://sre.google/sre-book/postmortem-culture/), Google SRE. Blameless postmortems.
- [5 Whys analysis](https://www.atlassian.com/team-playbook/plays/5-whys), Atlassian.

### Sibling project

- [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), GitHub. Coordinator, producer plus reviewer, register, Learn phase, scorecard.
- [ai-sdlc-loop coordinator](https://github.com/mitulamin/ai-sdlc-loop/blob/main/agents/coordinator.md), GitHub.
- [ai-sdlc-loop /retro command](https://github.com/mitulamin/ai-sdlc-loop/blob/main/commands/retro.md), GitHub.
- [ai-sdlc-loop learn-producer](https://github.com/mitulamin/ai-sdlc-loop/blob/main/agents/learn-producer.md), GitHub.
- [ai-sdlc-loop testing the skills (scorecard rules)](https://github.com/mitulamin/ai-sdlc-loop/blob/main/guides/developer/testing-the-skills.md), GitHub.

Links come from the research pass. The arXiv and project links were spot-checked and open; a few publisher sites (Wiley, Agile Business Consortium) refuse automated requests, so check them in a browser if one does not load.
