#!/usr/bin/env python3
"""PreToolUse hook (Bash): block git invocations that abuse long-option
abbreviation or short-option bundling to smuggle an exec vector into
--upload-pack (git fetch / git ls-remote) or --open-files-in-pager
(git grep).

This complements, rather than replaces, the Bash permission deny
patterns in .claude/settings.json. Those patterns match literal
substrings and cover the common spellings, but cannot express git's
short-option bundling (e.g. `git grep -lO/tmp/evil.sh`, where the
literal substring "-O" never appears) without also blocking most
legitimate `git grep` usage. Proper tokenization also closes shell
quote-splicing bypasses of the same substring rules (e.g.
`--up''load-pack`), which resolve to the dangerous flag but don't
contain it as an unbroken substring.
"""
import json
import shlex
import sys

SHELL_OPERATORS = {";", "&&", "||", "|", "&", "(", ")"}


def _long_option_name(token):
    """Strip -- and any =value / no- prefix, or None if not a long option."""
    if not token.startswith("--"):
        return None
    name = token[2:]
    if "=" in name:
        name = name.split("=", 1)[0]
    if name.startswith("no-"):
        name = name[3:]
    return name


def is_upload_pack_abbrev(token, min_len):
    name = _long_option_name(token)
    if name is None:
        return False
    return len(name) >= min_len and "upload-pack".startswith(name)


def is_pager_long_abbrev(token):
    name = _long_option_name(token)
    if name is None:
        return False
    return len(name) >= 2 and "open-files-in-pager".startswith(name)


def is_pager_short_bundle(token):
    """Matches -O and any short-option bundle containing -O (e.g. -lO<pager>).

    Walks the bundle left to right and stops at the first value-taking
    short flag (-e, -f, -m, -A, -B, -C), since the remainder of the token
    is that flag's attached argument, not additional flags. This avoids
    misclassifying e.g. ``-eOK`` (pattern "OK") as containing -O.
    """
    if token.startswith("--") or not token.startswith("-"):
        return False
    if token == "-":
        return False
    value_flags = {"e", "f", "m", "A", "B", "C"}
    for ch in token[1:]:
        if ch == "O":
            return True
        if ch in value_flags:
            # Remaining characters are the value for this flag, not flags.
            return False
    return False


def tokenize(command):
    """shlex.split() only splits on whitespace, so an operator glued
    directly to the next command (e.g. `true;git fetch ...`, no space
    after `;`) merges into one token and `git` is never recognized.
    Using punctuation_chars gives control operators (; & | ( )) their
    own tokens even without surrounding whitespace, while still
    resolving quote-splicing within a word the same way shlex.split
    does."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    return list(lexer)


def _filter_heredoc_bodies(tokens):
    """Return tokens with heredoc bodies removed.

    A heredoc ``<<[ -]WORD`` body fed to a non-executing consumer like
    ``cat`` is prose, not a command, so a line like
    ``git grep -O runs a pager`` inside it should not be flagged. The body
    runs from the ``<<`` operator through the matching terminator line.
    Heredocs whose target *does* execute the body (``bash``, ``sh``,
    ``ssh``, ``python3``, etc.) are not stripped, since the body there
    genuinely runs.

    With ``punctuation_chars``, ``<<-EOF`` (no space) tokenizes as
    ``<<`` + ``-EOF``, and ``<<- EOF`` (with space) as ``<<`` + ``-`` +
    ``EOF``, so both forms are handled. Only a plausible delimiter
    (word-like, not numeric) is treated as a heredoc; this avoids
    misclassifying arithmetic ``1<<2`` as a heredoc start.
    """
    import re

    # Heredocs fed to these consumers are prose, not execution.
    SAFE_HEREDOC_CONSUMERS = {"cat", "tee"}

    filtered = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "<<" and i + 1 < len(tokens):
            # Only strip when the heredoc target is a known non-executing
            # consumer. ``bash <<EOF ...`` genuinely executes its body.
            prev = tokens[i - 1] if i > 0 else ""
            if prev not in SAFE_HEREDOC_CONSUMERS:
                filtered.append(tokens[i])
                i += 1
                continue
            # Determine delimiter token, handling ``<<-`` split forms.
            nxt = tokens[i + 1]
            if nxt == "-" and i + 2 < len(tokens):
                delim_token = tokens[i + 2]
                delim_start = i + 1
            elif nxt.startswith("-") and len(nxt) > 1:
                delim_token = nxt[1:]
                delim_start = i + 1
            else:
                delim_token = nxt
                delim_start = i + 1

            # Heredoc delimiters are typically word-like (EOF, END, etc.),
            # not numeric. This distinguishes ``cat <<EOF`` from ``1<<2``.
            plausible = bool(re.match(r"^[A-Za-z_][A-Za-z0-9_-]*$", delim_token))
            if plausible:
                # Find the terminator line (next occurrence of delimiter).
                term_idx = None
                for k in range(delim_start + 1, len(tokens)):
                    if tokens[k] == delim_token:
                        term_idx = k
                        break
                if term_idx is not None:
                    # Skip the entire heredoc: <<, delimiter, body, terminator.
                    i = term_idx + 1
                    continue
        filtered.append(tokens[i])
        i += 1
    return filtered


def find_violations(command):
    try:
        tokens = tokenize(command)
    except ValueError:
        # Unbalanced quotes etc. -- don't try to out-clever a command we
        # can't safely parse; fall back on the existing deny patterns.
        return []

    # Strip heredoc bodies so prose inside them is not scanned as commands,
    # but resume scanning after the terminator so a real command following
    # the heredoc is still checked (avoids a full bypass).
    tokens = _filter_heredoc_bodies(tokens)

    violations = []
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == "git" and tokens[i + 1] in ("fetch", "ls-remote", "grep"):
            subcmd = tokens[i + 1]
            j = i + 2
            while j < len(tokens):
                tok = tokens[j]
                if tok == "git" or tok in SHELL_OPERATORS:
                    break
                if subcmd == "fetch" and is_upload_pack_abbrev(tok, min_len=3):
                    violations.append((subcmd, tok))
                elif subcmd == "ls-remote" and is_upload_pack_abbrev(tok, min_len=1):
                    violations.append((subcmd, tok))
                elif subcmd == "grep" and (
                    is_pager_long_abbrev(tok) or is_pager_short_bundle(tok)
                ):
                    violations.append((subcmd, tok))
                j += 1
        i += 1
    return violations


def main():
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        return
    command = (data.get("tool_input") or {}).get("command", "")
    if not command:
        return

    violations = find_violations(command)
    if violations:
        reasons = "; ".join(f"git {sub}: {tok!r}" for sub, tok in violations)
        print(
            json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            "Blocked: resolves to a git exec-vector flag "
                            "(--upload-pack / --open-files-in-pager) via "
                            "option abbreviation or short-option bundling: "
                            f"{reasons}. See .claude/settings.json and PR #61."
                        ),
                    }
                }
            )
        )


if __name__ == "__main__":
    main()
