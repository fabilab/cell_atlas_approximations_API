[![Documentation Status](https://readthedocs.org/projects/atlasapprox/badge/?version=latest)](https://apidocs.atlasapprox.org/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/atlasapprox.svg)](https://badge.fury.io/py/atlasapprox)
[![npm version](https://badge.fury.io/js/@fabilab%2Fatlasapprox.svg)](https://badge.fury.io/js/@fabilab%2Fatlasapprox)
![CRAN Downloads](https://cranlogs.r-pkg.org/badges/atlasapprox)

<img src="https://raw.githubusercontent.com/fabilab/cell_atlas_approximations/main/figures/figure_API.png" width="150" height="150">

# Cell Atlas Approximations - JavaScript API
Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed via the internet.

This project enables biologists, doctors, and data scientist to quickly find answers for questions such as:

- *What types of cells populate the human heart?*
- *What is the expression of a specific gene across cell types in C elegans?*
- *What are the marker genes of a specific cell type in mouse pancreas*?
- *What fraction of cells (of a specific type) express a gene of interest?*

This package enables users to ask those questions using the JavaScript API.

## Version
The latest API version is `v1`.

We support several organs and organisms: human, mouse, lemur (a type of monkey), zebrafish, C. elegans. More organisms and organs are planned for the near future.

## Documentation
Tutorial and reference documentation is available at [https://atlasapprox.readthedocs.io](https://atlasapprox.readthedocs.io).

## Usage
An object containing one function for each API endpoint is exported by the `@fabilab/atlasapprox` npm package:

```javascript
// EC6 imports
import atlasapprox from '@fabilab/atlasapprox';
// CommonJS variant
//let atlasapprox = require('@fabilab/atlasapprox');

(async () => {
  let data = await atlasapprox.organisms();
  console.log(data);
  }  
})();

```

## Authors
- [Fabio Zanini @ fabilab](https://fabilab.org)
- [Ying Xu @ fabilab](https://fabilab.org/pages/people.html)
