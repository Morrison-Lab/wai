# Policies for Using AI

Code

Published

Last modified: 2026-08-29 23:08:45 (PDT)

[AI-powered coding assistants](https://en.wikipedia.org/wiki/AI-assisted_software_development) can dramatically accelerate and improve your work, but they require careful and responsible use. Lab members who use AI tools must adhere to the following guidelines.

> **WARNING:**
>
> As of early 2026, AI coding assistant technology is changing extremely rapidly, and we are just beginning to figure out how to use these tools effectively ourselves. All information on this site should be taken with extra caution, as best practices and capabilities continue to evolve.

# 1 Responsibility for validation

**You are fully responsible for checking and validating all AI-generated code and content.** AI tools can make mistakes, generate insecure code, produce incorrect logic, or suggest approaches that are inappropriate for our specific research context. Before using any AI-generated code:

Carefully review the code to ensure you understand what it does

Test the code thoroughly to verify it works as expected

Verify that the logic is appropriate for your specific use case

Check that the code follows our lab’s coding standards and best practices

Ensure the code does not introduce security vulnerabilities or data privacy issues

> **WARNING:**
>
> Never blindly use AI-generated code without fully understanding it. If you don’t completely understand what the AI has suggested, take the time to learn or ask a colleague for help.

# 2 Disclosure of AI use

**You must clearly state whenever you have used AI tools in your work.** This is essential for transparency and reproducibility. Specifically:

- In code comments, note when AI tools were used to generate or significantly modify code
- In commit messages, mention if AI tools assisted with the changes
- In manuscripts and reports, acknowledge AI tool usage in the methods or acknowledgments section
- In presentations, disclose AI assistance when relevant

Example code comment:

    # The following function was generated with assistance from GitHub Copilot
    # and has been reviewed and tested to ensure correctness

# 3 Attribution of sources

**When using AI tools to generate content that borrows from or adapts existing sources, you must ensure proper attribution.** AI tools sometimes paraphrase or adapt content from documentation, guides, or other resources without clearly indicating the original source. It is your responsibility to:

- Ask the AI tool to identify and properly cite sources when it borrows or adapts content
- Verify that any content the AI generates includes appropriate citations
- Add citations yourself if the AI fails to do so
- Follow appropriate attribution practices for the type of content (code comments, documentation, academic writing, etc.)

When instructing AI tools to create documentation or written content, explicitly request that they provide proper attribution for any borrowed or adapted material. For example: “Please quote from and paraphrase \[source\], with proper attribution” rather than simply asking it to summarize information on a topic.

# 4 Using AI for Journal Articles

When using AI tools to help develop journal articles and other academic writing, you must take special care to ensure transparency, maintain intellectual ownership, and avoid plagiarism. The following practices help achieve these goals.

#### Establish a Clear Track Record

**Working with AI through GitHub creates valuable documentation of your contributions versus the AI’s.** This track record can be crucial if reviewers or editors question your use of AI tools.

GitHub Pull Requests and Issues provide:

- **Attribution clarity**: Each commit shows exactly who (you or `@copilot`) made which changes
- **Audit trail**: The full conversation history shows your instructions and the AI’s responses
- **Intellectual ownership**: Your prompts and guidance demonstrate that the core ideas are yours
- **Transparency**: Reviewers can see that you actively supervised and validated all AI contributions

This transparency protects you if journal reviewers are skeptical about or opposed to AI use in research. You can point to the PR history to demonstrate that you maintained control and responsibility for the work.

#### Write Out Your Core Ideas in Prompts

**Make your prompts explicit and detailed to establish that the ideas originate from you, not from the AI.**

When requesting AI assistance with academic writing:

- State your research question, hypothesis, or argument clearly
- Outline the structure and key points you want to make
- Specify the evidence or data you want to include
- Describe the logic connecting your points
- Explain the interpretation or conclusions you want to draw

**Example of a good prompt:**

> I need help writing the discussion section for a study on social determinants of health. My core argument is that \[your specific argument\]. The key findings I want to discuss are: \[list findings\]. I want to interpret these findings as suggesting \[your interpretation\]. Please help me draft this section while preserving these core ideas and citing relevant literature.

This approach creates clear evidence that the intellectual content came from you, while the AI helped with expression, organization, and literature integration.

**Avoid vague prompts** like “write a discussion section about my results” that give the AI too much creative control and make it unclear whose ideas are being presented.

#### Request Explicit Source Attribution

**Always instruct AI tools to identify and cite their sources to prevent unknowing plagiarism.**

AI language models are trained on vast amounts of text, including published research. While they don’t have direct access to their training data during generation, they may produce text that closely resembles or paraphrases existing work without providing attribution. This creates a plagiarism risk.

**Best practices:**

- Explicitly ask the AI to cite sources for any borrowed or adapted content
- Request that the AI indicate when it is drawing from specific works
- Verify that generated text includes proper citations
- Add citations yourself if the AI fails to provide them
- Cross-check AI-generated content against the cited sources to ensure accuracy

**Example request:**

> Please help me write this section, and explicitly cite any sources you draw from or adapt. If you’re paraphrasing from specific papers, identify them clearly so I can verify the citations.

Remember that even with these precautions, you must still verify the accuracy and appropriateness of any AI-generated citations, as AI tools can sometimes generate plausible-but-incorrect references (“hallucinate” citations).

#### Example Workflow

A GitHub issue-and-pull-request workflow makes this transparency practical:

1.  **Core ideas stated clearly**: An issue describing the specific concepts you want covered (for example, transparency through GitHub, writing explicit prompts, requesting source attribution)
2.  **Detailed instructions**: Guidance in the issue or your prompts specifies what content should be created and how it should be structured
3.  **Transparent record**: The commit and PR history shows what was human-directed versus AI-generated
4.  **Demonstrated accountability**: The pull request provides a full audit trail of all changes

When developing content for journal articles, a similar workflow creates documentation that demonstrates responsible AI use and intellectual ownership. You can point to your GitHub history to show reviewers that you directed the AI rather than simply accepting its output.

#### Additional Considerations

When using AI for academic writing, also remember to:

- **Disclose AI use**: Follow journal policies on acknowledging AI assistance (see [Section 2](#sec-ai-disclosure))
- **Maintain responsibility**: You are accountable for all content, including AI-generated text
- **Verify accuracy**: Always fact-check AI-generated claims and citations
- **Preserve your voice**: Ensure the writing reflects your thinking and style, not just AI’s patterns
- **Follow ethical guidelines**: Comply with your institution’s and journals’ policies on AI use

These practices help you benefit from AI assistance while maintaining the integrity, originality, and credibility of your academic work.

# References

Back to top
