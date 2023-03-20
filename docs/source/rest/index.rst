RESTful API
===========
Cell atlas approximations are designed to be readable by machines independent of programming language. For this purpose, a RESTful API is provided.

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

