const api_uri = "https://api.atlasapprox.org/v1/"

async function _callEndpoint(endpoint, params = {}) {
    let uri = api_uri + endpoint;

    const uriSuffix = new URLSearchParams(params).toString();
    if (uriSuffix != "")
        uri += "?" + uriSuffix;

    let response = await fetch(uri);
    let data;
    if (!response.ok) {
        data = {
            error: "API call failed: " + response.message,
        }
    } else {
        // NOTE: response.body is a stream, so it can be processed only ONCE
        data = await response.json();
    }

    return data;
}

let isString = value => typeof value === 'string' || value instanceof String;  

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

// AVERAGE GENE EXPRESSION
async function average(organism, organ, features) {
  features = features.join(",");
  let params = { organism, organ, features };
  return await _callEndpoint("average", params=params);
}

// FRACTION EXPRESSING
async function fraction_detected(organism, organ, features) {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, organ, features };
  return await _callEndpoint("fraction_detected", params=params);
}

// MARKERS
async function markers(organism, organ, celltype, number=10) {
  let params = { organism, organ, celltype, number };
  return await _callEndpoint("markers", params=params);
}

// HIGHEST MEASUREMENT
async function highest_measurement(organism, feature, number=10) {
  let params = { organism, feature, number };
  return await _callEndpoint("highest_measurement", params=params);
}

// SIMILAR FEATURES
async function similar_features(organism, organ, feature, number=10, method='correlation') {
  let params = { organism, organ, feature, number, method };
  return await _callEndpoint("similar_features", params=params);
}

// SIMILAR CELLTYPES
async function similar_celltypes(organism, organ, celltype, features, number=10, method='correlation') {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, organ, celltype, features, number, method };
  return await _callEndpoint("similar_features", params=params);
}

// CELLTYPEXORGAN TABLE
async function celltypexorgan(organism, organs=undefined) {
  let params = { organism };
  if (organs)
    params.organs = organs;
  return await _callEndpoint("celltypexorgan", params=params);
}

// DATA SOURCES
async function data_sources() {
  return await _callEndpoint("data_sources");
}



///////////////////////////////////////////////////////////////////////////////

// export functions
const atlasapprox = {
    organisms,
    organs,
    celltypes,
    average,
    fraction_detected,
    markers,
    highest_measurement,
    similar_features,
    similar_celltypes,
    celltypexorgan,
    data_sources,
}

module.exports = atlasapprox;
