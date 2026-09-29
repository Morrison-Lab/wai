---
applyTo: "**/*.{qmd,Rmd}"
description: "Use when editing Quarto pages, chapters, slides, handouts, or narrative content in this repository."
---

# Quarto Content

- Link to source `.qmd` files, not rendered `.html` files.
- Always leave a blank line before a markdown bullet list, and use a bullet
  list (not comma-separated prose) for three or more items.
- Prefer Quarto div wrappers for new figures and tables.
- HTML output folds code by default (the site config sets `code-fold: true`
  with `code-tools: true`, as rme does). Keep the default when the *output*
  (plot, table) is the point and the code is incidental; set
  `#| code-fold: false` on tutorial code, short examples, code that is the
  main focus, or chunks where the console output is the main content.
- Prefer chunk options as YAML-style `#|` directives, not inline
  `r, opt = val` arguments.
- For a changed `.qmd` with R code, run
  `Rscript -e 'lintr::lint("path/to/file.qmd")'` before finishing.
- Do not hard-code computed values in narrative text. Compute them in a chunk
  and reference them with inline R.
- Treat files under `_extensions/` as vendored third-party code: read them for
  context if needed, but do not reformat or edit them as part of a content
  change.

See also:

- [CLAUDE.md](../../CLAUDE.md)
- [copilot-instructions.md](../copilot-instructions.md)
- [r-and-config.instructions.md](r-and-config.instructions.md)
