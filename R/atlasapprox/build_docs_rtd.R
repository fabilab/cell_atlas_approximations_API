library("stringr")

# Install pkgdown
install.packages("pkgdown", lib = ".", repos = "https://cloud.r-project.org")
library("pkgdown", lib.loc = ".")

# Find R package path
path <- str_split(commandArgs(trailingOnly = FALSE)[4], "=")[[1]][2]
if (!startsWith(path, "/")) {
    cwd = getwd()
    path <- paste(cwd, path, sep="/")
}
pkg <- dirname(path)

# Delete placeholder index.html file required by Sphinx
fake_idx_path <- paste(Sys.getenv("READTHEDOCS_OUTPUT"), "html", "R", "index.html", sep = "/")
if (file.exists(fake_idx_path)) {
    write('-- Deleting placeholder index.html file ------------------------------------', stderr())
    tmp <- file.remove(fake_idx_path)
}

# override the destination in _pkgdown
pkgdown_cfg_fn <- paste(pkg, "_pkgdown.yml", sep = "/")
configlines <- readLines(pkgdown_cfg_fn)
configlines[1] = paste("destination: ", Sys.getenv("READTHEDOCS_OUTPUT"), "/html/R/", sep = "")
writeLines(configlines, pkgdown_cfg_fn)


# Build API docs .R -> .rd
devtools::document(pkg = pkg)

# Build R docs
pkgdown::build_site(pkg = pkg)
