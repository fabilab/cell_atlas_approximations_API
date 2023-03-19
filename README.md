Cell Atlas Approximations - API
===============================
(WIP!)

Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed over a RESTful API.

This repo contains:
- code implementing such an API
- documentation for end users of the API itself
- a Python package to interface with the API

Version
-------
The latest API version is `v1`.

Installation
------------
The RESTful API can be queried using any HTTP request handler, e.g. Python's `requests`:
```python

import requests

# Get a list of human organs covered by the API
requests.get(
    '<baseurl>/api/v1/organs',
    organism='homo_sapiens',
)
```


Documentation
-------------
Documentation of the RESTful API and its Python interface is available at https://api.atlasapprox.org (WIP).



Repo contents
-------------
- `data`: files required for the compression of current cell atlases
- `preprocess`: scripts used for the approximations
- `web`: webserver code in Flask that implements the RESTful API
- `Python`: package code providing a Python interface for the RESTful API
- `R`: package code providing an R interface for the RESTful API
- `docs`: user documentation for the API
