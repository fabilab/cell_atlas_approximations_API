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
            'http://api.atlasapprox.org/v1/organs',
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
        xmlHttp.open("GET", 'http://api.atlasapprox.org/v1/organisms', true);
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
The complete API is described below. Endpoints refer to the end of the URL only. For
instance, to query a list of available organisms, the **endpoint** description is ``/organisms`` so the full URL is ``http://api.atlasapprox.org/v1/organisms``.

Measurement types
+++++++++++++++++
**Endpoint**: ``/measurement_types``

**Parameters**: None

**Returns**: A dict with the following key-value pairs:
  - ``measurement_types``: The types of measurements (e.g. gene expression, chromatin accessibility). Not all organisms and organs are available for all measurement types, of course.

Organisms
+++++++++
**Endpoint**: ``/organisms``

**Parameters**:
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organisms``: The organisms available.


Organs
++++++
**Endpoint**: ``/organs``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organism``: The organism chosen.
  - ``organs``: The available organs for that measurement type and organism.

Features
++++++++
**Endpoint**: ``/features``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The type of measurement (e.g. gene expression, chromatin accessibility).
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``features``: The features available for that organism and measurement type.

   
.. note::
   All organs within one organism use the same features, in the same order.

Cell types
++++++++++
**Endpoint**: ``/celltypes``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen (same comment).
  - ``celltypes``: The list of cell types for that organism and organ.

Cell type location
++++++++++++++++++
**Endpoint**: ``/celltype_location``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``celltype``: The cell type to find organs/locations for.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``celltype``: The cell type chosen.
  - ``organs``: A list of organs in which that cell type was detected.

Table of cell types x organ
+++++++++++++++++++++++++++
**Endpoint**: ``/celltypexorgan``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organs`` (optional): A list of organs of interest. If not specified, all organs from the chosen organism will be used. If specified, must be a subset of the available ones for the chosen organism. A special value, ``whole``, returns the union of all cell types across all organs.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.
  - ``boolean`` (optional, default ``false``): Whether to return a boolean presence/absence matrix
        (if ``true``) or the number of cells/nuclei sampled for each type and organ (if ``false``).

**Returns**: An object/dict with the following keys:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organs``: A list of organs chosen.
  - ``celltypes``: A list containing all celltypes from any of the chosen organs or, if no organs were specified, from the whole organism. They are ordered from celltypes detected in most organs to the ones found in only one organ.
  - ``detected``: A table (list of lists) of numeric values. If ``boolean`` was set to ``true``, ``1`` or ``true`` means that cell type was detected in that organ. Otherwise, this is the number of samples cells/nuclei from that cell type and organ, without any normalisation. Order of rows and columns as in the ``organs`` and ``celltypes`` part of the returned object.

Averages
++++++++
**Endpoint**: ``/average``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen.
  - ``features``: The features requested. Any spelling correction is included here.
  - ``celltypes``: A list containing all celltypes from any of the chosen organ.
  - ``average``: The average measurement (e.g. gene expression) for each cell type and feature.
  - ``unit``: The unit of measurement for this measurement type.

Fraction of cells with signal
+++++++++++++++++++++++++++++
**Endpoint**: ``/fraction_detected``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``features``: A list of features (e.g. genes) for which the average measurement in the atlas is requested.
  - ``measurement_type`` (optional, default ``gene_expresion``): What kind of measurement to query about. 

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen.
  - ``features``: The features requested. Any spelling correction is included here.
  - ``celltypes``: A list containing all celltypes from any of the chosen organ.
  - ``fraction_detected``: The fraction of cells with detected signal (e.g. gene expression) for each cell type and feature.

.. note::
   For some measurement types (e.g. chromatin accessibility), fraction of cells with signal is currently defined as exactly equal the average measurement, so the two API calls are equivalent except for the keys of the output dictionary.

Marker features
+++++++++++++++
**Endpoint**: ``/markers``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``celltype``: The cell type for which marker features are requested.
  - ``number``: The number of marker features to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen (this confirms it exists in the database).
  - ``organ``: The organ chosen.
  - ``celltype``: The cell type chosen.
  - ``markers``: The markers (e.g. genes, peaks) that are measured at higher level in the chosen cell type compared to other cell types within the same organ.

.. note::
   There are multiple methods to determine marker features (e.g. genes). Future versions of the API might allow the user to choose between methods.

Highest-measurement cell types
++++++++++++++++++++++++++++++
**Endpoint**: ``/highest_measurement``

**Parameters**:
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``feature``: The feature to look for.
  - ``number``: The number of cell types to return.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism chosen.
  - ``feature``: The feature chosen.
  - ``celltypes``: A list of cell types with the highest measurement (e.g. expression) for that feature
  - ``organs``: A list of corresponding organs. This parameter and ``celltypes`` should be interpreted together as pairs that fully specify cell types.
  - ``average``: average measurement (e.g. expression) in those cell types and organs.
  - ``unit``: The unit of measurement for the average measurement returned.

Similar features
++++++++++++++++
**Endpoint**: ``/similar_features``

**Parameters**:
  - ``organism``: The organism of interest.
  - ``organ``: The organ of interest.
  - ``feature``: The original feature to look for similar features of.
  - ``number``: How many similar features to return.
  - ``method``: Method to use to compute distance between features. Available methods are:
    - ``correlation`` (default): Pearson correlation of the ``fraction_detected``.
    - ``cosine``: Cosine similarity/distance of the ``fraction_detected``.
    - ``euclidean``: Euclidean distance of average measurement (e.g. expression).
    - ``manhattan``: Taxicab/Manhattan/L1 distance of average measurement.
    - ``log-euclidean``: Log the average measurement with a pseudocount of 0.001, then compute euclidean distance. This tends to highlight sparsely measured features.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``method``: The method used.
  - ``feature``: The requested feature.
  - ``similar_features``: A list of similar features (e.g. genes) to the one requested.
  - ``distances``: Distances of the listed feature in the method chosen. For correlation/cosine methods, the distance is 1 - correlation.

Similar cell types
++++++++++++++++++
**Endpoint**: ``/similar_celltypes``

**Parameters**:
  - ``organism``: The organism of interest.
  - ``organ``: The organ of the cell type of interest. This parameter, together with the ``celltype`` parameter, constitute a full specification of the type of cells you are focusing on. Note that the similar cell types will *not* be restricted to this organ.
  - ``celltype``: The cell type of interest, to find similar types to. This parameter works jointly with the ``organ`` parameter, see above.
  - ``number``: How many similar cell types are requested.
  - ``features``: What features (genes, chromatin peaks, etc.) to use to determine similarity. Because many measurement spaces are high-dimensional, similarities are not meaningful without a feature selection (https://en.wikipedia.org/wiki/Curse_of_dimensionality). The same does *not* apply to the ``/similar_features`` endpoint, because there are only a few dozens cell types within an organ, so the space is relatively low-dimensional.
  - ``method`` (optional, default ``correlation``): What method to use to compute similarity. Currently available methods are:
    - ``correlation``: Pearson correlation of fraction detected.
    - ``euclidean``: Euclidean (L2) distance of average measurement.
    - ``manhattan``: Manhattan (L1) distance of average measurement.
    - ``log-euclidean``: Take the log of the measurement, then Euclidean distance. This emphasizes low-detected features, but also amplifies noise if the features are not selected carefully.
  - ``measurement_type`` (default: ``gene_expression``): Optional parameter to choose what type of measurement is sought. Currently, only ``gene_expression`` is supported.

**Returns**: A dict with the following key-value pairs:
  - ``measurement_type``: The measurement type selected.
  - ``organism``: The organism of interest. Must be one of the available ones as returned by ``organisms``.
  - ``organ``: The organ of interest. Must be among the available ones for the chosen organism.
  - ``celltype``: The cell type of interest.
  - ``method``: The method used.
  - ``features``: The requested features.
  - ``similar_celltypes``: A list of similar cell types. This should be interpreted in tandem with the ``similar_organs`` key below.
  - ``similar_organs``: A list of the organs for the similar cell types. This should be interpreted together with the ``similar_celltypes`` key above. Each pair of ``(organ, celltype)`` fully specifies a similar cell type.
  - ``distances``: Distances of the listed cell types in the method chosen. For correlation/cosine methods, the distance is 1 - correlation.

Data Sources
++++++++++++
**Endpoint**: ``/data_sources``

**Returns**: A dict with a key per organism listing the cell atlases (data sources) used for the approximations.
