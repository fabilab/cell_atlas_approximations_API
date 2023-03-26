# Find R package path
path <- strsplit(commandArgs(trailingOnly = FALSE)[4], "=")[[1]][2]
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

# Override destination in _pkgdown.yml to work on RTD
pkgdown_cfg_fn <- paste(pkg, "_pkgdown.yml", sep = "/")
configlines <- readLines(pkgdown_cfg_fn)
configlines[1] = paste("destination: ", Sys.getenv("READTHEDOCS_OUTPUT"), "/html/R/", sep = "")
writeLines(configlines, pkgdown_cfg_fn)


# Build API docs .R -> .rd
devtools::document(pkg = pkg)

# Install pkgdown locally and load it
install.packages("pkgdown", lib = ".", repos = "https://cloud.r-project.org")
library("pkgdown", lib.loc = ".")

# Build R docs
build_site(pkg = pkg)
