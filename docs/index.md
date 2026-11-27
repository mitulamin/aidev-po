---
title: Home
layout_class: landing
---

<section class="lp-hero" aria-labelledby="lp-title">
<div class="lp-logo"><img src="assets/brand/aidev-po.svg" alt="aidev-po logo" width="96" height="96"></div>
<p class="lp-eyebrow">Product definition for AI-built software</p>
<h1 id="lp-title">From a basic product idea to a full design specification, with an AI product owner that asks, challenges and learns</h1>
<p class="lede">aidev-po is a set of agents, skills and commands. You talk to one agent, <code>po</code>. It works through eight stages, writes down where every claim came from, stops at every gate for your decision, and hands the approved FSD to ai-sdlc-loop.</p>
<p class="lp-cta">
<a class="btn btn-primary" href="quick-start.html">Quick start</a>
<a class="btn" href="stages.html">See the stages</a>
<a class="btn" href="philosophy.html">Why it works this way</a>
<a class="btn" href="https://github.com/mitulamin/aidev-po">GitHub</a>
</p>
</section>

<div class="notice" markdown="1">
**Status.** This site describes how aidev-po is designed to work. The repo is built in pull requests: the foundation (licences, scaffold, schemas, products-repo detection) first, then the stage agents and skills, then the learning loop, then these docs, then a worked example. Where a page describes behaviour that has not landed yet, treat it as the contract the build follows. The worked example will be a fictional demo under [examples/](https://github.com/mitulamin/aidev-po/tree/main/examples), not a real client product.
</div>

<section class="lp-section" aria-labelledby="why">

## What this is and why it exists {#why}

<div class="lp-cols" markdown="1">
<div markdown="1">

Most failed software starts as a vague idea nobody questioned. aidev-po does the work a good product owner does before any code: find the problem under the idea, name the audience and the job they hire the product for, list every actor and system, decide what is in and out, test the plan with real people, and write it all as a specification a team (human or AI) can build from.

</div>
<div markdown="1">

Everything it writes carries where it came from. Anything with no evidence is a question, not a fact. You decide at every gate, and every run teaches the next one. It is a sibling of [ai-sdlc-loop](https://github.com/mitulamin/ai-sdlc-loop), which takes the FSD through build, verify and ship.

</div>
</div>
</section>

<section class="lp-section" aria-labelledby="stages">

## Eight stages, one gate each {#stages}

<ol class="lp-chips">
<li><a class="chip" href="stages.html#1-idea">Idea</a></li>
<li><a class="chip" href="stages.html#2-audience">Audience</a></li>
<li><a class="chip" href="stages.html#3-actors">Actors</a></li>
<li><a class="chip" href="stages.html#4-systems">Systems</a></li>
<li><a class="chip" href="stages.html#5-scope">Scope</a></li>
<li><a class="chip" href="stages.html#6-workshops">Workshops</a></li>
<li><a class="chip" href="stages.html#7-presentations">Presentations</a></li>
<li><a class="chip" href="stages.html#8-fsd">FSD</a></li>
</ol>

Each stage has a producer and an adversarial reviewer in fresh contexts. See [Stages](stages.md) and [Method](method.md).
</section>

<section class="lp-section lp-links" aria-labelledby="next">

## Where to go next {#next}

<div class="lp-cards" markdown="1">
<div class="lp-card" markdown="1">
### [Quick start](quick-start.md)
Clone, set up your private products repo, and start with `po`.
</div>
<div class="lp-card" markdown="1">
### [Philosophy](philosophy.md)
AI-first, evidence over invention, challenge assumptions, humans decide at gates, learn from every run.
</div>
<div class="lp-card" markdown="1">
### [How it fits](how-it-fits.md)
aidev, ai-sdlc-loop, aidev-platform and the governance platform. What aidev-po does and does not do.
</div>
<div class="lp-card" markdown="1">
### [Learning loop](learning-loop.md)
IDs and traces, feedback, the tracer, `/rerun-from`, `/retro` and the scorecard.
</div>
<div class="lp-card" markdown="1">
### [Your products repo](products-repo.md)
A separate private git repo outside this checkout, one per client or team.
</div>
<div class="lp-card" markdown="1">
### [Research and references](research.md)
What the design rests on, with sources.
</div>
</div>
</section>

<section class="lp-section" aria-labelledby="licences">

## Licences {#licences}

Code (scripts, schemas, workflows) is GPL-3.0, writing (agents, skills, commands, docs, examples) is CC BY-SA 4.0, and `templates/` is MIT. Your products repo is yours and is not covered. Detail in [NOTICE.md](https://github.com/mitulamin/aidev-po/blob/main/NOTICE.md).
</section>
