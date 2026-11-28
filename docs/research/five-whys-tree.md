---
title: "Asking why until you hit a value: my take on the 5 whys"
---

# Asking why until you hit a value: my take on the 5 whys

*By Mitul Amin. Part of [Research and references](../research.md).*

Most of us can say what we want. Fewer of us can say why, and fewer still can say why *that* is the reason. The 5 whys is the oldest trick I know for closing that gap, and I have come to use it in a slightly different shape from the one it is usually taught in. This is that shape, and why I think it matters for how aidev-po approaches discovery.

## Where the 5 whys comes from

The technique is credited to Sakichi Toyoda, and Taiichi Ohno developed it within the Toyota Production System. The classic use is on a fault: a machine stopped, so ask why it stopped, then why that happened, and keep going until you reach a cause you can fix rather than a symptom you can only patch. I have no quarrel with that. It is a good habit, and it is the form most people have in mind when they say "5 whys".

## One chain, or a tree

In its classic form the 5 whys is a single chain. One problem, one answer, one next question, and so on down. That works when the problem really does have a single line of cause.

Wants are rarely like that. When I say I want something, there is usually more than one reason behind it, and the reasons do not all agree with each other. So here is how I do it:

> When you state you want something, you need to ask why. The answers to that each need their whys. Do this for five levels if possible and it will reveal not just the core problem you are trying to address but also your values, aims and objectives at the lowest levels.

The important words are "the answers to that each need their whys". If I give two answers to the first question, both get questioned. The chain becomes a tree. Each branch might bottom out somewhere different, and the places where they bottom out are the interesting part. A single chain tells you one cause. A tree shows you everything that is holding the want up.

## Five is a guide, not a rule

I say five levels "if possible", and I mean it. Five is a useful target because it is further than most of us go on instinct. The first answer is usually the one we would give without thinking. The further down we go, the more likely we are to say something we had not said before.

But some branches run out at three, and some deserve eight. Counting levels is only there to stop me quitting early. What I am really watching for is a change in the kind of answer: from a reason about the situation to a reason about me, or about us.

## The leaf nodes

If you get good at it, keep asking why until you reach the leaf nodes. A leaf is where the answer is basic and can be attributed to a value, a preference, a bias, or something similar. You cannot usefully ask why of it. "Because I prefer it" is a legitimate end to a branch, as long as you got there honestly rather than by being tired.

This is the part I find most valuable. At the top of the tree, a want sounds like a requirement. At the leaves, it turns out to be a choice that someone made, often without noticing they were making it.

## Making a conscious decision at the leaf

Once you have a leaf, you can do something with it. You can decide.

Maybe you are glad of the value and want to keep it. Maybe you realise it is a bias that does not suit this project and set it aside. Maybe you keep it and accept what it costs. All three are fine. What is not fine is the position most of us start from, which is holding the bias without knowing it and calling the result "just the way things should be done".

Owning a bias does not mean getting rid of it. It means that when someone challenges the decision, I can say what it rests on, and they can disagree with that, rather than with a stack of reasons I made up afterwards.

## A small worked tree

Here is one from my own preferences, as an illustration. The starting want: *I prefer verbose code when it makes the code easier to understand.*

- **Want:** I prefer verbose code if it makes understanding easier.
  - **Why?** Because I want the next reader to follow it without needing me.
    - **Why does that matter?** Because people move on, and I do not want the system to depend on one person's memory.
      - **Why does that matter?** Because I would rather ownership of the code was shared. *Leaf: a value, shared ownership.*
  - **Why?** Because when I read compact, clever code I slow down and trust it less.
    - **Why does that matter?** Because I make fewer mistakes changing code I understood in one pass.
      - **Why does that matter?** Because I weigh being clear above being short. *Leaf: a bias, towards readability over complexity.*

Two branches, two different leaves. One is a value about how a team should work. The other is a bias about my own reading. Neither is wrong, but they are different kinds of thing, and I would handle them differently.

The decision: yes, I am biased towards readability over complexity, and therefore I prefer verbose code if it makes understanding easier. The cost is more lines to read through, and I accept that. Having said it plainly, I can also revisit it later if the cost ever outweighs the benefit.

## Two pitfalls

**Stopping at a comfortable answer.** This is the common one. Somewhere in the tree there is an answer that sounds sensible, feels complete and is safe to say in a meeting. It is also where people stop. The test I use is whether the answer would surprise me, or whether I could have given it before I started. If I could have, I have probably not gone deep enough yet.

**Whys that blame a person rather than the system or the value.** "Why did it break?" "Because Sam did not check." That is a dead end, and an unkind one. It ends the tree on a person, and a person is not a leaf in the sense I mean: you cannot make a conscious decision about them. If a why lands on someone's name, I ask it again of the process: what made that mistake easy to make, and what would have caught it? Keep the question aimed at the system, or at the value that the system was serving.

## How this could shape product discovery in aidev

aidev-po is built to take a basic idea through to a full specification, and a lot of that is asking people what they want. The risk is that a stated want is taken as settled and written down as a requirement. If the discovery work asked why of each stated want, and then why of each answer, it would find the real problem sooner. It would also record the values and preferences underneath, so that later decisions can be checked against them.

I have not worked out how this would fit into the stages, and I would rather say so than pretend otherwise. One idea worth trying is to record the leaf nodes in the register alongside assumptions and decisions, tagged for what they are. The rest of the research behind aidev-po is on the [Research and references](../research.md) page.

If you try it, start small. Pick one thing you want this week, ask why, and then ask why of each answer. See where the branches end.
