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

General rules
-------------
- The API generally accepts **GET** requests only.
- For data involving gene expression, only 50 features at a time are supported to reduce egress throughput.
- No aliases for names (e.g. organisms, genes) are supported yet: please double check your spelling.
- If you can use one of the languge-dedicated APIs (e.g. the Python API), please do so instead of using the REST API. Language-specific packages use caching to reduce load on our servers and also give you faster answers, so it's a win-win.

.. note::
   Mouse genes are generally spelled with only the first letter capitalised, while human genes
   are spelled ALL CAPS.

Entry points
------------
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

**Returns**: A list of organisms for which an atlas approximation is available.


organs
++++++
**Endpoint**: ``/organs``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.

**Returns**: A list of organs for one organism, for which an atlas approximation is available.


features
++++++++
**Endpoint**: ``/features``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A list of features (e.g. genes) for one organism, for which an atlas approximation is available.
   
.. note::
   All organs within one organism use the same features, in the same order.

celltypes
+++++++++
**Endpoint**: ``/celltypes``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A list of cell types for one organism and organ. To obtain a list with the union of all cell types across organs, set ``organ`` equal to ``whole`` in your request.

average
+++++++
**Endpoint**: ``/average``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A map. Each key is a cell type in the chosen organ, each value is a list of average measurement in the cell atlas for the requested features, in the same order.


fraction_detected
+++++++++++++++++
**Endpoint**: ``/fraction_detected``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A map. Each key is a cell type in the chosen organ, each value is a list, with each element corresponding to a queried feature, in the same order. Each item represents the fraction of cells within that type in which the requested feature was detected (e.g. nonzero).


markers
+++++++
**Endpoint**: ``/markers``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``celltype``: The cell type for which marker features are requested.
  - ``number``: The number of marker features to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A list of features (e.g. genes) that mark one cell type, i.e. they are detected at higher levels in that cell type than in the other ones from the same organ.

.. note::
   There are multiple methods to determine marker features (e.g. genes). Future versions of the API might allow the user to choose between methods. For the time being, the method is fixed.
