#!/usr/bin/env Rscript
# Spell-check the site's prose pages against inst/WORDLIST.
#
# The Spellcheck workflow's r-spellcheck-action runs
# spelling::spell_check_package(), which reads the package files
# (README, DESCRIPTION, man/, vignettes/) and never reaches chapters/
# (Morrison-Lab/wai#177). This script covers the pages the package
# check cannot see: index.qmd, appendix-*.qmd, chapters/**/*.qmd, and the
# shared/**/*.md fragments those chapters include.
#
# `{{< include ... >}}` lines are dropped before checking: hunspell splits
# the include path on hyphens, so every kebab-case filename segment would
# otherwise be reported as a misspelling of the prose. Bold markers are
# dropped too, so an initial-letter emphasis such as **A**ddress is checked
# as the word it renders as rather than as its two halves, and so is LaTeX
# math ($...$ and $$...$$), whose commands hunspell would read as words.
#
# Exit status is 1 when any word is misspelled, else 0.

files <- c(
  "index.qmd",
  list.files(".", pattern = "^appendix.*[.]qmd$"),
  list.files(
    "chapters", pattern = "[.]qmd$", recursive = TRUE, full.names = TRUE
  ),
  list.files("shared", pattern = "[.]md$", recursive = TRUE, full.names = TRUE)
)

# spelling reports each hit as basename:line, so two files sharing a
# basename would be indistinguishable in the report.
duplicated_names <- unique(basename(files)[duplicated(basename(files))])
if (length(duplicated_names) > 0) {
  stop(
    "Duplicate file names would make the report ambiguous: ",
    paste(duplicated_names, collapse = ", ")
  )
}

staging <- file.path(tempdir(), "spellcheck-chapters")
shortcode <- "^[[:space:]]*\\{\\{<.*>\\}\\}[[:space:]]*$"
staged <- vapply(files, function(f) {
  out <- file.path(staging, f)
  dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
  lines <- readLines(f, warn = FALSE)
  lines <- gsub("**", "", lines[!grepl(shortcode, lines)], fixed = TRUE)
  text <- paste(lines, collapse = "\n")
  text <- gsub("(?s)\\$\\$.*?\\$\\$", "", text, perl = TRUE)
  text <- gsub("\\$[^$\n]+\\$", "", text, perl = TRUE)
  writeLines(text, out)
  out
}, character(1))

wordlist <- readLines("inst/WORDLIST", warn = FALSE)
result <- spelling::spell_check_files(staged, ignore = wordlist)
print(result)

n <- nrow(result)
if (n > 0) {
  cat("\nNumber of misspelled words:", n, "\n")
  cat(
    "Fix the spelling, backtick code identifiers,",
    "or add real terms to inst/WORDLIST.\n"
  )
}
quit(save = "no", status = as.integer(n > 0))
