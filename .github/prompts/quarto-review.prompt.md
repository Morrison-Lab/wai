---
mode: agent
description: Quarto-first PR review for this repository --- content, rendering correctness, links, and validation gaps. Use when preparing or checking a PR that touches pages, rendering logic, or workflow files.
---

Review the requested changes as a Quarto-first code review for this repository.

Scope:

- Prioritize changed `.qmd`, `.R`, `.Rmd`, `.yml`, and `.yaml` files.
- Treat files under `_extensions/` as vendored third-party code. Read them for
  context if needed, but do not flag or request changes there.
- Focus on behavior, rendering correctness, broken links or references, and
  validation gaps.

Review checklist:

1. Links point to source `.qmd` targets, not rendered `.html` files; cross-refs
   (`@fig-`, `@tbl-`, `@sec-`) resolve to defined labels.
2. Lists of three or more items use bullets with a blank line above them.
3. `code-fold: true` is used where the *output* is the point and avoided on
   tutorial code; chunk options use `#|` directives, not inline `r, opt = val`.
4. Narrative text does not hard-code computed values --- they are computed in a
   chunk and referenced with inline R.
5. Citations and attribution are present where adapted content or factual
   claims appear, and only sources in `references.bib` are used.
6. No new R package or Quarto extension is added without a clear reason (this is
   a template --- every dependency lands in every downstream book).
7. No generated files are edited (`README.md` from `README.Rmd`; `_site/`,
   `_freeze/`, `.quarto/`), and spell/link-check failures are fixed at the
   source (wordlist or content), not suppressed.
8. The author ran the required local validation:
   - render of the touched page
   - `lintr`
   - `spelling::spell_check_package()`

Output format:

- Findings first, ordered by severity, with file references.
- Then open questions or assumptions.
- Then a short change summary only if useful.
- If there are no findings, say so explicitly and note any residual testing gaps.

Base the review on [copilot-instructions.md](../copilot-instructions.md) and
[CLAUDE.md](../../CLAUDE.md), plus any path-scoped rules under
`.github/instructions/` (if present) that apply to the changed files.
