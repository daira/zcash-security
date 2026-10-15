# Cambridge FV workshop lightning talk

Slides for a lightning talk on deriving the cost of security reductions in Lean (the
`efficient` keyword prototype in the Ironwood formalization), on the last day of the
Cambridge formal verification workshop, October 2026.

The deck is [Marp](https://marp.app/) Markdown in `talk.md`, in the same format as the
Beirut talk: slides are separated by `---`, maths is KaTeX, speaker notes are HTML
comments, per-slide directives are comments like `<!-- _class: lead -->`, and the styling
lives in the front-matter `style:` block. `.marprc.yml`, `marp-engine.mjs` (Mermaid
diagrams rendered to inline SVG at build time), the fonts, and the Makefile are copied
from `../beirut-talk`; see its README for the details.

## Building

- `make html` / `make pdf` for one-shot exports (PDF drives an installed Chrome via
  puppeteer).
- `make watch` to rebuild `talk.html` on save; `make serve` for a live-reload preview.

Lean snippets use ```` ```haskell ```` fences, since Marp's highlighter has no Lean grammar.

Bullets use `-`, not `*`: in Marp's HTML template a `*` list is "fragmented", revealed one item
at a time, while a `-` list appears with the rest of the slide.
