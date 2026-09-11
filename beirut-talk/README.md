# Beirut talk

Slides for a guest talk on the Zcash security formalization, for Nadim Kobeissi's
Applied Cryptography course at the American University of Beirut.

The deck is [Marp](https://marp.app/) Markdown in `talk.md`: slides are separated
by `---`, maths is KaTeX (`$...$` / `$$...$$`), speaker notes are HTML comments,
and per-slide directives are comments like `<!-- _class: lead -->`. Styling lives
in the front-matter `style:` block.

## Building

- `make html` / `make pdf` — one-shot exports (PDF drives an installed
  Chrome/Chromium via puppeteer).
- `make watch` — rebuild `talk.html` on save; `make serve` — live-reload preview
  server.
- Or use the "Marp for VS Code" extension for an in-editor live preview.

`marp-cli` is fetched on first use via `npx`; nothing needs a global install.

## Mermaid diagrams

A ```` ```mermaid ```` fence is rendered to SVG at build time and inlined into the
slide, by the engine in `marp-engine.mjs` (selected in `.marprc.yml`). The
rendering is done by mermaid-cli, fetched via `npx` on first use together with a
headless Chrome for its own use; renders are cached in `diagrams/` by the hash of
the diagram's source, so an unchanged diagram costs nothing on rebuild. Inline SVG
means the diagram is vector in both the HTML and the PDF, uses the deck's fonts,
and keeps its links. The `figure.mermaid` rules in the `style:` block size it to
the slide width. The VS Code extension does not load custom engines, so its
preview shows the fence as code; use `make watch` or `make serve` instead.

## Notes

- Marp's highlighter has no Lean grammar; use ```` ```haskell ```` as an
  approximation for Lean snippets, or plain fences.
- Local images need `--allow-local-files` (already in the Makefile targets).
- Both browsers' PDF export emits the deck's fonts as Type 3 glyph procedures,
  because Raleway is loaded as a variable font and the body text falls back to
  the (variable) system font. Most viewers render those like any other text, but
  some readers may do a poor job on them (e.g. mupdf).