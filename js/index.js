const api_version = "v1";
const api_uri = "https://api.atlasapprox.org/" + api_version + "/";

async function _callEndpoint(endpoint, params = {}) {
    let uri = api_uri + endpoint;

    const uriSuffix = new URLSearchParams(params).toString();
    if (uriSuffix != "")
        uri += "?" + uriSuffix;

    let response = await fetch(uri);
    let data;
    if (!response.ok) {
        data = {
            message: "Underlying REST API call failed: " + response.message,
            error: response.error,
            status: response.status,
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
// MEASUREMENT TYPE
async function measurement_types() {
  return await _callEndpoint("measurement_types");
}

// ORGANISMS
async function organisms(measurement_type = "gene_expression") {
  let params = { measurement_type };
  return await _callEndpoint("organisms", params=params);
}

// ORGANS
async function organs(organism, measurement_type = "gene_expression") {
  let params = { organism, measurement_type };
  return await _callEndpoint("organs", params=params);
}

// CELL TYPES
async function celltypes(organism, organ, measurement_type = "gene_expression") {
  let params = { organism, organ, measurement_type };
  return await _callEndpoint("celltypes", params=params);
}

// FEATURES
async function features(organism, organ, measurement_type = "gene_expression") {
  let params = { organism, organ, measurement_type };
  return await _callEndpoint("features", params=params);
}

// FEATURE SEQUENCES
async function sequences(organism, features, measurement_type = "gene_expression") {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, features, measurement_type };
  return await _callEndpoint("sequences", params=params);
};

// AVERAGE GENE EXPRESSION/CHROMATIN ACCESIBILITY
async function average(organism, features, organ = null, celltype = null, measurement_type = "gene_expression") {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, features, measurement_type };
  if (organ != null)
    params.organ = organ;
  if (celltype != null)
    params.celltype = celltype;
  return await _callEndpoint("average", params=params);
}

// FRACTION EXPRESSING/ACCESSIBLE
async function fraction_detected(organism, features, organ = null, celltype = null, measurement_type = "gene_expression") {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, features, measurement_type };
  if (organ != null)
    params.organ = organ;
  if (celltype != null)
    params.celltype = celltype;
  return await _callEndpoint("fraction_detected", params=params);
}

// MARKERS
async function markers(organism, organ, celltype, number=10, measurement_type = "gene_expression") {
  let params = { organism, organ, celltype, number, measurement_type };
  return await _callEndpoint("markers", params=params);
}

// HIGHEST MEASUREMENT
async function highest_measurement(organism, feature, number=10, measurement_type = "gene_expression") {
  let params = { organism, feature, number, measurement_type };
  return await _callEndpoint("highest_measurement", params=params);
}

// SIMILAR FEATURES
async function similar_features(organism, organ, feature, number=10, method = "correlation", measurement_type = "gene_expression") {
  let params = { organism, organ, feature, number, method, measurement_type };
  return await _callEndpoint("similar_features", params=params);
}

// SIMILAR CELLTYPES
async function similar_celltypes(organism, organ, celltype, features, number=10, method = "correlation", measurement_type = "gene_expression") {
  if (!isString(features))
    features = features.join(",");
  let params = { organism, organ, celltype, features, number, method, measurement_type };
  return await _callEndpoint("similar_celltypes", params=params);
}

// CELLTYPEXORGAN TABLE
async function celltypexorgan(organism, organs=undefined, measurement_type = "gene_expression") {
  let params = { organism, measurement_type };
  if (organs)
    params.organs = organs;
  return await _callEndpoint("celltypexorgan", params=params);
}

// CELLTYPE LOCATION
async function celltype_location(organism, celltype, measurement_type = "gene_expression") {
  let params = { organism, celltype, measurement_type };
  return await _callEndpoint("celltype_location", params=params);
}


// DATA SOURCES
async function data_sources() {
  return await _callEndpoint("data_sources");
}



///////////////////////////////////////////////////////////////////////////////

// export functions
const atlasapprox = {
    measurement_types,
    organisms,
    organs,
    celltypes,
    features,
    sequences,
    average,
    fraction_detected,
    markers,
    highest_measurement,
    similar_features,
    similar_celltypes,
    celltypexorgan,
    celltype_location,
    data_sources,
}

module.exports = atlasapprox;
