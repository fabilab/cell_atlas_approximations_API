.. Cell Atlas Approximations API documentation master file, created by
   sphinx-quickstart on Mon Mar 20 10:21:07 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

API for cell atlas approximations
=================================
Cell atlases such as Tabula Muris and Tabula Sapiens are multi-organ single cell omics data sets describing entire organisms. A cell atlas approximation is a lossy and lightweight compression of a cell atlas that can be streamed over a RESTful API.

This project enables biologists, doctors, and data scientist to quickly find answers for questions such as:

- *What is the expression of a specific gene in human lung?*
- *What are the marker genes of a specific cell type in mouse pancreas*?
- *What fraction of cells (of a specific type) express a gene of interest?*

These questions can be asked in Python or R using the provided packages (see below), or in a language agnostic manner using the REST API.

Version
-------
The most recent version of the API is **v1**.

API interfaces
--------------
There are three ways to access the data programmatically: Python, R, or REST (language-agnostic).

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   rest/index
   python/index
   R/index
   rest/embed

Authors
-------
**Fabio Zanini** @ [fabilab](https://fabilab.org)

Citation
--------
Ying Xu and Fabio Zanini. Lightweight and scalable approximations democratise access to single cell atlases. In preparation (2023).

Data Sources
------------
- *Homo sapiens*: [Tabula Sapiens](https://www.science.org/doi/10.1126/science.abl4896)
- *Mus musculus*: [Tabula Muris Senis](https://www.nature.com/articles/s41586-020-2496-1)
- *Mus myoxinus*: [Tabula Microcebus](https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)
- *Caenorhabditis elegans*: [Cao et al. 2017](https://www.science.org/doi/10.1126/science.aam8940)
- *Danio rerio*: [Wagner et al. 2018](https://www.science.org/doi/10.1126/science.aar4362)
- *Spongilla lacustris*: [Musser et al. 2021](https://www.science.org/doi/10.1126/science.abj2949)
- *Amphimedon queenslandica*, *Mnemiopsis leidyi*, and *Trichoplax adhaerens*: [Sebé-Pedrós et al 2018](https://www.nature.com/articles/s41559-018-0575-6)
