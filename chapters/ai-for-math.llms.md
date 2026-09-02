# AI for Math and Statistics

Code

Published

Last modified: 2026-09-01 18:57:36 (PDT)

This chapter collects notes on language models applied to mathematical reasoning, which is the part of an AI assistant’s work a statistics lab leans on most when a derivation, a proof step, or a numerical check is at stake.

> **WARNING:**
>
> The resources reviewed here change weekly. Entry counts, model names, and benchmark results quoted below were true when the section was written (the date is stated in each section) and will drift. Re-check the source before acting on any of them.

# 1 A Reading List: Awesome-Math-LLM

[`doublelei/Awesome-Math-LLM`](https://github.com/doublelei/Awesome-Math-LLM) is an MIT-licensed, community-curated list of resources on large language models for mathematics: surveys, techniques, models, benchmarks, and tools. The notes below reflect its README as read on 2026-09-01, when it carried about 310 entries, most of them papers on arXiv with a code or model link where one exists.

## 1.1 What it covers

The list is organized into seven content sections:

- **Surveys and overviews**, led by the March 2025 survey on mathematical reasoning and optimization with LLMs ([arXiv:2503.17726](https://arxiv.org/abs/2503.17726)), which the list names as its own key source
- **Mathematical tasks**, from number representation and arithmetic through word problems, competition math, and formal theorem proving
- **Reasoning techniques**: chain-of-thought and prompting, search and planning, reinforcement learning and reward modeling, self-improvement, tool use, and integration with symbolic solvers
- **Multimodal mathematical reasoning**, for problems that include figures or diagrams
- **Models**, split into math-specialized models (for example `DeepSeekMath`, `Qwen2.5-Math`, `Llemma`, and Minerva), reasoning-focused models (`rStar-Math`, DeepSeek R1, OpenAI o1, and `QwQ-32B`), and the leading general models each vendor reports on math benchmarks
- **Datasets and benchmarks**, grouped by level: grade-school word problems (`GSM8K`, `SVAMP`), competition and university level (`MATH`, `AIME`, `MMLU-Pro`, `GPQA`), theorem proving (`miniF2F`, `ProofNet`), multimodal, and the training and synthetic sets
- **Tools and libraries**, which pairs LLM tooling (`OpenCompass` for evaluation, LoRA for fine-tuning) with the interactive theorem-proving assistants Lean, Isabelle, and `Coq`

Most entries carry a paper title, links, and a month-and-year date; the tool entries and the related-lists entries carry a name and a link only.

## 1.2 What to read with care

- The “Recent Highlights” block at the top carries the maintainer’s own note that its dates “appear to be futuristic”, so treat a date there as unreliable until checked against the paper.
- Several entries appear under more than one section (`AlphaGeometry` under both geometry and competition math, for instance), which is deliberate cross-listing rather than an error, and the entry counts above include those repeats.
- The list records what exists rather than what works: it makes no recommendations and ranks nothing, so the benchmark section is the place to start when a claim about a model’s mathematical ability needs a source.

## 1.3 Useful to us? As a map, not a recommendation

For a statistics lab the list is most useful in three ways:

- **Choosing a model for a derivation-heavy task.** The reasoning-focused and math-specialized model sections name the models whose math benchmark results are published, and the benchmark section names the tests those results come from, so a claim such as “model X is strong at math” can be tied to a number.
- **Understanding why an assistant gets a calculation wrong.** The fundamental-calculation section collects the papers on how models split and represent numbers that explain arithmetic failures, and the tool-use section collects the approaches (calling a calculator, running code, consulting a solver) that fix them, which is the pattern this lab already follows by having an agent run R rather than reason about numbers in prose.
- **Formal verification as a direction to watch.** The theorem-proving entries and the Lean, Isabelle, and `Coq` tools describe machine-checked proofs, which is the standard a statistical derivation could eventually be held to.

Its limits for us are that statistics appears only through general math benchmarks, none of the entries evaluate applied statistical reasoning specifically, and the list stops at collection: comparing the models it names is work for the reader.

Back to top
