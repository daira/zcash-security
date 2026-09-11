// Marp CLI engine: Marp Core plus pre-rendered Mermaid diagrams.
//
// A ```mermaid fence is rendered to SVG at build time by mermaid-cli (which draws it in a
// headless Chrome that puppeteer fetches on first use) and inlined into the slide, so the
// diagram is ordinary SVG in the HTML and in the PDF export, uses the deck's fonts, and
// keeps its links. Renders are cached in `diagrams/` by the hash of the source; a changed
// diagram renders again, an unchanged one costs nothing.
import { execFileSync } from 'node:child_process'
import { createHash } from 'node:crypto'
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const DIAGRAMS = join(dirname(fileURLToPath(import.meta.url)), 'diagrams')

function renderMermaid(source) {
  const hash = createHash('sha256').update(source).digest('hex').slice(0, 16)
  const mmd = join(DIAGRAMS, `${hash}.mmd`)
  const svg = join(DIAGRAMS, `${hash}.svg`)
  if (!existsSync(svg)) {
    mkdirSync(DIAGRAMS, { recursive: true })
    writeFileSync(mmd, source)
    execFileSync(
      'npx',
      ['-y', '@mermaid-js/mermaid-cli', '-q', '-i', mmd, '-o', svg, '-b', 'transparent',
       '-I', `mermaid-${hash}`],
      { stdio: 'inherit' },
    )
  }
  return readFileSync(svg, 'utf8')
}

export default ({ marp }) =>
  marp.use((md) => {
    const fence = md.renderer.rules.fence
    md.renderer.rules.fence = (tokens, idx, options, env, self) => {
      const token = tokens[idx]
      if (token.info.trim() === 'mermaid') {
        return `<figure class="mermaid">${renderMermaid(token.content)}</figure>\n`
      }
      return fence(tokens, idx, options, env, self)
    }
  })
