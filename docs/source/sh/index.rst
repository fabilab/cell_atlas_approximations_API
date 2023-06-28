Shell
=====
The shell interface can be used to access the atlas approximation API from a UNIX terminal (e.g. bash, zsh). It is a single executable.

Quick start
-----------
.. code-block:: bash

   atlasapprox average --organism=m_musculus --organ=Lung --features=Col1a1,Ptprc
   
Requirements
------------
  - A UNIX terminal. Windows will probably not work, but if you need Windows terminal support, please open a GitHub issue and we can
work together to find a solution.
  - `curl`: Future versions will support other cli request handlers such as `wget`.

Installation
------------
Download the [script](https://raw.githubusercontent.com/fabilab/cell_atlas_approximations_API/main/shell/atlasapprox) and place it in a folder within your `$PATH`.
Alternatively, place it in whatever folder and call it via relative or absolute path. Or add that folder to your path (e.g. in your `.bashrc`).

Getting started
---------------
Run the script with the `--help` flag to read instructions and examples:

.. code-block:: bash

   atlasapprox --help

Use whichever option you wish, e.g.:

.. code-block:: bash

   atlasapprox celltypexorgan --organism=h_sapiens

If you are exploring the API from scratch, you would usually:

  1. Ask about available `organisms`.
  2. Ask about available `organs` within your organism of interest.
  3. Ask about `average` gene expression in that organ.

Reference API
-------------
Positional arguments available are exact mirrors of the REST API endpoints, e.g. `average`, `organisms`, `data_sources`, etc. Flag options are used to pass parameters to the data request, e.g. to specify what organism, organ, and cell type you are querying about, and are described in the REST API documentation.
