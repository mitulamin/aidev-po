# Learning-loop templates

Formats for the files the learning loop writes. MIT, like everything in `templates/`.

| Template | Written by | Lands in |
|----------|-----------|----------|
| [feedback-comment.md](feedback-comment.md) | You, as a pull request comment | The products repo's pull request |
| [tracer-report.md](tracer-report.md) | `tracer` | `<product>/.po/tracer/<FB-ID>-<AT-ID>.md` |
| [rerun-plan.md](rerun-plan.md) | `po`, before `/po-rerun-from` rebuilds anything | Shown to you; recorded in `<product>/.po/reruns.jsonl` |
| [retro-brief.md](retro-brief.md) | `po`, at `/po-retro` | `<products repo>/.po/retro/<retro-id>/brief.md` |
| [retro-proposal.md](retro-proposal.md) | `learn-producer` | `<products repo>/.po/retro/<retro-id>/proposals.md` |
| [heldout-results.md](heldout-results.md) | `po`, after the held-out runs | `<products repo>/.po/retro/<retro-id>/heldout.md` |

The JSON formats are in `schemas/`.
