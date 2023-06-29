Embedding atlas approximations in a web page
============================================
Atlas approximations are very lightweight and therefore suitable for embedding in web pages (e.g. to augment functionality of a dashboard). This page explains how to do that.

Context: Web browsers
---------------------
Web pages are parsed and rendered by a browser onto your screen. Browsers currently understand two programming languages:

 - `JavaScript <https://en.wikipedia.org/wiki/ECMAScript>`_
 - `WebAssembly <https://webassembly.org/>`_

While WebAssembly is useful for specific, performance-sensitive applications, 99% of the web is built on top of JavaScript. That's why the REST API for atlas approximations includes an example in JavaScript as well.

Examples
--------
Embedding via JavaScript can be achieved either by querying the REST APIs directly (see pure JS and jQuery examples below) or by passing through the npm package `atlasapprox` (see
React example below). Needless to say, the API is also compatible with other frameworks such as Vuejs.

.. tabs::

  .. tab:: **Pure JavaScript**

    .. code-block:: html

      <html>
        <head></head>
        <body>
          <div>Hello world!</div>
          <script>
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() { 
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    console.log(xmlHttp.responseText);
            }
            xmlHttp.open("GET", 'http://api.atlasapprox.org/v1/organisms', true);
            xmlHttp.send(null);
          </script>
        </body>
      </html>

  .. tab:: **jQuery**

    .. code-block:: html

      <html>
        <head>
        <script src="https://code.jquery.com/jquery-3.7.0.min.js"
		integrity="sha256-2Pmvv0kuTBOenSvLm6bvfBSSHrUJ+3A7x6P5Ebd07/g="
		crossorigin="anonymous">
        </script>
        </head>
        <body>
          <div>Hello world!</div>
          <script>
            $.ajax({
                url: 'https://api.atlasapprox.org/v1/organisms',
                success: function (result) {
                    console.log(result);
                },
            })
          </script>
        </body>
      </html>

  .. tab:: **React**

    .. code-block:: 

      import atlasapprox from 'atlasapprox';

      const MyCompoment = () => {

        // E.g. use a stateful variable for the result
        const [myData, setMyData] = useState({});

        useEffect(() => {
          (async () => {
             ...
             let data = await atlasapprox.organisms();

             // Set the state from the API result, which
             // will automatically trigger component rendering
             setMyData(data);
          })();
        }
      };

      export default MyComponent;

