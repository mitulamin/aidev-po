# docs

The documentation site for aidev-po. These are plain Markdown pages that read fine on GitHub and are also published with GitHub Pages.

The schemas those pages describe are drafts: the shared register, plus trace, feedback, attribution, rerun, ledger and scorecard. The learning loop adds the commands `/po-feedback`, `/po-rerun-from` and `/po-retro`, and the agents `tracer`, `learn-producer` and `learn-reviewer`. See [learning-loop.md](learning-loop.md).

## Publishing

Settings, Pages, Source "Deploy from a branch", Branch `main`, folder `/docs`. There is no Actions workflow; GitHub builds the Markdown with Jekyll.

## Styling

The look is copied from the [ai-sdlc-loop site](https://github.com/mitulamin/ai-sdlc-loop) so the two read as one family: the same `assets/style.css` (system fonts, light and dark, the orange-to-cyan header rule, the Alpha ribbon), the same header, nav, page and footer markup, no trackers and no external scripts. ai-sdlc-loop generates static HTML; here the pages are Markdown, so the markup lives once in `_layouts/default.html` and the nav in `_data/nav.yml`. Differences, on purpose: Jekyll instead of a generator script, the aidev-po name and logo (the Lens mark: `assets/aidev-po.svg`, with `aidev-po-512.png`, `aidev-po-128.png` and `favicon.ico` made from it), and a short block at the end of `style.css` for Markdown output (tables, blockquotes). No theme is set in `_config.yml`.

`_config.yml` sets the base URL `/aidev-po` and the `jekyll-relative-links` plugin, so links between pages are ordinary `page.md` links that work on GitHub and on the site. To add a page, create it here and add it to `_data/nav.yml`. To preview locally, run `bundle exec jekyll serve` in this folder with the `github-pages` gem (optional).

## Pages

| Page | What |
|------|------|
| [index.md](index.md) | Home: what aidev-po is and where to start |
| [philosophy.md](philosophy.md) | The thinking behind it, and what we are trying to achieve |
| [how-it-fits.md](how-it-fits.md) | How it fits with aidev, ai-sdlc-loop, aidev-platform and the governance platform, and what it does and does not do |
| [method.md](method.md) | The coordinator pattern, evidence tags, challenger, outliner questions, stage gates |
| [stages.md](stages.md) | Stage by stage: Idea to FSD, with techniques and artefacts |
| [learning-loop.md](learning-loop.md) | Stable IDs, traces, feedback, `/po-feedback`, `/po-rerun-from`, `/po-retro`, `tracer`, `learn-producer`, `learn-reviewer`, scorecard |
| [quick-start.md](quick-start.md) | Get going in a few minutes |
| [products-repo.md](products-repo.md) | Where your product work lives |
| [research.md](research.md) | What the design is based on, with sources |

Writing here is CC BY-SA 4.0. See [NOTICE.md](https://github.com/mitulamin/aidev-po/blob/main/NOTICE.md).
