"""Unit tests for highlight-html-changes.py's element matching.

Run from the repository root:

    python3 .github/scripts/test_highlight_html_changes.py

The fixtures pin the behaviour the #180 optimization must preserve: an
unchanged element is left alone, a changed one is highlighted inline, an
unmatched one is marked as added, an element whose best match sits exactly
on the minimum similarity threshold is left alone, and a duplicated old
element serves every identical new one. A second class pins
find_changed_sections's word-level similarity: the 0.95 shortcut, the diff
lines below it, and the missing-old-page case.
"""

import importlib.util
import pathlib
import unittest

SCRIPT = pathlib.Path(__file__).with_name("highlight-html-changes.py")
spec = importlib.util.spec_from_file_location("highlight_html_changes", SCRIPT)
if spec is None or spec.loader is None:
    raise ImportError(f"cannot load the script under test from {SCRIPT}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def page(*elements):
    body = "".join(elements)
    return f"<html><body><main>{body}</main></body></html>"


def highlight(old, new):
    differ = module.HTMLDiffer(".", None)
    return differ.highlight_changed_elements(old, new)


class HighlightChangedElementsTest(unittest.TestCase):
    def test_identical_element_is_untouched(self):
        old = page("<p>The quick brown fox jumps over the lazy dog.</p>")
        html, changes = highlight(old, old)
        self.assertEqual(changes, 0)
        self.assertNotIn("<mark", html)

    def test_edited_element_is_highlighted_inline(self):
        old = page("<p>The quick brown fox jumps over the lazy dog.</p>")
        new = page("<p>The quick brown fox leaps over the lazy dog.</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 1)
        self.assertIn('<mark class="preview-text-', html)
        self.assertNotIn("preview-element-added", html)

    def test_unmatched_element_is_marked_added(self):
        old = page("<p>The quick brown fox jumps over the lazy dog.</p>")
        new = page("<p>Completely different words appear here instead.</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 1)
        self.assertIn("preview-element-added", html)

    def test_ratio_exactly_at_threshold_is_untouched(self):
        # "ab" vs "ac": 2 * 1 match / 4 characters = 0.5, the threshold.
        old = page("<p>ab</p>")
        new = page("<p>ac</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 0)
        self.assertNotIn("<mark", html)

    def test_duplicate_new_elements_match_one_old_element(self):
        old = page("<p>Repeated paragraph text.</p>")
        new = page("<p>Repeated paragraph text.</p>",
                   "<p>Repeated paragraph text.</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 0)
        self.assertNotIn("<mark", html)

    def test_edited_and_new_elements_together(self):
        old = page("<p>First paragraph about foxes and dogs.</p>",
                   "<p>Second paragraph about cats and mice.</p>")
        new = page("<p>First paragraph about foxes and hounds.</p>",
                   "<p>Second paragraph about cats and mice.</p>",
                   "<p>Zq xw kj vb.</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 2)
        self.assertEqual(html.count("preview-element-added"), 1)

    def test_identical_element_not_marked_added_after_fuzzy_match(self):
        # Even if an old element was consumed by a preceding fuzzy match,
        # an identical subsequent new element remains unchanged (#194).
        old = page("<p>The quick brown fox jumps over the lazy dog.</p>")
        new = page("<p>The quick brown fox leaps over the lazy dog.</p>",
                   "<p>The quick brown fox jumps over the lazy dog.</p>")
        html, changes = highlight(old, new)
        self.assertEqual(changes, 1)
        self.assertNotIn("preview-element-added", html)
        self.assertIn('<mark class="preview-text-', html)


class FindChangedSectionsTest(unittest.TestCase):
    def test_nearly_identical_page_takes_the_shortcut(self):
        words = " ".join(f"word{i}" for i in range(200))
        old = page(f"<p>{words}</p>")
        new = page(f"<p>{words.replace('word7 ', 'word7 extra ')}</p>")
        differ = module.HTMLDiffer(".", None)
        diff_lines, similarity = differ.find_changed_sections(old, new)
        self.assertIsNone(diff_lines)
        self.assertGreater(similarity, 0.95)

    def test_rewritten_page_reports_diff_lines(self):
        old = page("<p>" + " ".join(f"alpha{i}" for i in range(50)) + "</p>")
        new = page("<p>" + " ".join(f"beta{i}" for i in range(50)) + "</p>")
        differ = module.HTMLDiffer(".", None)
        diff_lines, similarity = differ.find_changed_sections(old, new)
        self.assertIsNotNone(diff_lines)
        self.assertLess(similarity, 0.95)

    def test_missing_old_page_reports_nothing(self):
        differ = module.HTMLDiffer(".", None)
        self.assertEqual(differ.find_changed_sections("", page("<p>x</p>")), (None, 0))


if __name__ == "__main__":
    unittest.main()
