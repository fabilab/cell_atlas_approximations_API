library(testthat)
library(atlasapprox)

test_that("GetOrganisms works", {
  organisms <- GetOrganisms()
  expect_false(is.null(organisms))
  expect_type(organisms, "character")
  expect_gte(length(organisms), 28)

})

test_that("GetOrgans works", {
  organs <- GetOrgans("h_sapiens")
  expect_type(organs, "character")
  expect_true(length(organs) > 6)
})

test_that("GetCelltypes works", {
  celltypes <- GetCelltypes("h_sapiens", "Lung")
  expect_type(celltypes, "character")
  expect_true(length(celltypes) > 6)
})

test_that("GetAverage works", {
    genes <- c("COL1A1", "PTPRC")
  result_avg <- GetAverage("h_sapiens", "Lung", genes)
  expect_true(is.list(result_avg))
  expect_equal(length(result_avg), length(genes))
  expect_equal(tolower(names(result_avg)), tolower(genes))
})

test_that("GetFractionDetected works", {
    genes <- c("COL1A1", "PTPRC")
  result_frac <- GetFractionDetected("h_sapiens", "Lung", genes)
  expect_true(is.list(result_frac))
  expect_equal(length(result_frac), length(genes))
  expect_equal(tolower(names(result_frac)), tolower(genes))
})

test_that("GetMarkers works", {
  markers <- GetMarkers("h_sapiens", "Lung", "fibroblast", 5)
  expect_type(markers, "character")
  expect_equal(length(markers), 5)
})

test_that("GetCelltypeLocation works", {
  locations <- GetCelltypeLocation("h_sapiens", "fibroblast")
  expect_type(locations, "character")
  expect_true(length(locations) > 1)
})

# Gives an internal server error, need to fix this
# test_that("GetDataSources works", {
#   sources <- GetDataSources()
#   expect_type(sources, "list")
#   expect_true(length(sources) > 0)
# })