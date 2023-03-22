Python
======
The Python interface can be used to access the atlas approximation API from Python. It uses caching to speed up multiple requests so it is generally as fast or faster than using the REST API directly.

Requirements
------------
You need the following Python packages:
  - ``requests``
  - ``pandas``

Installation
------------
You can use `pip` to install the `atlasapprox` package:

.. code-block:: bash

  pip install atlasapprox

Getting started
---------------
Instantiate the ``API`` object:

.. code-block:: Python

   api = atlasapprox.API()

Use whichever method you wish, e.g.:

.. code-block:: Python

   human_organs = api.organs(organism="h_sapiens")
   print(human_organs)

Each method is described in detail below.

Reference API
-------------
.. automodule:: atlasapprox
   :members:
