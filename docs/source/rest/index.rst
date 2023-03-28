REST
====
Cell atlas approximations are designed to be readable by machines independent of programming language. For this purpose, a RESTful API is provided.

The current version of the RESTful API is **v1**.

Quick start
-----------
.. tabs::

   .. tab:: **Python**

      .. code-block:: python
      
        import requests
        response = requests.get(
            'http://api.atlaxapprox.org/v1/organs',
            params=dict(organism='h_sapiens'),
        )
        print(response.json())


   .. tab:: **R**

      .. code-block:: R
      
        response <- httr::GET('http://api.atlasapprox.org/v1/organs')
        print(reponse)

   .. tab:: **JavaScript**

      .. code-block:: javascript

        var xmlHttp = new XMLHttpRequest();
        xmlHttp.onreadystatechange = function() { 
            if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                console.log(xmlHttp.responseText);
        }
        xmlHttp.open("GET", 'http://api.atlasapprox.org/v1/organs', true);
        xmlHttp.send(null);

Getting started
---------------
- The API generally accepts **GET** requests only.
- For data involving gene expression, only 50 features at a time are supported to reduce egress throughput.
- No aliases for names (e.g. organisms, genes) are supported yet: please double check your spelling.
- If you can use one of the languge-dedicated APIs (e.g. the Python API), please do so instead of using the REST API. Language-specific packages use caching to reduce load on our servers and also give you faster answers, so it's a win-win.

.. note::
   Mouse genes are generally spelled with only the first letter capitalised, while human genes
   are spelled ALL CAPS.

If you are starting to explore the API from scratch, you can start by asking:

1. What organisms are available.
2. What organs are covered in your organism of choice.
3. What cell types are found in your organism and organ of interest.

After that you can query gene expression in specific cell types, organs, and organisms.

Reference API
-------------
The complete API is described below. Endpoints refer to the end of the URL only. For instance,
to query ``organisms``, the **endpoint** description is ``/organisms`` so the full URL is ``http://api.atlasapprox.org/v1/organisms``.

organisms
+++++++++
**Endpoint**: ``/organisms``

**Parameters**: None 

**Returns**: A dict with only one key, containing a list of organisms for which an atlas approximation is available.


organs
++++++
**Endpoint**: ``/organs``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.

**Returns**: A dict with two keys, one for the organism requested and one for the list of organs in that organism.


features
++++++++
**Endpoint**: ``/features``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with two keys, one for the organism and one for the list of features (e.g. genes) of that organism.
   
.. note::
   All organs within one organism use the same features, in the same order.

celltypes
+++++++++
**Endpoint**: ``/celltypes``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with three keys: one for the organism, one for the organ, and one for a list of cell types for that organism and organ.

average
+++++++
**Endpoint**: ``/average``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.

**Returns**: A dict containing organism, organ, features found, units of measurement, cell types, and averages. The latter is a list of lists, with the outer dimension determined by the cell types and the inner dimension determined by the features.


fraction_detected
+++++++++++++++++
**Endpoint**: ``/fraction_detected``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.

**Returns**: A dict containing organism, organ, features found, units of measurement, cell types, and fractions. The latter is a list of lists, with the outer dimension determined by the cell types and the inner dimension determined by the features.


markers
+++++++
**Endpoint**: ``/markers``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``celltype``: The cell type for which marker features are requested.
  - ``number``: The number of marker features to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with four keys: one for the organism, one for the organ, one for the cell type, and one containing a list of features (e.g. genes) that mark the chosen cell type, i.e. they are detected at higher levels in that cell type than in the other ones from the same organ.

.. note::
   There are multiple methods to determine marker features (e.g. genes). Future versions of the API might allow the user to choose between methods. For the time being, the method is fixed.

data_sources
++++++++++++
**Endpoint**: ``/data_sources``

**Returns**: A dict with a key per organism listing the cell atlases (data sources) used for the approximations.
