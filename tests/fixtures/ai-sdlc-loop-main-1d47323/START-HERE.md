# Start here

This project was set up for you in one step. This note is for the agent (and for you, if you are curious). You do not need to read it to get going: say what you want to build.

The goal is to hand you over to a Cursor agent that understands what's going on and can handhold you from here into the decisions you need to make. You should never feel unassisted. Bootstrap only gave Cursor a leg up: the full SDLC is here so you are not dependent on the AI model to do all the thinking.

## What was set up

- The project files from the solo template: `AGENTS.md` (the short rules file), `PROCESS.md`, `README.md` and `CHANGELOG.md`.
- In `.cursor/`: a coordinator, the producer and reviewer agents, the skills, and the `/sdlc-*` commands.
- An always-on rule, `.cursor/rules/ai-sdlc-bootstrap.mdc`, that sends every session back to this file.
- A local git repository on the `main` branch with nothing committed yet. There is no GitHub repository, no remote and no account.

## For the agent

You may be talking to someone who has never written code. Use plain language, one idea at a time, and no jargon unless they use it first.

Work as the project's coordinator, as `.cursor/agents/coordinator.md` describes. Every step of the SDLC goes through it, and through the producers and reviewers it starts. The `/sdlc-*` commands are the same steps, for when the person wants to run one by hand.

1. **Make the initial commit.** The repository has no commits yet, and you make the first one. Run `git status` and tell the person, in plain words, what is about to be committed. When they agree, commit everything with a short message such as "Start the project". Do this as your first step, or right after the first step they approve if you would rather not interrupt the interview. Do not leave it undone.
2. **Interview, unless `AGENTS.md` is already filled in.** If `AGENTS.md` still has `TODO` in it, ask the person what they want to build, one question at a time. Give your recommended answer with each question, so they can just say yes. Stop when you can describe the project, who it is for, and what done looks like. Then fill in `AGENTS.md` (stack, commands, conventions, boundaries) and keep it short. Once `AGENTS.md` has no `TODO` left, skip the interview and start from what the person asks for now.
3. **Show the plan before any code.** Write the plan in plain language, with numbered goals the person can check, and wait for them to approve it. Change it if they ask. Write no code until they say go.
4. **Build in small steps.** Run each step through the coordinator. When the person approves a step, make one git commit for it with a short plain-language message (the initial commit, if you have not made it yet, comes first).
5. **Keep it local.** Do not create a GitHub repository, add a remote, push, or sign up for any service. If the person wants to share the project later, explain the options and help only when they ask.
6. **If a commit fails because git does not know who they are (this can happen at the initial commit),** ask for their name and email, and set them for this project only with `git config user.name` and `git config user.email` (no `--global`). Do not invent an identity.

When the work is done, say what was built, how to run it, and what you would suggest next.
