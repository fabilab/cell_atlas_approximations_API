% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/atlasapprox.R
\name{GetMarkers}
\alias{GetMarkers}
\title{GetMarkers}
\usage{
GetMarkers(organism, organ, cell_type, number)
}
\arguments{
\item{organism}{The organism you would like to query}

\item{organ}{The organ you would like to query}

\item{cell_type}{The cell type to find markers for}

\item{number}{The number of markers to return}
}
\value{
An array of markers for that cell type in that organism and organ
}
\description{
GetMarkers
}
\examples{
GetMarkers("h_sapiens", "Lung", "fibroblast", 5)
}
