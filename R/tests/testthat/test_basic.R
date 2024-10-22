# Use fixtures to improve the test

# Shared Variables: Store commonly used data in a fixture.
setup({
  test_organism <<- "h_sapiens"
  test_tissue <<- "lung"
  test_gene <<- "COL1A1"
  test_genes <<- c("COL1A1", "PTPRC")
  test_celltype <<- "fibroblast"
  test_number <<- 10
})

# Clean up the test environment if needed
teardown({
  rm(test_organism, test_tissue, test_genes, test_celltype, envir = .GlobalEnv)
})

# Test cases using the shared fixtures

test_that("GetOrganisms works", {
  organisms <- GetOrganisms()
  expect_false(is.null(organisms))
  expect_gte(length(organisms), 28)
})

test_that("GetOrgans works", {
  organs <- GetOrgans(test_organism)
  expect_false(is.null(organs))
  expect_true(is.array(organs))
  expect_true(length(organs) > 6)
})

test_that("GetCelltypes works", {
  celltypes <- GetCelltypes(test_organism, test_tissue)
  expect_false(is.null(celltypes))
  expect_true(is.array(celltypes))
  expect_true(length(celltypes) > 6)
})

test_that("GetAverage works", {
  result_avg <- GetAverage(test_organism, test_tissue, test_genes)
  expect_false(is.null(result_avg))
  expect_true(is.data.frame(result_avg))
  expect_equal(length(result_avg), length(test_genes))
  expect_equal(tolower(names(result_avg)), tolower(test_genes))
})

test_that("GetFractionDetected works", {
  result_frac <- GetFractionDetected(test_organism, test_tissue, test_genes)
  expect_false(is.null(result_frac))
  expect_true(is.data.frame(result_frac))
  expect_equal(length(result_frac), length(test_genes))
  expect_equal(tolower(names(result_frac)), tolower(test_genes))
})

test_that("GetMarkers works", {
  markers <- GetMarkers(test_organism, test_tissue, test_celltype, test_number)
  expect_false(is.null(markers))
  expect_true(is.array(markers))
  expect_equal(length(markers), test_number)
})

test_that("GetCelltypeLocation works", {
  locations <- GetCelltypeLocation(test_organism, test_celltype)
  expect_false(is.null(locations))
  expect_true(is.array(locations))
  expect_true(length(locations) > 1)
})

test_that("GetHighestMeasurement works", {
  highest_expressors <- GetHighestMeasurement(test_organism, test_gene, test_number)
  expect_false(is.null(highest_expressors))
  expect_true(is.data.frame(highest_expressors))
  expect_equal(nrow(highest_expressors), test_number)
})

test_that("GetSimilarFeatures works", {
  similar_features = GetSimilarFeatures(test_organism, test_tissue, test_gene, test_number, "correlation")
  expect_false(is.null(similar_features))
  expect_true(is.data.frame(similar_features))
  expect_true(nrow(similar_features) == test_number, paste("Should have", test_number, "rows"))
  expect_true(ncol(similar_features) >= 2, "Should have at least 2 columns: features and distance")
})

test_that("GetDataSources works", {
  data_sources <- GetDataSources()
  expect_false(is.null(data_sources))
  expect_type(data_sources, "list")
  expect_true(length(data_sources) >= 28)
})