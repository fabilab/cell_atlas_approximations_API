library(testthat)
library(atlasapprox)

# Use fixtures to improve the test

# Shared Variables: Store commonly used data in a fixture.
setup({
  test_organism <<- "h_sapiens"
  test_tissue <<- "Lung"
  test_genes <<- c("COL1A1", "PTPRC")
  test_celltype <<- "fibroblast"
})

# Clean up the test environment if needed
teardown({
  rm(test_organism, test_tissue, test_genes, test_celltype, envir = .GlobalEnv)
})

# Test cases using the shared fixtures

test_that("GetOrganisms works", {
  organisms <- GetOrganisms()
  expect_false(is.null(organisms))
  expect_type(organisms, "character")
  expect_gte(length(organisms), 28)
})

test_that("GetOrgans works", {
  organs <- GetOrgans(test_organism)
  expect_type(organs, "character")
  expect_true(length(organs) > 6)
})

test_that("GetCelltypes works", {
  celltypes <- GetCelltypes(test_organism, test_tissue)
  expect_type(celltypes, "character")
  expect_true(length(celltypes) > 6)
})

test_that("GetAverage works", {
  result_avg <- GetAverage(test_organism, test_tissue, test_genes)
  expect_true(is.list(result_avg))
  expect_equal(length(result_avg), length(test_genes))
  expect_equal(tolower(names(result_avg)), tolower(test_genes))
})

test_that("GetFractionDetected works", {
  result_frac <- GetFractionDetected(test_organism, test_tissue, test_genes)
  expect_true(is.list(result_frac))
  expect_equal(length(result_frac), length(test_genes))
  expect_equal(tolower(names(result_frac)), tolower(test_genes))
})

test_that("GetMarkers works", {
  markers <- GetMarkers(test_organism, test_tissue, test_celltype, 5)
  expect_type(markers, "character")
  expect_equal(length(markers), 5)
})

test_that("GetCelltypeLocation works", {
  locations <- GetCelltypeLocation(test_organism, test_celltype)
  expect_type(locations, "character")
  expect_true(length(locations) > 1)
})

# TODO:
# add unit test for getDataSource() and getHighestMeasurement() and other functions...