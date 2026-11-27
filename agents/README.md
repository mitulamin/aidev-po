# agents

Agent sources, one markdown file per agent, with `name` and `description` front matter. `scripts/build-agents.py` copies them into `.cursor/agents/`.

## Coordinator

- [po.md](po.md): The product owner coordinator and the only agent the user talks to.

## Stage producers and adversarial reviewers

| Stage | Producer | Adversarial reviewer |
| --- | --- | --- |
| `idea` | [idea-producer.md](idea-producer.md) | [idea-reviewer.md](idea-reviewer.md) |
| `audience` | [audience-producer.md](audience-producer.md) | [audience-reviewer.md](audience-reviewer.md) |
| `actors` | [actors-producer.md](actors-producer.md) | [actors-reviewer.md](actors-reviewer.md) |
| `systems` | [systems-producer.md](systems-producer.md) | [systems-reviewer.md](systems-reviewer.md) |
| `scope` | [scope-producer.md](scope-producer.md) | [scope-reviewer.md](scope-reviewer.md) |
| `workshops` | [workshops-producer.md](workshops-producer.md) | [workshops-reviewer.md](workshops-reviewer.md) |
| `presentations` | [presentations-producer.md](presentations-producer.md) | [presentations-reviewer.md](presentations-reviewer.md) |
| `fsd` | [fsd-producer.md](fsd-producer.md) | [fsd-reviewer.md](fsd-reviewer.md) |

## Cross-cutting agents

- [evidence-auditor.md](evidence-auditor.md): Adversarial check that every item carries an evidence tag (`Stated`, `Inferred`, `Assumed`, `Simulated`, `Validated`) and verifiable provenance.
- [challenger.md](challenger.md): Fresh-context PO pushback (Mom Test last real instance, build-nothing baseline, assumption map, pre-mortem, `[Simulated]` gap check).

Learning-loop agents (`tracer`, `learn-producer`, `learn-reviewer`) arrive in PR 3.
