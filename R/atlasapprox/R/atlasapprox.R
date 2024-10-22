#' api_version
api_version <- 'v1'

baseurl <- Sys.getenv("ATLASAPPROX_BASEURL")
if (baseurl == "") {
    baseurl <- paste('http://api.atlasapprox.org/', api_version, '/', sep="")
}

#' @importFrom utils URLencode
NULL

###########################
# INTERNALS
###########################
# A new environment storing cache info (e.g. list of organisms)
# These act a little like Python dictionaries
.atlas_approx_cache <- new.env()


# Utility functions to manipulate the cache
.EmptyCache <- function() {
    rm(list = ls(envir = .atlas_approx_cache), envir = .atlas_approx_cache)
}


.PrintCache <- function() {
    print(ls(envir = .atlas_approx_cache))
}


.HasCache <- function(key) {
    return(exists(key, envir = .atlas_approx_cache))
}


.GetCache <- function(key) {
    return(get(key, envir = .atlas_approx_cache))
}


.SetCache <- function(key, value) {
    assign(key, value, envir = .atlas_approx_cache)
}


# We have to code our own URL parameter expander... sigh
.GetParams <- function(root_uri, params) {
    uri <- paste(root_uri, "?", sep = "")
    for (i in seq_along(params)) {
        namei <- URLencode(names(params)[i])
        vali <- URLencode(toString(params[[i]]))
        uri <- paste(uri, "&", namei, "=", vali, sep = "")
    }
    return(uri)
}

###########################
# EXPORTED FUNCTIONS
###########################

#' GetOrganisms
#'
#' Get a list of organisms available for querying in the atlasapprox api.
#' 
#' @return An array of available organisms
#' @export
#'
#' @examples
#' GetOrganisms()
GetOrganisms <- function() {
    if (!.HasCache('organisms')) {
        uri <- paste(baseurl, 'organisms', sep="")
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response$status))
        }
        result <- array(unlist(httr::content(response)$organisms))
	.SetCache('organisms', result)
    } else {
        result <- .GetCache('organisms')
    }
    return(result)
}


#' GetOrgans
#'
#' Get all available organs for an organism

#' @param organism The organism you would like to query
#'
#' @return An array of available organs from that organism
#' @export
#'
#' @examples
#' GetOrgans("h_sapiens")
GetOrgans <- function(organism) {
    cacheKey <- paste('organs', organism, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(organism = organism)
        root_uri <- paste(baseurl, 'organs', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response$status))
        }
        result <- array(unlist(httr::content(response)$organs))
	.SetCache(cacheKey, result)
    } else {
        result <- .GetCache(cacheKey)
    }
    return(result)
}


#' GetFeatures
#'
#' Get a list of available features (typically genes) for a specified organism.
#' 
#' @param organism The organism you would like to query
#'
#' @return An array of available features (genes) from that organism
#' @export
#'
#' @examples
#' GetFeatures("h_sapiens")
GetFeatures <- function(organism) {
    cacheKey <- paste('features', organism, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(organism = organism)
        root_uri <- paste(baseurl, 'features', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response$status))
        }
        result <- array(unlist(httr::content(response)$features))
	.SetCache(cacheKey, result)
    } else {
        result <- .GetCache(cacheKey)
    }
    return(result)
}


#' GetCelltypes
#'
#' Get all available cell types for a specified organism and organ.
#' 
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#'
#' @return An array of available cell types from that organism and organ
#' @export
#'
#' @examples
#' GetCelltypes("h_sapiens", "Lung")
GetCelltypes <- function(organism, organ) {
    cacheKey <- paste('celltypes', organism, organ, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(
            organism = organism, 
            organ = organ
        )
        root_uri <- paste(baseurl, 'celltypes', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response$status))
        }
        result <- array(unlist(httr::content(response)$celltypes))
	.SetCache(cacheKey, result)
    } else {
        result <- .GetCache(cacheKey)
    }
    return(result)
}


#' GetAverage
#'
#' Get the average gene expression for specified features across cell types in a given organism and organ.
#'
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param features The features (genes) you would like to query
#'
#' @return A data.frame of average gene expression by cell type in that organism and organ
#' @export
#'
#' @examples
#' GetAverage("h_sapiens", "Lung", c("COL1A1", "PTPRC"))
GetAverage <- function(organism, organ, features) {
    features_string <- paste(features, collapse = ",")
    params <- list(
        organism = organism, 
        organ = organ, 
        features = features_string
    )
    root_uri <- paste(baseurl, 'average', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    res <- (httr::content(response)$average)
    nrows <- length(res)
    ncols <- length(res[[1]])
    result <- data.frame(array(unlist(res), dim=c(ncols,nrows)))
    names(result) <- httr::content(response)$features

    celltypes <- GetCelltypes(organism, organ)
    row.names(result) <- celltypes

    return(result)
}


#' GetFractionDetected
#'
#' Get the fraction of cells expressing specified features across cell types in a given organism and organ.
#'
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param features The features (genes) you would like to query
#'
#' @return A data.frame of fraction of expressing cells by cell type in that organism and organ
#' @export
#'
#' @examples
#' GetFractionDetected("h_sapiens", "Lung", c("COL1A1", "PTPRC"))
GetFractionDetected <- function(organism, organ, features) {
    features_string <- paste(features, collapse = ",")
    params <- list(
        organism = organism, 
        organ = organ, 
        features = features_string
    )
    root_uri <- paste(baseurl, 'fraction_detected', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    res <- (httr::content(response)$fraction_detected)
    nrows <- length(res)
    ncols <- length(res[[1]])
    result <- data.frame(array(unlist(res), dim=c(ncols,nrows)))
    names(result) <- httr::content(response)$features

    celltypes <- GetCelltypes(organism, organ)
    row.names(result) <- celltypes

    return(result)
}

#' GetMarkers
#'
#' Get marker genes for a specified cell type in a given organism and organ.
#'
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param cell_type The cell type you would like to query
#' @param number The number of markers you would like to get
#'
#' @return An array of markers for that cell type in that organism and organ
#' @export
#'
#' @examples
#' GetMarkers("h_sapiens", "Lung", "fibroblast", 5)
GetMarkers <- function(organism, organ, cell_type, number) {
    params <- list(
        organism = organism, 
        organ = organ,
   		celltype = cell_type,
   		number = number
    )
    root_uri <- paste(baseurl, 'markers', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    result <- array(unlist(httr::content(response)$markers))
    return(result)
}


#' GetCelltypeLocation
#'
#' Get the organs where a specified cell type is found in a given organism.
#'
#' @param organism The organism you would like to query
#' @param cell_type The cell type you would like to query
#'
#' @return An array of organs in which that cell type is found
#' @export
#'
#' @examples
#' GetCelltypeLocation("h_sapiens", "fibroblast")
GetCelltypeLocation <- function(organism, cell_type) {
    params <- list(
        organism = organism, 
        celltype = cell_type
    )
    root_uri <- paste(baseurl, 'celltype_location', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    result <- array(unlist(httr::content(response)$organs))
    return(result)
}


#' GetHighestMeasurement
#'
#' Get the cell types with the highest expression of a specified feature in a given organism.
#'
#' @param organism The organism you would like to query
#' @param feature The feature you would like to query
#' @param number The number of highest expressors you would like to get
#'
#' @return A dataframe of cell types, organs, and averages for the
#'         cell types with the highest measurement for that feature
#' @export
#'
#' @examples
#' GetHighestMeasurement("h_sapiens", "PTPRC", 5)
GetHighestMeasurement <- function(organism, feature, number) {
    params <- list(
        organism = organism,
   		feature = feature,
   		number = number
    )
    root_uri <- paste(baseurl, 'highest_measurement', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    cell_types <- array(unlist(httr::content(response)$celltypes))
    organs <- array(unlist(httr::content(response)$organs))
    average <- array(unlist(httr::content(response)$average))

    # Make data frame with all three arrays
    df <- data.frame(cell_types, organs, average)
    colnames(df) <- c("Cell type", "Organ", "Average")

    return(df)
}


#' GetSimilarFeatures
#' 
#' Get features with similar expression patterns to a specified feature in a given organism and organ.
#'
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param feature The feature to find similarities for
#' @param number The number of similar features you would like to get.
#' @param method The method used to compute similarity between features. 
#'             The following methods are available:
#'             - correlation (default): Pearson correlation of the fraction_detected
#'             - cosine: Cosine similarity/distance of the fraction_detected
#'             - euclidean: Euclidean distance of average measurement (e.g. expression)
#'             - manhattan: Taxicab/Manhattan/L1 distance of average measurement
#'             - log-euclidean: Log the average measurement with a pseudocount
#'               of 0.001, then compute euclidean distance. This tends to
#'               highlight sparsely measured features
#'
#' @return A dataframe of similar features and their distances from the focal feature according to the method chosen
#' @export
#'
#' @examples
#' GetSimilarFeatures("h_sapiens", "lung", "PTPRC", 5, "correlation")
GetSimilarFeatures <- function(organism, organ, feature, number, method) {
    params <- list(
        organism = organism,
        organ = organ,
		feature = feature,
		number = number,
        method = method
    )
    root_uri <- paste(baseurl, 'similar_features', sep="")
    uri <- .GetParams(root_uri, params)

    response <- httr::GET(uri)

    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    
    similar_features <- array(unlist(httr::content(response)$similar_features))
    distances <- array(unlist(httr::content(response)$distances))

    # Make data frame
    df <- data.frame(similar_features, distances)
    colnames(df) <- c("Similar features", "distances")

    return(df)
}

#' GetDataSources
#'
#' Get information about the cell atlases used as data sources for the approximations.
#'
#' @return A list containing information about the cell atlases used as data sources
#' @export
#'
#' @examples
#' GetDataSources()
GetDataSources <- function() {
    uri <- paste(baseurl, 'data_sources', sep="")
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response$status))
    }
    result <- httr::content(response)
    return(result)
}