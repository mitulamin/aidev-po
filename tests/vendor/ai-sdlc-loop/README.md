# Vendored from ai-sdlc-loop

ai-sdlc-loop's register checker and contract data, copied unchanged, so `tests/test_shared_register.py` can show that an aidev-po register passes ai-sdlc-loop's `scripts/register.py check` and that an ai-sdlc-loop register passes aidev-po's (DEC-002 in [docs/decisions.md](../../../docs/decisions.md)). The layout matches ai-sdlc-loop's, so the script finds its data where it expects.

| File | Upstream path | Licence |
|------|---------------|---------|
| `scripts/register.py` | `scripts/register.py` | GPL-3.0, ai-sdlc-loop |
| `data/agent-contract.json` | `data/agent-contract.json` | CC BY-SA 4.0, ai-sdlc-loop (its data files) |

## Pin

- **Base:** [mitulamin/ai-sdlc-loop@9f49094](https://github.com/mitulamin/ai-sdlc-loop/commit/9f4909455e8a51c38b59b5321782acffc02aeab9) (main on 27 November 2026).
- **Plus:** the change that adds the optional aidev-po extension to the register contract (schema 1.2.0, `register.extensions`). It is proposed in an ai-sdlc-loop pull request that is **not merged yet** and waits for approval: PR link and head SHA to be added here once it is open.
- **SHA-256:** `scripts/register.py` `c9518ca44662b87a724279cbfc0def88b0daf8d1a9557a41c1d83f61baf791c6`, `data/agent-contract.json` `53735c45e71f1edd0e983c226651958b383db8df4067595dafa9b73d01138947`.

Without the extension, ai-sdlc-loop's checker still passes the baseline lines of an aidev-po register (`phase`, `blocker`, `by: human`), but not its decision, feedback and attribution lines. The test checks both.

## Refresh

When the pull request merges (or changes), copy the two files again from ai-sdlc-loop main, update the pin and hashes above, and run `python3 -m unittest discover -s tests -t tests`. Do not edit the copies here.
