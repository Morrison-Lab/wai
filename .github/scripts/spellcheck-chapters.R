#!/usr/bin/env Rscript
# Spell-check the site's prose pages against inst/WORDLIST.
#
# The Spellcheck workflow's r-spellcheck-action runs
# spelling::spell_check_package(), which reads the package files
# (README, DESCRIPTION, man/, vignettes/) and never reaches chapters/
# (Morrison-Lab/wai#177). This script covers the pages the package
# check cannot see: index.qmd, appendix-*.qmd, and chapters/**/*.qmd.
#
# `{{< include ... >}}` lines are dropped before checking: hunspell splits
# the include path on hyphens, so every kebab-case filename segment would
# otherwise be reported as a misspelling of the prose.
#
# Exit status is the number of misspelled words, matching the action.

files <- c(
  "index.qmd",
  list.files(".", pattern = "^appendix.*[.]qmd$"),
  list.files(
    "chapters", pattern = "[.]qmd$", recursive = TRUE, full.names = TRUE
  )
)

staging <- file.path(tempdir(), "spellcheck-chapters")
shortcode <- "^[[:space:]]*\\{\\{<.*>\\}\\}[[:space:]]*$"
staged <- vapply(files, function(f) {
  out <- file.path(staging, f)
  dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
  lines <- readLines(f, warn = FALSE)
  writeLines(lines[!grepl(shortcode, lines)], out)
  out
}, character(1))

wordlist <- readLines("inst/WORDLIST", warn = FALSE)
result <- spelling::spell_check_files(staged, ignore = wordlist)
result$found <- lapply(
  result$found, sub, pattern = paste0("^", staging, "/"), replacement = ""
)
print(result)

n <- nrow(result)
if (n > 0) {
  cat("\nNumber of misspelled words:", n, "\n")
  cat(
    "Fix the spelling, backtick code identifiers,",
    "or add real terms to inst/WORDLIST.\n"
  )
}
quit(save = "no", status = n)
