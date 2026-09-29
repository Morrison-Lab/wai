---
description: Scaffold a new chapter in the Quarto website
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(quarto render:*)
---

Create a new chapter from `$ARGUMENTS` (e.g. `/new-chapter intro Introduction`).

First, parse `$ARGUMENTS`: the first whitespace-delimited token is the **slug**
(used for the filename, no `.qmd`); everything after the first space is the
**title** (default the title to the slug if none is given).

Steps:

1. Create `chapters/<slug>.qmd` with YAML frontmatter holding just `title:` (set
   to the title). Do NOT set `date:` — `_quarto-website.yml` sets
   `date: last-modified` globally, and a per-page `date:` would override it and
   freeze the date. Do NOT add a top-level `#` heading in the body — Quarto
   renders the frontmatter `title:` as the page heading, so a `#` heading would
   duplicate it.
2. Add an entry for the new chapter to the `website.navbar.left` "Chapters" menu
   in `_quarto-website.yml` (read the file first to find the menu; there is no
   `chapters:` key in `_quarto.yml`). Use `text:` for the menu label and
   `href: chapters/<slug>.qmd`.
3. Confirm it renders: `quarto render chapters/<slug>.qmd`.

Style rules (from CLAUDE.md):

- Blank line before every bullet list
- Chunk options via `#|` directives, not inline `r, opt = val`
- Code folds by default: keep the default when the output is the point; set `#| code-fold: false` on tutorial code, short examples, code that is the main focus, or chunks where the console output is the main content
