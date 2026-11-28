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

### Root-cause questioning: the 5 whys

The 5 whys is the habit of asking "why" of each answer. The Toyota sources below describe it for finding the cause of a failure. Asking it of a want, to reach the need and values behind it, is aidev-po's adaptation, not Toyota's, and it has a different stopping rule.

**Two stopping rules**

Ohno stops at a cause you can fix. The tree essay ([Asking why until you hit a value](research/five-whys-tree.md)) stops at a value, preference or bias you can own. These are different stopping rules, and aidev-po uses each one where it fits: the first for faults, the second for wants. The `learn-edits` skill already uses the first, running five whys to a condition at `/po-retro`. Where the second fits into the stages is not settled yet; the essay says so too. See [Philosophy](philosophy.md).

**Where it comes from**

- Toyota's own account credits Taiichi Ohno, "pioneer of the Toyota Production System in the 1950s". He told staff to "Observe the production floor without preconceptions" and "Ask 'why' five times about every matter" (Toyota Traditions, March 2006).
- In Ohno's book the method is "the basis of Toyota's scientific approach": "ask why five times whenever we find a problem … By repeating why five times, the nature of the problem as well as its solution becomes clear" (Ohno 1988, p. 123, as quoted by Card 2017). The book is lending-only at the Internet Archive and was not opened for this page; the passage is taken from Card. The book was first published in Japanese in 1978.
- Toyota's example is a welding robot that stops. The chain runs from a blown fuse, through locked bearings, a pump that is not circulating enough oil and a pump intake clogged with metal shavings, to "there is no filter on the pump". The fifth answer is the one a person can fix. The Lean Enterprise Institute cites an older version in Ohno 1988, p. 17 (a stopped machine; the last answer is that no strainer was attached) and adds: "The specific number five is not the point."
- Minoura, who worked under Ohno, recalls Ohno ordering the question because "that way you'll find the root cause, and if you get rid of that it'll never happen again" (Toyota, 2003).

**Who started it**

- Sakichi Toyoda is credited with originating the method (for example, Serrat 2009 says it "was developed by Sakichi Toyoda for the Toyota Industries Corporation", with no source). In the sources opened for this page the written record comes from Ohno and Toyota, not from Toyoda; none of them contains a text by Toyoda on the method.
- Toyota's Production System page traces its roots to Toyoda's automatic loom and says jidoka was born there. His page at Toyota Industries describes his looms and the company. Neither mentions asking why.
- The Toyoda Precepts (1935) are the closest thing to a founding text. They are not by Toyoda: five years after his death in 1930, the top management of the Toyoda companies "assembled" them "to clearly crystallize the spirit of Sakichi Toyoda" (Toyota Industries). They call for being faithful to duty, "studious and creative", practical, warm at work, and respectful of spiritual matters and grateful. They say nothing about questioning or root causes.

**Limits and criticisms**

| Limit | What the sources say |
|-------|----------------------|
| One causal chain | Card (2017): it forces one analytical pathway and one root cause (see "Chain or tree" below for how far that holds). In his wristband example another team could produce "five wholly different and equally valid" whys, and a causal tree found over 75 causes and contributing factors against the one or two a chain would find. Card's target is healthcare incident analysis, where he argues it should be dropped; he still sees value as a teaching example. |
| Stops at what the asker knows | Serrat (2009): critics cite investigators who stop at symptoms and who cannot "cast their minds beyond current information and knowledge". That is investigator bias: the chain can only hold causes the asker already thinks to look for. The name is ours; Serrat does not use it. |
| Results differ between people | Serrat: different teams have come up with different causes for the same problem. Card makes the same point. A likely ingredient is confirmation bias: an asker tends to accept the answers that fit the cause they already suspect, so two people who start from different suspicions end at different roots. That is our reading; none of the sources opened names it. |
| Deduction instead of observation | Minoura (2003) says the method works less well than it should because people answer from deduction, "reel off five causes as quick as a flash", and then so many causes come back that "you end up totally confused as to which of them is important". His remedy is on-the-spot observation and training, not dropping the method. |
| Drift into blame | Serrat notes that when a problem appears "the temptation is strong to blame others or external events". Atlassian's 5 whys play opens the session with "We're here to investigate, not to blame", and Google SRE's postmortem practice is explicitly blameless. I found no study that measures this drift for the 5 whys, so treat it as a recognised risk and a convention. |

**Chain or tree**

- The single-chain problem comes from Ohno's published examples and from common practice, not from every account of the method. The examples I could open are single chains: Toyota's welding robot, and the stopped machine the Lean Enterprise Institute cites from Ohno 1988, p. 17. Atlassian's play collects several answers at each step but has the team choose one to carry forward, so it ends as a single chain. Card says the two-pathway practice he describes "is not how use of the tool has generally been taught in the healthcare industry". I could not open Ohno's book, so I cannot say it never branches.
- Serrat (2009) already branches. His process has the team record every sensible answer to the first why ("There will probably be three or four sensible answers") and ask the next why "for every statement", posting each answer near its parent and following up "all plausible answers". Minoura describes the same at Toyota: he asks "five whys again for each of the causes they came up with", and finds that so many causes come back that it is hard to tell which matters. His worked example, the Amazon conveyor case, is still a single chain.

**Depth is not the target**

- Card (2017) says the fifth, most distal why is not automatically the best place to intervene. He says there is "no logical reason to assume that this is always the most effective or most efficient target for intervention", and that "Appropriate targets for intervention may occur anywhere along the causal continuum". His example is a proximate fix, a forcing function on the wristband check, that would make the distal causes moot. He also says distal causes can be worth acting on, for culture or as quick wins. His subject is fixing faults.
- For discovery that carries over as our inference, not Card's claim: a need halfway down the tree may be the real requirement, not only the leaf. The leaf says what the asker values or prefers; the requirement may sit higher up. Which one to build from is a decision, and the register should record it as one.

What aidev-po takes from this: five is a rule of thumb and not a rule (Serrat), so branch, and stop where the stopping rule for that kind of question says to; check each answer against the evidence and tag it (Stated, Inferred, Assumed) instead of deducing; let someone other than the asker review the chain or tree in a fresh context, which is the main guard against investigator and confirmation bias; and never end on a person, only on a condition or a value.

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

### Root-cause questioning (5 whys)

- [Toyota Production System: Beyond Large-Scale Production](https://archive.org/details/toyotaproduction0000onot), Taiichi Ohno, Productivity Press, Cambridge, MA, 1988, ISBN 0-915299-14-3 (Card's citation gives Portland, OR). Internet Archive record, which gives Cambridge, Mass. Lending-only; not opened. Cited through Card (p. 123) and the Lean Enterprise Institute (p. 17).
- [トヨタ生産方式: 脱規模の経営をめざして](https://ndlsearch.ndl.go.jp/books/R100000002-I000001376735), 大野耐一 (Taiichi Ohno), Diamond-sha, 1978. National Diet Library catalogue record for the Japanese original.
- ["Ask 'why' five times about every matter."](http://web.archive.org/web/20190326100957/https://www.toyota-global.com/company/toyota_traditions/quality/mar_apr_2006.html), Toyota Traditions, Toyota Motor Corporation, March 2006. Archived copy; the original address now redirects to Toyota's company page. The welding-robot example.
- [The Story of Sakichi Toyoda](https://www.toyota-industries.com/company/history/toyoda_sakichi/), Toyota Industries Corporation. His looms, and the 1935 Toyoda Precepts.
- [Toyota Production System](https://global.toyota/en/company/vision-and-philosophy/production-system/), Toyota Motor Corporation. Roots in Sakichi Toyoda's loom and jidoka; Ohno's role.
- [The "Thinking" Production System: TPS as a winning strategy for developing people in the global manufacturing environment (2003)](https://web.archive.org/web/20201121032113/https://media.toyota.co.uk/wp-content/files_mf/1323862732essenceTPS.pdf), Toyota Motor Corporation. Teruyuki Minoura's 2003 talk, in Toyota's write-up. Archived copy.
- [The problem with '5 whys' (2017)](https://doi.org/10.1136/bmjqs-2016-005849), Alan J. Card, BMJ Quality & Safety 26(8):671-677. Single chain, single root cause, differing results.
- [The Five Whys Technique (2009)](https://www.adb.org/publications/five-whys-technique), Olivier Serrat, Knowledge Solutions 30, Asian Development Bank. Process, and the list of criticisms.
- [5 Whys](https://www.lean.org/lexicon-terms/5-whys/), Lean Lexicon, Lean Enterprise Institute. Ohno's stopped-machine example (1988, p. 17); "The specific number five is not the point."

### Sibling project

- [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), GitHub. Coordinator, producer plus reviewer, register, Learn phase, scorecard.
- [ai-sdlc-loop coordinator](https://github.com/mitulamin/ai-sdlc-loop/blob/main/agents/coordinator.md), GitHub.
- [ai-sdlc-loop /retro command](https://github.com/mitulamin/ai-sdlc-loop/blob/main/commands/retro.md), GitHub.
- [ai-sdlc-loop learn-producer](https://github.com/mitulamin/ai-sdlc-loop/blob/main/agents/learn-producer.md), GitHub.
- [ai-sdlc-loop testing the skills (scorecard rules)](https://github.com/mitulamin/ai-sdlc-loop/blob/main/guides/developer/testing-the-skills.md), GitHub.

Links come from the research pass. The arXiv and project links were spot-checked and open; a few publisher sites (Wiley, Agile Business Consortium) refuse automated requests, so check them in a browser if one does not load. The 5 whys sources were each opened and read, except Ohno's book (lending-only). Card's BMJ page and DOI refuse automated requests, so its text was read through a page-text fetch; check the BMJ page in a browser.
