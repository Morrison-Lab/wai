#!/usr/bin/env python3
"""Vendor the ai-config fragments that chapters/pr-workflow-with-agents.qmd includes.

The lab's machine-facing workflow rules live in Morrison-Lab/ai-config. This
site includes several of that repo's ``shared/workflow`` fragments as chapter
sections. They used to arrive through a git submodule; they are now vendored
copies under ``shared/workflow/`` so the site builds from a plain checkout
(see issue #81).

Run this script from the repository root to refresh the copies from ai-config's
``main`` branch::

    python3 scripts/vendor-ai-config-fragments.py

The set of fragments is read from the chapter's own ``{{< include >}}`` lines,
so adding or dropping an include is the only edit needed. Each copy gets a
provenance header naming the upstream path and commit, and three rewrites are
applied to its prose (never to code spans or fenced blocks):

- relative Markdown links become absolute GitHub URLs, because a link such as
  ``[ardi](ardi.md)`` or ``[CLAUDE.md](../../CLAUDE.md)`` only resolves inside
  the ai-config checkout;
- bare ``@mentions`` are backslash-escaped, because Pandoc would otherwise read
  ``@claude`` as a citation key and render it as ``claude?``;
- typographic punctuation is normalized to ASCII, because this repository's
  non-standard-character check scans ``.md`` files.
"""

from __future__ import annotations

import json
import posixpath
import re
import sys
import urllib.request
from collections.abc import Callable
from pathlib import Path

REPO = "Morrison-Lab/ai-config"
BRANCH = "main"
CHAPTER = Path("chapters/pr-workflow-with-agents.qmd")
DEST = Path("shared/workflow")

# `{{< include ../shared/workflow/<name>.md >}}` in the chapter.
INCLUDE = re.compile(r"\{\{<\s*include\s+\.\./shared/workflow/([\w.-]+\.md)\s*>\}\}")
# A Markdown link target that is neither absolute, an anchor, nor a mailto,
# with an optional "title" after it.
RELATIVE_LINK = re.compile(r'\]\((?!https?://|#|mailto:)([^)\s]+)((?:\s+"[^"]*")?)\)')
# An inline code span (any backtick run, possibly wrapping across lines).
CODE_SPAN = re.compile(r"`+[^`]*`+")
# A bare @mention such as "@claude" in prose, which Pandoc reads as a citation.
MENTION = re.compile(r"(?<![\w`\\])@(?=[A-Za-z])")
# A fenced-block delimiter; four or more leading spaces make an indented block.
FENCE = re.compile(r"^ {0,3}(```|~~~)")
ASCII_PUNCTUATION = {
    "—": "---",
    "–": "--",
    "‘": "'",
    "’": "'",
    "“": '"',
    "”": '"',
    "…": "...",
}


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def head_commit() -> str:
    api = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"
    return json.loads(fetch(api))["sha"]


def fragments() -> list[str]:
    names = INCLUDE.findall(CHAPTER.read_text(encoding="utf-8"))
    if not names:
        sys.exit(f"no shared/workflow includes found in {CHAPTER}")
    return [f"shared/workflow/{name}" for name in names]


def map_prose(text: str, transform: Callable[[str], str]) -> str:
    """Apply ``transform`` to prose only, leaving fenced blocks and code spans intact."""
    out: list[str] = []
    chunk: list[str] = []
    in_fence = False

    def flush() -> None:
        joined = "\n".join(chunk)
        pieces: list[str] = []
        last = 0
        for span in CODE_SPAN.finditer(joined):
            pieces.append(transform(joined[last:span.start()]))
            pieces.append(span.group(0))
            last = span.end()
        pieces.append(transform(joined[last:]))
        out.append("".join(pieces))
        chunk.clear()

    for line in text.split("\n"):
        if FENCE.match(line):
            if in_fence:
                out.append(line)
            else:
                flush()
                out.append(line)
            in_fence = not in_fence
        elif in_fence:
            out.append(line)
        else:
            chunk.append(line)
    flush()
    return "\n".join(out)


def absolutize(text: str, source_path: str, commit: str) -> str:
    """Rewrite relative links so they point at the upstream file on GitHub."""
    source_dir = posixpath.dirname(source_path)

    def replace(match: re.Match[str]) -> str:
        target, _, anchor = match.group(1).partition("#")
        if target.startswith("/"):
            resolved = posixpath.normpath(target.lstrip("/"))
        else:
            resolved = posixpath.normpath(posixpath.join(source_dir, target))
        url = f"https://github.com/{REPO}/blob/{commit}/{resolved}"
        if anchor:
            url += f"#{anchor}"
        return f"]({url}{match.group(2)})"

    return RELATIVE_LINK.sub(replace, text)


def escape_mentions(text: str) -> str:
    return MENTION.sub(r"\\@", text)


def asciify(text: str) -> str:
    for char, replacement in ASCII_PUNCTUATION.items():
        text = text.replace(char, replacement)
    return text


def header(source_path: str, commit: str) -> str:
    return (
        "<!--\n"
        f"Vendored from https://github.com/{REPO}/blob/{commit}/{source_path}\n"
        "Do not edit by hand; refresh with scripts/vendor-ai-config-fragments.py\n"
        "-->\n\n"
    )


def main() -> int:
    commit = head_commit()
    DEST.mkdir(parents=True, exist_ok=True)
    for source_path in fragments():
        raw = f"https://raw.githubusercontent.com/{REPO}/{commit}/{source_path}"
        text = fetch(raw).decode("utf-8")
        text = map_prose(text, lambda prose: absolutize(prose, source_path, commit))
        text = map_prose(text, escape_mentions)
        text = map_prose(text, asciify)
        out = DEST / posixpath.basename(source_path)
        out.write_text(header(source_path, commit) + text, encoding="utf-8")
        print(f"wrote {out} from {source_path}@{commit[:7]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
