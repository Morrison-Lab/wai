#!/usr/bin/env python3
"""Tests for scripts/bibunion.py.

Run directly (`python3 scripts/test_bibunion.py`) or via
`python3 -m unittest discover -s scripts`, which is what CI does.
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "bibunion.py"

BASE = """@misc{alpha,
  title = {Alpha},
  year = {2026}
}

@misc{beta,
  title = {Beta},
  year = {2026}
}
"""

ADD = """@misc{beta,
  title = {Beta},
  year = {2026}
}

@misc{gamma,
  title = {Gamma},
  year = {2026}
}
"""

ADD_CONFLICTING = """@misc{beta,
  title = {Beta but different},
  year = {2026}
}
"""


def run(base, add):
    """Union `base` and `add`, returning (exit code, output text, stderr)."""
    tmp = Path(tempfile.mkdtemp())
    (tmp / "base.bib").write_text(base, encoding="utf-8")
    (tmp / "add.bib").write_text(add, encoding="utf-8")
    out = tmp / "out.bib"
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(tmp / "base.bib"), str(tmp / "add.bib"), str(out)],
        capture_output=True,
        text=True,
    )
    text = out.read_text(encoding="utf-8") if out.exists() else ""
    return proc.returncode, text, proc.stderr


class TestBibUnion(unittest.TestCase):
    def test_keeps_every_distinct_key_once(self):
        code, text, _ = run(BASE, ADD)
        self.assertEqual(code, 0)
        for key in ("alpha", "beta", "gamma"):
            self.assertIn(key, text)
        self.assertEqual(text.count("@misc{beta,"), 1)

    def test_preserves_base_order(self):
        _, text, _ = run(BASE, ADD)
        self.assertLess(text.index("alpha"), text.index("beta"))
        self.assertLess(text.index("beta"), text.index("gamma"))

    def test_separates_entries_with_a_blank_line(self):
        """The defect this script exists to avoid: a resolver that joins
        entries with a single newline, which pandoc then refuses."""
        _, text, _ = run(BASE, ADD)
        self.assertIn("\n}\n\n@misc{", text)

    def test_re_separates_adjacent_base_entries(self):
        adjacent = BASE.replace("}\n\n@misc", "}\n@misc")
        code, text, _ = run(adjacent, ADD)
        self.assertEqual(code, 0)
        self.assertIn("\n}\n\n@misc{", text)

    def test_ends_with_exactly_one_newline(self):
        _, text, _ = run(BASE, ADD)
        self.assertTrue(text.endswith("}\n"))
        self.assertFalse(text.endswith("\n\n"))

    def test_refuses_a_conflicting_duplicate_key(self):
        code, _, err = run(BASE, ADD_CONFLICTING)
        self.assertEqual(code, 2)
        self.assertIn("beta", err)

    def test_empty_base_yields_the_added_entries(self):
        code, text, _ = run("", ADD)
        self.assertEqual(code, 0)
        self.assertIn("gamma", text)

    def test_bad_usage_exits_nonzero(self):
        proc = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
