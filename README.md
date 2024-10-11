<table>
  <tr>
    <td></td>
    <td>REST</td>
    <td>Python</td>
    <td>R</td>
    <td>JS</td>
    <td>Shell</td>
  </tr>
  <tr>
    <td>Build</td>
    <td><a href="https://github.com/fabilab/cell_atlas_approximations_API/actions"><img src="https://github.com/fabilab/cell_atlas_approximations_API/actions/workflows/rest_test.yml/badge.svg"></a></td>
    <td>[![Python CI](https://github.com/fabilab/cell_atlas_approximations_API/actions/workflows/python_build.yml/badge.svg)](https://github.com/fabilab/cell_atlas_approximations_API/actions)</td>
    <td>(missing)</td>
    <td>[![JS CI](https://github.com/fabilab/cell_atlas_approximations_API/actions/workflows/js_test.yml/badge.svg)](https://github.com/fabilab/cell_atlas_approximations_API/actions)</td>
    <td>(missing)</td>
  </tr>
  <tr>
    <td>Release</td>
    <td>REST</td>
    <td>[![PyPI version](https://badge.fury.io/py/atlasapprox.svg)](https://badge.fury.io/py/atlasapprox)</td>
    <td>![CRAN Downloads](https://cranlogs.r-pkg.org/badges/atlasapprox)</td>
    <td>[![npm version](https://badge.fury.io/js/@fabilab%2Fatlasapprox.svg)](https://badge.fury.io/js/@fabilab%2Fatlasapprox)</td>
    <td>(see repo)</td>
  </tr>
  <tr>
    <td>Docs</td>
    <td colspan="5">[![Documentation Status](https://readthedocs.org/projects/atlasapprox/badge/?version=latest)](https://apidocs.atlasapprox.org/en/latest/?badge=latest)</td>
  </tr>
</table>

<img src="https://raw.githubusercontent.com/fabilab/cell_atlas_approximations/main/figures/figure_API.png" width="150" height="150">

# Cell Atlas Approximations - API
Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed via the internet.

This project enables biologists, doctors, and data scientist to quickly find answers for questions such as:

- *What types of cells populate the human heart?*
- *What is the expression of a specific gene across cell types in C elegans?*
- *What are the marker genes of a specific cell type in mouse pancreas*?
- *What fraction of cells (of a specific type) express a gene of interest?*

These questions can be asked in Python or R using the provided packages (see below), or in a language agnostic manner using the REST API. We even made a shell script for Linux and Mac that calls the API from your terminal! - check out [shell/atlasapprox](https://github.com/fabilab/cell_atlas_approximations_API/blob/main/shell/atlasapprox)!

## Version
The latest API version is `v1`.

We support several organs and organisms: human, mouse, lemur (a type of monkey), zebrafish, C. elegans. More organisms and organs are planned for the near future.

## Documentation
Tutorial and reference documentation is available at [https://atlasapprox.readthedocs.io](https://atlasapprox.readthedocs.io).

## Usage
<details> 

<summary> REST </summary>

### REST
The REST interface is language-agnostic and can be queried using any HTTP request handler, e.g. in JavaScript:

```javascript
(async () => {
  let response = await fetch("http://api.atlasapprox.org/v1/organisms");
  if (response.ok) {
    let data = await response.json();
    console.log(data);
  }  
})();
```

Similar results can be obtained via Python's `requests`, R's `httr`, etc. If you are using Python or R, however, please consider using the dedicated interfaces below, as they are more efficient and easier on our servers thanks to caching.
</details>

<details>
  <summary>Python</summary>

### Python
The Python interface uses a central `API` class. Its methods implement the REST endpoints:

```python
import atlasapprox

api = atlasapprox.API()
print(api.organisms())
print(api.celltypes(organism="c_elegans", organ="whole"))
```
</details>

<details>
  <summary>R</summary>

### R
The R interface includes a number of `GetXXX` functions connected to the REST endpoints:

```R
library("atlasapprox")

organisms <- GetOrganisms()
print(organisms)
```
</details>

<details>
  <summary>JavaScript</summary>

### JavaScript/nodejs
An object containing one function for each API endpoint is exported by the `atlasapprox` npm package:

```javascript
let atlasapprox = require('atlasapprox');
(async () => {
  let data = await atlasapprox.organisms();
  console.log(data);
  }  
})();

```
</details>

<details>
  <summary>Shell</summary>

### Shell (bash, zsh, et similia)
A single script is provided in this repo under `shell/atlasapprox`. Usage instructions are included, but as a quick example:

```bash
atlasapprox average --organism=m_musculus --organ=Lung --features=Col1a1,Ptprc
```

Note that the output is a serialized JSON string: you'll probably need some kind of parser to interpret the results.

</details>

## Repo contents
- `data`: files required for the compression of current cell atlases
- `preprocess`: scripts used for the approximations
- `web`: webserver code in Flask that implements the RESTful API
- `Python`: package code providing a Python interface for the RESTful API
- `R`: package code providing an R interface for the RESTful API
- `docs`: user documentation for the API

## Authors
- [Fabio Zanini @ fabilab](https://fabilab.org)
