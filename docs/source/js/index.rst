JavaScript
==========
The JavaScript interface can be used to access the atlas approximation API from nodejs or a web page.

Quick start
-----------
.. code-block:: javascript

   let average_expression;
   (async () => {
     average_expression = await atlasapprox.average(
       organism = "m_musculus", organ = "Lung", features=["Col1a1", "Ptprc"],
     );
     console.log(average_expression);
   })();
   
Requirements
------------
The JavaScript library has no dependencies, just good ol' ES6.

Installation
------------
You can use `npm` to install the `atlasapprox` package:

.. code-block:: bash

  npm install atlasapprox

Getting started
---------------
Import or require the ``API`` object:

.. code-block:: javascript

   api = require('atlasapprox');

Use whichever method you wish, e.g.:

.. code-block:: javascript

   let human_organs = await api.organs(organism="h_sapiens")
   console.log(human_organs)

If you are exploring the API from scratch, you would usually:

  1. Ask about available `organisms`.
  2. Ask about available `organs` within your organism of interest.
  3. Ask about `average` gene expression in that organ.

Each API method is described in detail below.

Reference API
-------------
For now, you can look at the [test script](https://github.com/fabilab/cell_atlas_approximations_API/blob/main/js/test/script.js) for usage examples.
