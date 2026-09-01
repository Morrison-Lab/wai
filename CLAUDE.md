# Claude Code Instructions

Project guidance for Claude Code (CLI, IDE, and the GitHub Action). The same conventions apply to GitHub Copilot --- see [`.github/copilot-instructions.md`](.github/copilot-instructions.md), which is the source of truth for style.

## Project context

`wai` (Working with AI) is a UCD-SERG lab [Quarto](https://quarto.org/) website collecting the lab's notes on working responsibly and effectively with AI coding assistants --- policies, coding agents, and the pull-request workflow. It was migrated out of the [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/)'s "Working with AI" chapter, and is built from the [`qwt` (Quarto Website Template)](https://github.com/Morrison-Lab/qwt). Published at <https://Morrison-Lab.github.io/wai/>.

Authoritative style guide: [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/) (source: <https://github.com/UCD-SERG/lab-manual>).

## Repository layout

- `index.qmd`, `chapters/`, `appendix-*.qmd` --- Quarto source pages
- `references.qmd` --- standalone reference page; excluded from the default website
  render (`!references.qmd` in `_quarto-website.yml`), so it isn't part of the
  normal site build
- `_quarto.yml`, `_quarto-website.yml` --- Quarto project + website config
- `_extensions/` --- vendored Quarto extensions
- `macros/` --- git submodule for shortcode/macro definitions (see `.gitmodules`)
- `shared/` --- vendored prose fragments included by chapters; `shared/workflow/`
  holds copies of `Morrison-Lab/ai-config` workflow fragments, refreshed by
  `scripts/vendor-ai-config-fragments.py` (do not edit those copies by hand)
- `scripts/` --- maintainer scripts run by hand (not by CI)
- `R/`, `man/`, `DESCRIPTION`, `NAMESPACE` --- the project is also a small R package
- `references.bib` --- BibTeX bibliography
- `styles.css` --- website styling; `styles-reveal.scss`, `qwt-reveal-toggle.html`, and the `revealjs-*.lua` filters drive the reveal.js slide output
- `assets/`, `images/` --- static image and asset files (site pages, docs, CI/PR screenshots)
- `.github/workflows/` --- CI workflow definitions
- `.github/scripts/` --- helper scripts used by workflows
- `.github/instructions/` --- path-scoped Copilot rules that attach by file glob (see `.github/copilot-instructions.md`)
- `CONTRIBUTING.md` --- contributor guide
- `_site/`, `_freeze/`, `.quarto/` --- build artifacts (do not edit by hand)

## Style conventions

Mirrors [`.github/copilot-instructions.md`](.github/copilot-instructions.md). Key points:

- **Lists of 3+ items**: use bullet lists rather than comma-separated prose. Always leave a blank line before a markdown bullet list (especially in `.qmd` files).
- **Code chunks**: use `#| code-fold: true` when the *output* (plot, table) is the point and the code is incidental. Don't fold tutorial code, short examples, or chunks where the console output is the main content.
- **R style**: respect `.lintr.R`. Run `lintr::lint_dir()` before declaring R changes done.
- **Quarto chunks**: prefer chunk options as YAML-style `#|` directives, not as inline `r, opt = val` arguments.

## Working in this repo

- **Don't edit generated files**: `README.md` is built from `README.Rmd`; `_site/` and `_freeze/` are build outputs.
- **Local preview**: `quarto preview` (live reload). Full build: `quarto render`. When verifying a single edited page, render just that page (`quarto render <file>.qmd --to html`) rather than the whole site --- the `/render` command is for the full build.
- **Submodules**: see `.gitmodules` for the current set (`macros/`).
  Run `git submodule update --init --recursive` after cloning.
- **Vendored ai-config fragments**: `chapters/pr-workflow-with-agents.qmd` includes
  the `shared/workflow/*.md` copies of `Morrison-Lab/ai-config` fragments.
  To pick up upstream changes, run `python3 scripts/vendor-ai-config-fragments.py`
  and commit the result rather than editing the copies.
- **Spell check**: words go in `inst/WORDLIST` (see `.github/workflows/check-spelling.yaml`). Update the wordlist instead of disabling the check.
- **Link check**: tuned in `lychee.toml`; prefer fixing broken links over adding exceptions.
- **Other CI checks**: workflows also verify bibliography DOIs (`check-bibliography-dois.yml`) and flag non-standard characters (`check-non-standard-chars.yaml`). Fix the flagged source rather than relaxing the check.
- **Dependencies**: Dependabot auto-updates the git submodules listed in `.gitmodules` and GitHub Actions (see `.github/dependabot.yml`); don't bump those by hand unless a PR needs it.

## Pull request expectations

- Keep PRs scoped --- bug fixes shouldn't smuggle in refactors.
- Write commit messages and PR descriptions explaining the *why*, not just the *what*.
- Don't bypass CI failures (spell check, link check, lint, bibliography DOIs, non-standard chars) --- fix the underlying issue.
- Don't commit `_site/` or `_freeze/` changes unless that is genuinely the intent of the PR.

## Things to avoid

- Adding new top-level dependencies (R packages, Quarto extensions) without a clear reason; keep the build lean.
- Reformatting unrelated files.
- Inventing URLs or citations --- only use sources actually present in `references.bib` or explicitly provided.
