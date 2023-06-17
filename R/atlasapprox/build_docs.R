library("stringr")

# Find R package path
write('-- Find package location ---------------------------------------------------', stderr())
path <- str_split(commandArgs(trailingOnly = FALSE)[4], "=")[[1]][2]
if (!startsWith(path, "/")) {
    cwd = getwd()
    path <- paste(cwd, path, sep="/")
}
pkg <- dirname(path)

# Delete placeholder index.html file required by Sphinx
fake_idx_path <- paste(dirname(dirname(pkg)), "docs", "build", "html", "R", "index.html", sep = "/")
if (file.exists(fake_idx_path)) {
    write('-- Deleting placeholder index.html file ------------------------------------', stderr())
    tmp <- file.remove(fake_idx_path)
}

write('-- Build API .R -> .rd -----------------------------------------------------', stderr())
devtools::document(pkg = pkg)

write('-- Build site using pkgdown ------------------------------------------------', stderr())
pkgdown::build_site(pkg = pkg)
