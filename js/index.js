const api_version = "v1";
const api_uri_default = "https://api.atlasapprox.org/" + api_version + "/";
let api_uri = api_uri_default + "";

const setAPIURI = (uri) => {
  api_uri = uri;
};

const resetAPIURI = () => {
  api_uri = api_uri_default;
};

async function _callEndpoint(endpoint, params = {}) {
    // Filter out "undefined" key/values from params
    Object.keys(params).forEach(key => params[key] === undefined && delete params[key])

    // Encode GET request URL
    let uri = api_uri + endpoint;
    const uriSuffix = new URLSearchParams(params).toString();
    if (uriSuffix != "")
        uri += "?" + uriSuffix;

    let response = await fetch(uri);

    // NOTE: response.body is a stream, so it can be processed only ONCE
    const data = await response.json();
    if (!response.ok) {
        throw {
            status: response.status,
            // Human readable message
            message: data.message,
            // Machine readable error structure
            error: data.error,
        }
    }
    return data;
}

let isString = value => typeof value === 'string' || value instanceof String;  

const formatFeatures = (features) => {
  if ((features === undefined) || (features === null))
    return features

  if (!isString(features))
    return features.join(",");

  return features;
};

///////////////////////////////////////////////////////////////////////////////
// Public API
///////////////////////////////////////////////////////////////////////////////
// MEASUREMENT TYPE
async function measurement_types() {
  return await _callEndpoint("measurement_types");
}

// ORGANISMS
async function organisms({ measurement_type = "gene_expression" }) {
  let params = { measurement_type };
  return await _callEndpoint("organisms", params=params);
}

// ORGANS
async function organs({ organism, measurement_type = "gene_expression" }) {
  let params = { organism, measurement_type };
  return await _callEndpoint("organs", params=params);
}

// CELL TYPES
async function celltypes({ organism, organ, measurement_type = "gene_expression", include_abundance = false }) {
  let params = { organism, organ, measurement_type, include_abundance };
  return await _callEndpoint("celltypes", params=params);
}

// FEATURES
async function features({ organism, organ, measurement_type = "gene_expression" }) {
  let params = { organism, organ, measurement_type };
  return await _callEndpoint("features", params=params);
}

// FEATURE SEQUENCES
async function sequences({ organism, features, measurement_type = "gene_expression" }) {
  features = formatFeatures(features);
  let params = { organism, features, measurement_type };
  return await _callEndpoint("sequences", params=params);
};

// AVERAGE GENE EXPRESSION/CHROMATIN ACCESIBILITY
async function average({ organism, features, organ = null, celltype = null, measurement_type = "gene_expression" }) {
  features = formatFeatures(features);
  let params = { organism, features, measurement_type };
  if (organ != null)
    params.organ = organ;
  if (celltype != null)
    params.celltype = celltype;
  return await _callEndpoint("average", params=params);
}

// FRACTION EXPRESSING/ACCESSIBLE
async function fraction_detected({ organism, features, organ = null, celltype = null, measurement_type = "gene_expression" }) {
  features = formatFeatures(features);
  let params = { organism, features, measurement_type };
  if (organ != null)
    params.organ = organ;
  if (celltype != null)
    params.celltype = celltype;
  return await _callEndpoint("fraction_detected", params=params);
}

// DOTPLOT INFORMATION: AVG + FRACTION DETECTED
async function dotplot({ organism, features, organ = null, celltype = null, measurement_type = "gene_expression" }) {
  features = formatFeatures(features);
  let params = { organism, features, measurement_type };
  if (organ != null)
    params.organ = organ;
  if (celltype != null)
    params.celltype = celltype;
  return await _callEndpoint("dotplot", params=params);
}

// NEIGHBORHOOD
async function neighborhood({ organism, organ, features = null, measurement_type = "gene_expression", include_embedding = false }) {
  features = formatFeatures(features);
  let params = { organism, organ, measurement_type, features, include_embedding };
  return await _callEndpoint("neighborhood", params=params);
};

// MARKERS
async function markers({ organism, organ, celltype, number=10, measurement_type = "gene_expression", versus = "other_celltypes", surface_only = false }) {
  let params = { organism, organ, celltype, number, measurement_type, versus, surface_only };
  return await _callEndpoint("markers", params=params);
}

// INTERACTION PARTNERS
async function interaction_partners({ organism, features, measurement_type = "gene_expression" }) {
  let params = { organism, features, measurement_type };
  return await _callEndpoint("interaction_partners", params=params);
};

// HOMOlOGS
async function homologs({ source_organism, features, target_organism }) {
  let params = { source_organism, features, target_organism };
  return await _callEndpoint("homologs", params=params);
};

// HIGHEST MEASUREMENT
async function highest_measurement({ organism, feature, number=10, measurement_type = "gene_expression", per_organ = false }) {
  let params = { organism, feature, number, measurement_type, per_organ };
  return await _callEndpoint("highest_measurement", params=params);
}

// HIGHEST MEASUREMENT MULTIPLE
async function highest_measurement_multiple({ organism, features, features_negative = "", number=10, measurement_type = "gene_expression", per_organ = false }) {
  let params = { organism, features, features_negative, number, measurement_type, per_organ };
  return await _callEndpoint("highest_measurement_multiple", params=params);
}

// SIMILAR FEATURES
async function similar_features({ organism, organ, feature, number=10, method = "correlation", measurement_type = "gene_expression" }) {
  let params = { organism, organ, feature, number, method, measurement_type };
  return await _callEndpoint("similar_features", params=params);
}

// SIMILAR CELLTYPES
async function similar_celltypes({ organism, organ, celltype, features, number=10, method = "correlation", measurement_type = "gene_expression" }) {
  features = formatFeatures(features);
  let params = { organism, organ, celltype, features, number, method, measurement_type };
  return await _callEndpoint("similar_celltypes", params=params);
}

// CELLTYPEXORGAN TABLE
async function celltypexorgan({ organism, organs=undefined, measurement_type = "gene_expression" }) {
  let params = { organism, measurement_type };
  if (organs)
    params.organs = organs;
  return await _callEndpoint("celltypexorgan", params=params);
}

// ORGANXORGANISM TABLE
async function organxorganism({ celltype, measurement_type = "gene_expression" }) {
  let params = { celltype, measurement_type };
  return await _callEndpoint("organxorganism", params=params);
}

// CELLTYPE LOCATION
async function celltype_location({ organism, celltype, measurement_type = "gene_expression" }) {
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
    dotplot,
    neighborhood,
    markers,
    interaction_partners,
    homologs,
    highest_measurement,
    highest_measurement_multiple,
    similar_features,
    similar_celltypes,
    celltypexorgan,
    organxorganism,
    celltype_location,
    data_sources,
    setAPIURI,
    resetAPIURI,
    api_version,
}

module.exports = atlasapprox;
