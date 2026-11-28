---
title: "Asking why until you hit a value: my take on the 5 whys"
---

# Asking why until you hit a value: my take on the 5 whys

*By Mitul Amin. Part of [Research and references](../research.md#root-cause-questioning-the-5-whys), which has the sources behind this essay.*

Most of us can say what we want. Fewer of us can say why, and fewer still can say why *that* is the reason. Asking why repeatedly is an old habit for closing that gap, and I use it in a different shape from the one it is usually taught in. This is that shape, where it departs from the original, and why I think it matters for how aidev-po approaches discovery.

## Where I depart from the original

Ohno and Toyota describe the 5 whys for failures. A machine stops, you ask why, then why of that answer, and you carry on until you reach a cause you can fix. Ohno's own instruction, as quoted on the research page, was to "ask why five times whenever we find a problem". I have no quarrel with that.

My extension applies the same habit to *wants*, not faults. And it ends somewhere different: not at a cause I can fix, but at a value I can decide about.

Branching itself is not new. Serrat already asks the next why of every plausible answer, not only one. What I think is new is the last step: a conscious decision at the value leaf. Some accounts credit Sakichi Toyoda with originating the method, but the research page found the written record in Ohno and Toyota, so I do not lean on that here. The details and sources are on the [research page](../research.md#root-cause-questioning-the-5-whys).

## One chain, or a tree

The best-known examples of the 5 whys are single chains. One problem, one answer, one next question. That works when the problem has a single line of cause.

Wants are rarely like that. When I say I want something, there is usually more than one reason behind it, and the reasons do not all agree with each other. So here is how I do it:

> When you state you want something, you need to ask why. The answers to that each need their whys. Do this for 5 levels if possible and it will reveal not just the core problem you are trying to address but also your values, aims and objectives at the lowest levels.

The important words are "the answers to that each need their whys". If I give two answers to the first question, both get questioned, and the chain becomes a tree. A single chain tells you one cause. A tree shows you everything that is holding the want up.

## Five is a guide, not a rule

I say five levels "if possible", and I mean it. Five is a useful target because it is further than most of us go on instinct. The first answer is usually the one we would give without thinking, and the further down we go, the more likely we are to say something we had not said before.

But some branches run out at three, and some deserve eight. Counting levels is only there to stop me quitting early.

## The leaf nodes

If you get good at it, keep asking why until you reach the leaf nodes: the places where the answer is basic and can be attributed to a value, a preference, a bias, or something similar. At the top of the tree, a want sounds like a requirement. At the leaves, it turns out to be a choice that someone made, often without noticing.

The catch is that "because I prefer it" can be a true leaf, or it can be a comfortable halt. The words are the same either way. So I test the answer:

- Has the kind of answer changed, from the situation to me or us?
- Would another why change the decision?
- Did the answer surprise me?

If none of these is true, keep asking.

## Two kinds of node

Not every node in the tree is the same sort of claim, and I try not to treat them alike.

Nodes about how the world works need evidence: observation, not deduction (Minoura, as the research page notes, says people answer from deduction and end up confused about which cause matters). I tag them Stated, Inferred or Assumed, as in [Philosophy](../philosophy.md). That page lists five tags, so Simulated and Validated also exist; Validated means I have checked it against something observed, so I use it only when I have.

Value leaves need honesty, not proof. "I would rather protect the next person to change the code" is not something I can test in a lab. What I can do is say it truthfully and not dress it up as a fact about the world.

## Deciding at the leaf, and turning it into a rule

Once you have a leaf, you can decide. Maybe you are glad of the value and keep it. Maybe you see it is a bias that does not suit this project and set it aside. Maybe you keep it and accept what it costs. What is not fine is holding the bias without knowing it and calling the result "just the way things should be done". Owning a bias does not mean getting rid of it. It means that when someone challenges the decision, I can say what it rests on, and they can disagree with that, rather than with a stack of reasons I made up afterwards.

Leaves become informal personal decision rules. When I act against one, I ask whether it is a mood or a finer distinction. A finer distinction becomes a new, more precise rule.

## A small worked tree

Here is one from my own preferences, as an illustration. The starting want: *I prefer verbose code when it makes the code easier to understand.*

- **Want:** I prefer verbose code if it makes understanding easier.
  - **Why?** Because I want the next reader to follow it without needing me.
    - **Why does that matter?** Because people move on, and I do not want the system to depend on one person's memory.
      - **Why does that matter?** Because I would rather ownership of the code was shared. *Leaf: a value, shared ownership.*
  - **Why?** Because when I read compact, clever code I slow down and trust it less.
    - **Why does that matter?** Because I make fewer mistakes changing code I understood in one pass.
      - **Why does that matter?** Because compact, clever code hides its assumptions, and the reader fills them in without noticing. Whoever changes it later, maybe at midnight with something broken, pays for any wrong guess.
        - **Why does that matter?** Because I would rather pay for a few extra lines now than hand the next person a hidden risk. *Leaf: a value, protecting whoever changes the code next.*

Two branches, two different leaves. One is about how a team should work: shared ownership. The other is about who carries the risk: the next person to change the code. Both are values, and they usually agree, but they would not always. Shared ownership can be met with good documentation, while protecting the next person asks for clarity in the code itself.

The decision: yes, I will spend extra lines to make assumptions visible, because I would rather pay that cost now than leave the risk with whoever changes the code next. The cost is more lines to read through, and I accept that. As a rule, it is "make assumptions visible, even if it takes more lines". If I caught myself writing compact code in a throwaway script, I would ask whether that was a mood or a finer distinction. A throwaway script may have no next person, and if so the rule gets more precise: "make assumptions visible in code someone else will change".

## When two leaves conflict

Leaves can disagree. Shared ownership, from the tree above, is easy to set against another leaf I could just as easily hold: ship fastest, even if only I understand it.

When two leaves conflict, either rank them in advance or decide case by case and record the decision. This is still an open question, and I have not settled which of the two is better.

## Two pitfalls

**Stopping at a comfortable answer.** This is the common one. Somewhere in the tree there is an answer that sounds sensible, feels complete and is safe to say in a meeting. It is also where people stop. The three tests above are how I catch it: if the kind of answer has not changed, another why would change the decision, or the answer did not surprise me, I have probably not reached a leaf yet.

**Whys that blame a person rather than the system or the value.** "Why did it break?" "Because Sam did not check." That is a dead end, and an unkind one. It ends the tree on a person, and a person is not a leaf in the sense I mean: you cannot make a conscious decision about them. If a why lands on someone's name, I ask it again of the process: what made that mistake easy to make, and what would have caught it? Keep the question aimed at the system, or at the value the system was serving.

## How this could shape product discovery in aidev

aidev-po is built to take a basic idea through to a full specification, and a lot of that is asking people what they want. The risk is that a stated want is taken as settled and written down as a requirement. If the discovery work asked why of each stated want, and then why of each answer, it would find the real problem sooner. It would also record the values and preferences underneath, so that later decisions can be checked against them.

I have not worked out how this would fit into the stages, and I would rather say so than pretend otherwise. One idea worth trying is to record the leaf nodes in the register alongside assumptions and decisions, tagged for what they are.

If you try it, start small. Pick one thing you want this week, ask why, and then ask why of each answer. See where the branches end.
