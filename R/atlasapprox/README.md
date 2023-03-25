# R
The R interface can be used to access the atlas approximation API from R. It uses caching to speed up multiple requests so it is generally as fast or faster than using the [REST API](../index.html) directly.

## Requirements
You need the following R packages:

  - `httr`

## Installation
You can install the package from CRAN (WIP!):
```R
install.packages("atlasapprox")
```

## Getting started
Load the library:
```R
library("atlasapprox")
```

You now have access to the `GetXXX` functions within `atlasapprox`, e.g.:
```R
human_organs <- GetOrgans(organism = "h_sapiens")
```

See the Reference page for details on each function.
