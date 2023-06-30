.. Cell Atlas Approximations API documentation master file, created by
   sphinx-quickstart on Mon Mar 20 10:21:07 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

API for cell atlas approximations
=================================
Cell atlases are single cell omics data sets describing multiple organs and ideally entire organisms. A `cell atlas approximation <https://chanzuckerberg.com/science/programs-resources/single-cell-biology/data-insights/light-and-scalable-statistical-approximations-of-cell-atlases/>`_ is a lightweight, lossy compression of a cell atlas that retains key informtation while reducing data size and complexity.

.. note::

   While approximations are currently limited to single cell transcriptomic data, future support for chromatin accessibility and other single-cell assays is planned, with much of the code infrastructure already set up.

Because of their small size, atlas approximations are well suited for acess over a RESTful API, which is described in this page.

.. note::

   To access cell atlas approximations using a Human Interface (HI) instead, check out our friendly chat bot @ https://atlasapprox.org. Please be nice to the bot 😊 - it's not very smart yet.

**Examples of API usage**:
  - Ask the average expression of a set of genes in a cell type, organ, and organism.
  - List the cell types across an entire organism that have the highest expression of a certain gene.
  - Find marker genes for a specific cell type.
  - Show a table of which cell types are found in multiple tissues (e.g. various kinds immune cells).

Version
-------
The most recent version of the API is **v1**.

Interfaces
----------
There are multiple ways to access atlas approximations programmatically:

.. toctree::
   :maxdepth: 1

   Python <python/index>
   R <R/index>
   JavaScript <js/index>
   UNIX shell (bash, zsh, etc.) <sh/index>
   REST (language-agnostic) <rest/index>

.. note::

   All interfaces use the REST API internally and provide a convenience layer for users of specific languages.

Embedding in a web page
-----------------------
It is relatively easy to embed API calls to cell atlas approximations in a web page through the JavaScript and REST interfaces:

.. toctree::
   :maxdepth: 1

   rest/embed

Authors
-------
**Fabio Zanini** @ `fabilab <https://fabilab.org>`_.

Citation
--------
**Ying Xu and Fabio Zanini**. Lightweight and scalable approximations democratise access to single cell atlases. In preparation (2023).

Data Sources
------------
- *Homo sapiens*: [Tabula Sapiens](https://www.science.org/doi/10.1126/science.abl4896)
- *Mus musculus*: [Tabula Muris Senis](https://www.nature.com/articles/s41586-020-2496-1)
- *Mus myoxinus*: [Tabula Microcebus](https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)
- *Caenorhabditis elegans*: [Cao et al. 2017](https://www.science.org/doi/10.1126/science.aam8940)
- *Danio rerio*: [Wagner et al. 2018](https://www.science.org/doi/10.1126/science.aar4362)
- *Spongilla lacustris*: [Musser et al. 2021](https://www.science.org/doi/10.1126/science.abj2949)
- *Amphimedon queenslandica*, *Mnemiopsis leidyi*, and *Trichoplax adhaerens*: [Sebé-Pedrós et al 2018](https://www.nature.com/articles/s41559-018-0575-6)
