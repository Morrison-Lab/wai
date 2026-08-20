# Images Directory

Figures and screenshots used by the site pages live here.

## Naming conventions

Use descriptive, lowercase, hyphenated names that say what the image shows,
for example:

- `claude-code-cli.png`
- `pr-preview-banner.png`
- `agent-harness-diagram.svg`

## Supported formats

Quarto supports various image formats:

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- SVG (`.svg`)
- GIF (`.gif`)
- PDF (`.pdf`) -- for LaTeX/PDF output

## Referencing images

In a `.qmd` file, reference an image like this:

```markdown
![Caption describing the image](images/your-image.png){#fig-label}
```

Then cross-reference it in the text:

```markdown
As shown in @fig-label, ...
```
