[![Documentation Status](https://readthedocs.org/projects/atlasapprox/badge/?version=latest)](https://apidocs.atlasapprox.org/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/atlasapprox.svg)](https://badge.fury.io/py/atlasapprox)
![CRAN Downloads](https://cranlogs.r-pkg.org/badges/atlasapprox)

Cell Atlas Approximations - API
===============================
Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed via the internet.

This project enables biologists, doctors, and data scientist to quickly find answers for questions such as:

- *What is the expression of a specific gene in human lung?*
- *What are the marker genes of a specific cell type in mouse pancreas*?
- *What fraction of cells (of a specific type) express a gene of interest?*

These questions can be asked in Python or R using the provided packages (see below), or in a language agnostic manner using the REST API.

Version
-------
The latest API version is `v1`.

We support several organs and organisms: human, mouse, lemur (a type of monkey), zebrafish, C. elegans. More organisms and organs are planned for the near future.

Documentation
-------------
Tutorial and reference documentation is available at [https://atlasapprox.readthedocs.io](https://atlasapprox.readthedocs.io).

Usage (REST)
------------
The REST interface is language-agnostic and can be queried using any HTTP request handler, e.g. in JavaScript:

```javascript
var xmlHttp = new XMLHttpRequest();
xmlHttp.onreadystatechange = function() { 
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
        console.log(xmlHttp.responseText);
}
xmlHttp.open("GET", 'http://api.atlasapprox.org/v1/organs', true);
xmlHttp.send(null);
```

Similar results can be obtained via Python's `requests`, R's `httr`, etc. If you are using Python or R, however, please consider using the dedicated interfaces below, as they are more efficient and easier on our servers thanks to caching.

Usage (Python)
--------------
The Python interface uses a central `API` class. Its methods implement the REST endpoints:

```python
import atlasapprox

api = atlasapprox.API()
print(api.organisms())
print(api.celltypes(organism="c_elegans", organ="whole"))
```

Usage (R)
--------------
The R interface includes a number of `GetXXX` functions connected to the REST endpoints:

```R
library("atlasapprox")

organisms <- GetOrganisms()
print(organisms)
```

Repo contents
-------------
- `data`: files required for the compression of current cell atlases
- `preprocess`: scripts used for the approximations
- `web`: webserver code in Flask that implements the RESTful API
- `Python`: package code providing a Python interface for the RESTful API
- `R`: package code providing an R interface for the RESTful API
- `docs`: user documentation for the API
