#' api_version
api_version <- 'v1'

baseurl <- Sys.getenv("ATLASAPPROX_BASEURL")
if (baseurl == "") {
    baseurl <- paste('http://api.atlasapprox.org/', api_version, '/', sep="")
}


###########################
# INTERNALS
###########################
# A new environment storing cache info (e.g. list of organisms)
# Thse act a little like Python dictionaries
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
#' @return An array of available organisms
#' @export
#'
#' @examples GetOrganisms()
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
#' @param organism The organism you would like to query
#'
#' @return An array of available organs from that organism
#' @export
#'
#' @examples GetOrgans("h_sapiens")
GetOrgans <- function(organism) {
    cacheKey <- paste('organs', organism, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(organism = organism)
        root_uri <- paste(baseurl, 'organs', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response))
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
#' @param organism The organism you would like to query
#'
#' @return An array of available features (genes) from that organism
#' @export
#'
#' @examples GetFeatures("h_sapiens")
GetFeatures <- function(organism) {
    cacheKey <- paste('features', organism, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(organism = organism)
        root_uri <- paste(baseurl, 'features', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response))
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
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#'
#' @return An array of available cell types from that organism and organ
#' @export
#'
#' @examples GetCelltypes("h_sapiens", "Lung")
GetCelltypes <- function(organism, organ) {
    cacheKey <- paste('celltypes', organism, organ, sep = ":")
    if (!.HasCache(cacheKey)) {
        params <- list(organism = organism, organ = organ)
        root_uri <- paste(baseurl, 'celltypes', sep="")
        uri <- .GetParams(root_uri, params)
        response <- httr::GET(uri)
        if (response$status != 200) {
            stop(paste("Bad request: server returned", response))
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
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param features An array/list of features (e.g. genes) you would like to query
#'
#' @return A data.frame of average gene expression by cell type in that organism and organ
#' @export
#'
#' @examples GetAverage("h_sapiens", "Lung", c("COL1A1", "PTPRC"))
GetAverage <- function(organism, organ, features) {
    features_string <- paste(features, collapse = ",")
    params <- list(organism = organism, organ = organ, features = features_string)
    root_uri <- paste(baseurl, 'average', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
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
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param features An array/list of features (e.g. genes) you would like to query
#'
#' @return A data.frame of fraction of expressing cells by cell type in that organism and organ
#' @export
#'
#' @examples GetFractionDetected("h_sapiens", "Lung", c("COL1A1", "PTPRC"))
GetFractionDetected <- function(organism, organ, features) {
    features_string <- paste(features, collapse = ",")
    params <- list(organism = organism, organ = organ, features = features_string)
    root_uri <- paste(baseurl, 'fraction_detected', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
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
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param cell_type The cell type to find markers for
#' @param number The number of markers to return
#'
#' @return An array of markers for that cell type in that organism and organ
#' @export
#'
#' @examples GetMarkers("h_sapiens", "Lung", "fibroblast", 5)
GetMarkers <- function(organism, organ, cell_type, number) {
    params <- list(organism = organism,
   		organ = organ,
   		celltype = cell_type,
   		number = number)
    root_uri <- paste(baseurl, 'markers', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
    }
    result <- array(unlist(httr::content(response)$markers))
    return(result)
}


#' GetHighestMeasurement
#'
#' @param organism The organism you would like to query
#' @param feature The feature to check (e.g. gene)
#' @param number The number of cell types to return
#'
#' @return An array of cell types, organs, and averages for the
#'         cell types with the highest measurement for that feature
#' @export
#'
#' @examples GetHighestMeasurement("h_sapiens", "PTPRC", 5)
GetHighestMeasurement <- function(organism, feature, number) {
    params <- list(organism = organism,
   		feature = feature,
   		number = number)
    root_uri <- paste(baseurl, 'highest_measurement', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
    }
    cell_types <- array(unlist(httr::content(response)$celltypes))
    organs <- array(unlist(httr::content(response)$organs))
    average <- array(unlist(httr::content(response)$average))

    print(cell_types)
    print(organs)
    print(average)

    # Make data frame with all three arrays
    df <- data.frame(cell_types, organs, average)
    colnames(df) <- c("Cell type", "Organ", "Average")

    return(df)
}


#' GetSimilarFeatures
#'
#' @param organism The organism you would like to query
#' @param organ The organ you would like to query
#' @param feature The feature to check (e.g. gene)
#' @param number The number of similar features to return
#' @param method The method used for the distance computation.
#'        Available methods are: "correlation" (default), "cosine",
#'        "euclidean", "manhattan", "log-euclidean".
#'
#' @return An array of features and their distance from the focal feature
#'         according to the method chosen.
#' @export
#'
#' @examples GetSimilarFeatures("h_sapiens", "Lung", "PTPRC", 5, "correlation")
GetHighestMeasurement <- function(organism, organ, feature, number, method) {
    params <- list(organism = organism,
                organ = organ,
		feature = feature,
		number = number,
                method = method)
    root_uri <- paste(baseurl, 'similar-features', sep="")
    uri <- .GetParams(root_uri, params)
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
    }
    similar_features <- array(unlist(httr::content(response)$similar_features))
    distances <- array(unlist(httr::content(response)$distances))

    # Make data frame
    df <- data.frame(similar_features, distances)
    colnames(df) <- c("Features", "distances")

    return(df)
}


#' GetDataSources
#'
#' @return The cell atlases used as data sources for the approximations
#' @export
#'
#' @examples GetDataSources()
GetDataSources <- function() {
    uri <- paste(baseurl, 'data_sources', sep="")
    response <- httr::GET(uri)
    if (response$status != 200) {
        stop(paste("Bad request: server returned", response))
    }
    result <- httr::content(response)$data_sources
    return(result)
}
