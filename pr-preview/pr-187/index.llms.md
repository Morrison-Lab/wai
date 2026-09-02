# Working with AI

Code

Published

Last modified: 2026-09-01 18:13:05 (PDT)

This site collects the UCD-SERG lab’s notes on working responsibly and effectively with AI coding assistants: what they are, how to use them, and the policies lab members follow when using them. It was migrated out of the [UCD-SERG Lab Manual](https://ucd-serg.github.io/lab-manual/)’s “Working with AI” chapter, which had grown large enough to deserve a dedicated site. For the lab’s broader coding, reproducibility, and collaboration conventions, see the lab manual itself.

> **WARNING:**
>
> As of early 2026, AI coding assistant technology is changing extremely rapidly, and we are just beginning to figure out how to use these tools effectively ourselves. All information on this site should be taken with extra caution, as best practices and capabilities continue to evolve.

## 1 Chapters

- [**Policies for Using AI**](chapters/ai-use-policies.llms.md): responsibility for validation, disclosure, attribution, and using AI for journal articles
- [**Coding Agents**](chapters/coding-agents.llms.md): what language models, coding agents, and harnesses are; how to work with them; benefits, hazards, and best practices; and configuring your environment
- [**Orchestrating Teams of Agents**](chapters/agent-orchestration.llms.md): when running several agents at once is worth the cost, what we already use for it, and how three outside orchestrators (Agent Teams, Inflexa, TORQCLAW) compare
- [**Grok Bot and Alternatives**](chapters/grok-bot-and-alternatives.llms.md): persistent teammates with their own computer (Grok Bot, Rakazo, OpenClaw, Claude Cowork, ChatGPT Work) and how they differ from our coding-agent stack
- [**Data Dictionaries for Humans and Agents**](chapters/data-dict.llms.md): `data-dict.yaml` for making dataset context accessible to both humans and AI agents (see [data-dict.tidyverse.org](https://data-dict.tidyverse.org/))
- [**Benchbook: A Personal Wiki Under Contract**](chapters/benchbook.llms.md): a plain-markdown, git-versioned wiki that an AI agent maintains under a written contract (see [benchbook](https://github.com/Ulef1005/benchbook))
- [**Make: Visual Automation and AI Agents**](chapters/make.llms.md): visual, no-code canvas for 3,000+ apps, scenarios, and AI agents with Make Grid and MCP (see [make.com](https://www.make.com/en))
- [**Pull-Request Workflow with Agents**](chapters/pr-workflow-with-agents.llms.md): filing issues, claiming work, and driving a pull request to a clean, mergeable state

The notes are available in multiple formats:

- **HTML Website**: Navigate using the navbar for easy access to all pages
- **RevealJS Slides**: Each chapter can generate a presentation format with `-slides.html` suffix
- **PDF Handouts**: Each chapter can generate a PDF handout with `-handout.pdf` suffix
- **DOCX Documents**: Each chapter can generate a Microsoft Word document with `.docx` extension

## 2 About this website

This website is built with [Quarto](https://quarto.org/), an open-source scientific and technical publishing system, from the [UCD-SERG `qwt` (Quarto Website Template)](https://github.com/Morrison-Lab/qwt).

## 3 Building the website

To render the website locally:

``` bash
quarto render
```

To preview the website with live reload:

``` bash
quarto preview
```

The rendered output will be in the `_site/` directory, which is published to GitHub Pages.

## 4 License

See [`LICENSE`](https://github.com/Morrison-Lab/wai/blob/main/LICENSE).

## References

Back to top
