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
**Fabio Zanini**, **Ying Xu**, **Johanna Ahn**, **Amber Xu**, **Liuyi Chen** @ `fabilab <https://fabilab.org>`_.

Citation
--------
**Xu et al.** (2024) Lightweight and scalable approximations democratise access to single cell atlases. [biorxiv](https://www.biorxiv.org/content/10.1101/2024.01.03.573994v1).

Data Sources
------------
Animals:

- *Homo sapiens*: 
  - RNA: [Tabula Sapiens](https://www.science.org/doi/10.1126/science.abl4896)
  - ATAC: [Zhang et al. 2021](https://doi.org/10.1016/j.cell.2021.10.024)
- *Amphimedon queenslandica*: [Sebé-Pedrós et al 2018](https://www.nature.com/articles/s41559-018-0575-6)
- *Caenorhabditis elegans*: [Cao et al. 2017](https://www.science.org/doi/10.1126/science.aam8940)
- *Crassostrea gigas*: [Piovani et al. 2023](https://doi.org/10.1126/sciadv.adg6034)
- *Clytia hemisphaerica*: [Chari et al. 2021](https://www.science.org/doi/10.1126/sciadv.abh1683#sec-4)
- *Danio rerio*: [Wagner et al. 2018](https://www.science.org/doi/10.1126/science.aar4362)
- *Drosophila melanogaster* (fruitfly): [Li et al. 2022](https://doi.org/10.1126/science.abk2432
- *Hofstenia miamia*: [Hulett et al. 2023](https://www.nature.com/articles/s41467-023-38016-4)
- *Isodiametra pulchra*: [Duruz et al. 2020](https://academic.oup.com/mbe/article/38/5/1888/6045962)
- *Microcebus murinus*: [Tabula Microcebus](https://www.biorxiv.org/content/10.1101/2021.12.12.469460v2)
- *Mnemiopsis leidyi*: [Sebé-Pedrós et al 2018](https://www.nature.com/articles/s41559-018-0575-6)
- *Mus musculus*: [Tabula Muris Senis](https://www.nature.com/articles/s41586-020-2496-1)
- *Nematostella vectensis*: [Steger et al 2022](https://doi.org/10.1016/j.celrep.2022.111370)
- *Prostheceraeus crozieri*: [Piovani et al. 2023](https://doi.org/10.1126/sciadv.adg6034)
- *Platynereis dumerilii*: [Achim et al 2017](https://academic.oup.com/mbe/article/35/5/1047/4823215)
- *Strongylocentrotus purpuratus* (sea urchin): [Paganos et al. 2021](https://doi.org/10.7554/eLife.70416)
- *Schistosoma mansoni*: [Li et al. 2021](https://www.nature.com/articles/s41467-020-20794-w)
- *Schmidtea mediterranea*: [Plass et al 2018](https://www.science.org/doi/10.1126/science.aaq1723#sec-10)
- *Spongilla lacustris*: [Musser et al. 2021](https://www.science.org/doi/10.1126/science.abj2949)
- *Stylophora pistillata*: [Levi et al. 2021](https://www.sciencedirect.com/science/article/pii/S0092867421004402)
- *Trichoplax adhaerens*: [Sebé-Pedrós et al 2018](https://www.nature.com/articles/s41559-018-0575-6)
- *Xenopus laevis*: [Liao et al 2022](https://www.nature.com/articles/s41467-022-31949-2#ref-CR14)

Plants:
- *Arabidopsis thaliana*: [Shahan et al 2022](https://www.sciencedirect.com/science/article/pii/S1534580722000338), [Xu et al. 2024](https://www.biorxiv.org/content/10.1101/2024.03.04.583414v1)
- *Lemna minuta*: [Abramson et al. 2022](https://doi.org/10.1093/plphys/kiab564)
- *Fragaria vesca*: [Bai et al. 2022](https://doi.org/10.1093/hr/uhab055)
- *Oryza sativa*: [Zhang et al. 2022](https://doi.org/10.1038/s41467-021-22352-4)
- *Triticum aestivum* (wheat): [Zhang et al 2023](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-023-02908-x)
- *Zea mays* (maize/corn): [Marand et al. 2021](https://doi.org/10.1016/j.cell.2021.04.014), [Xu et al. 2024](https://www.biorxiv.org/content/10.1101/2024.03.04.583414v1)
