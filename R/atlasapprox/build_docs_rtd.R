# Find R package path
write('-- Find package location ---------------------------------------------------', stderr())
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

write('-- Override destination in _pkgdown.yml ------------------------------------', stderr())
pkgdown_cfg_fn <- paste(pkg, "_pkgdown.yml", sep = "/")
configlines <- readLines(pkgdown_cfg_fn)
configlines[1] = paste("destination: ", Sys.getenv("READTHEDOCS_OUTPUT"), "/html/R/", sep = "")
writeLines(configlines, pkgdown_cfg_fn)

write('-- Install packages in current folder and adapt libPaths --------------------', stderr())
.libPaths(c(".", .libPaths()))
install.packages("htmltools", repos = "https://cloud.r-project.org")
install.packages("pkgdown", repos = "https://cloud.r-project.org")

write('-- Build API .R -> .rd -----------------------------------------------------', stderr())
devtools::document(pkg = pkg)

write('-- Build site using pkgdown ------------------------------------------------', stderr())
pkgdown::build_site(pkg = pkg)
