#!/usr/bin/env python3
"""Union two BibTeX files by entry key.

Every chapter fragment appends its citations to the single `references.bib`,
so any two open pull requests collide there and the resolution is always
"keep both" (Morrison-Lab/wai#236). This script performs that resolution
deterministically.

Give it the two *parent* versions of a conflicted file rather than the file
carrying conflict markers. While a path is conflicted the index holds both:

    git show :3:references.bib > theirs.bib   # the side whose formatting wins
    git show :2:references.bib > ours.bib
    python3 scripts/bibunion.py theirs.bib ours.bib references.bib

Reconstructing the file from the markers instead loses the blank lines that
separate entries, because those are context rather than conflicted content,
and pandoc then refuses the whole bibliography.

BASE_FILE's entries come first, in their own order and formatting. ADD_FILE's
entries whose keys are absent are appended, separated by one blank line. A key
present in both with differing bodies is an error, because silently picking a
side would drop a real edit.

Validate the result with the tool that consumes it before committing:

    printf 'x [@matrix]\\n' > cite.md
    pandoc --citeproc -t plain -o /dev/null --bibliography references.bib cite.md

Exit status: 0 on success, 2 on a conflicting duplicate key, 1 on bad usage.
"""

import re
import sys

ENTRY_START = re.compile(r"@\w+\{\s*([^,\s]+)\s*,")


def entries(text, source):
    """Split BibTeX source into (key, block) pairs.

    A block runs from a line beginning with '@' to just before the next such
    line, so trailing comments and whitespace stay attached to the entry they
    follow.
    """
    text = text.replace("\r\n", "\n")
    out = []
    for block in re.split(r"\n(?=@)", "\n" + text.strip("\n")):
        block = block.strip("\n")
        if not block.startswith("@"):
            continue
        match = ENTRY_START.match(block)
        if match is None:
            raise SystemExit(f"{source}: entry does not start with '@type{{key,': {block[:60]!r}")
        out.append((match.group(1), block))
    return out


def union(base, add):
    seen = {key: block for key, block in base}
    merged = [block for _, block in base]
    for key, block in add:
        if key in seen:
            if seen[key].strip() != block.strip():
                raise SystemExit(f"duplicate key with differing bodies: {key}")
            continue
        seen[key] = block
        merged.append(block)
    return merged


def main(argv):
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 1
    base_path, add_path, out_path = argv[1:]
    base = entries(open(base_path, encoding="utf-8").read(), base_path)
    add = entries(open(add_path, encoding="utf-8").read(), add_path)
    merged = union(base, add)
    with open(out_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n\n".join(merged) + "\n")
    print(f"base {len(base)} entries, add {len(add)}, merged {len(merged)} -> {out_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except SystemExit as exc:
        if isinstance(exc.code, str):
            print(exc.code, file=sys.stderr)
            sys.exit(2)
        raise
