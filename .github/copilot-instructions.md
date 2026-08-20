# GitHub Copilot Instructions

This file provides custom instructions for GitHub Copilot when working in this repository.

## General Guidelines

Follow the guidance in the [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/).

The source files for the lab manual are available at <https://github.com/UCD-SERG/lab-manual> if easier to read.

For workflow fixes, do not restrict the publish workflow render target to HTML only.
Keep publish rendering all configured formats and fix underlying failures instead.

## Path-Scoped Rules

Path-scoped rules live in [`.github/instructions/`](instructions/) and attach
automatically (via each file's `applyTo:` glob) when you edit matching files:

- [`quarto-content.instructions.md`](instructions/quarto-content.instructions.md) -- `.qmd` / `.Rmd` content
- [`r-and-config.instructions.md`](instructions/r-and-config.instructions.md) -- `.R`, `.yml`, `.yaml`

## Style Guidelines

### Lists

When describing lists of three or more items, use a bullet list instead of a comma-separated list. Use your stylistic judgment to determine when this rule applies.

**Examples:**

❌ **Don't** use comma-separated lists for three or more items:
```
The template includes GitHub Actions workflows for publishing, link checking, and spell checking.
```

✅ **Do** use bullet lists instead:
```
The template includes GitHub Actions workflows for:

- Publishing
- Link checking
- Spell checking
```

Always put a blank line before the start of a bullet-point list in markdown (`.md`) files and variants (especially Quarto `.qmd` files).

**When to use your judgment:**

- Short, simple items in a sentence may remain comma-separated if it maintains readability
- Complex items or items with descriptions should always use bullet lists
- Use bullet lists when the items are important and deserve emphasis
- Technical lists (commands, file names, features) typically benefit from bullet format

## Code Chunks

### Code Folding

Use `code-fold: true` for code chunks where the output is what's important to the narrative and not the code used to produce it. This allows readers to focus on the results while still having the option to view the code if they want to.

**When to use `code-fold: true`:**

- Visualization code where the plot/figure is the main point
- Data preparation or cleaning code that produces a summary table
- Long or complex code that would distract from the narrative
- Code that generates output (plots, tables, results) that readers need to see

**When NOT to use `code-fold: true`:**

- Tutorial code where readers need to learn the syntax
- Short, simple examples that are part of the explanation
- Code that is the main focus of the section
- When the console output is part of the main content (unformatted tables, model summaries, etc.)

**Example:**

````markdown
```{{r}}
#| code-fold: true
#| fig-cap: "Relationship between weight and miles per gallon"

library(ggplot2)
ggplot(mtcars, aes(x = wt, y = mpg)) +
  geom_point() +
  geom_smooth(method = "lm") +
  theme_minimal() +
  labs(x = "Weight (1000 lbs)", y = "Miles per Gallon")
```
````

## Quality Assurance

### Testing Renders

Before requesting review or marking work as complete:

- **Test your changes locally** by running `quarto render` (or rendering only the touched page with `quarto render <file>.qmd --to html` while iterating).
- **Check the rendered output** in `_site/` to verify:
  - All content displays correctly
  - No broken links or missing images
  - Formatting is as expected
- **Review the PR preview** at the preview URL to confirm everything works in the deployed version.
- **Fix any rendering issues** before requesting review.

This ensures reviewers see working, polished output rather than discovering basic rendering problems.

### Check for Late-Arriving Comments

Before declaring an agent session complete, re-read the issue/PR thread for
comments that were posted *after* the request you started on. A follow-up or
correction can land while you're working, and ending the session without it
means the next reviewer has to re-ask.

- Re-check the timeline (and, on a PR, the inline review-thread comments) for
  newer messages directed at you.
- Address any in chronological order, then look again, until none remain.
- If comments keep arriving, stop after roughly five passes (mirroring the
  cap in `claude.yml`), say so in your closing reply, and don't loop
  indefinitely.
