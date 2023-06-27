let api_uri = "https://api.atlasapprox.org/v1/"

async function _callEndpoint(endpoint, params = {}) {
    let uri = api_uri + endpoint;

    const uriSuffix = new URLSearchParams(params).toString();
    if (uriSuffix != "")
        uri += "?" + uriSuffix;

    let response = await fetch(uri);
    let data;
    if (!response.ok) {
        data = {
            error: "API call failed",
        }
    } else {
        // NOTE: response.body is a stream, so it can be processed only ONCE
        data = await response.json();
    }

    return data;
}

///////////////////////////////////////////////////////////////////////////////
// Public API
///////////////////////////////////////////////////////////////////////////////
// ORGANISMS
async function organisms() {
  return await _callEndpoint("organisms");
}

// ORGANS
async function organs(organism) {
  let params = { organism };
  return await _callEndpoint("organs", params=params);
}

// CELL TYPES
async function celltypes(organism, organ) {
  let params = { organism, organ };
  return await _callEndpoint("celltypes", params=params);
}

///////////////////////////////////////////////////////////////////////////////

// export functions
module.exports = {
    organisms,
    organs,
    celltypes,
};
