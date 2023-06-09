"""
Data models and functions for the API
"""
from collections import Counter
import numpy as np
import pandas as pd

from config import configuration as config
from models.utils import ApproximationFile
from models.exceptions import (
    OrganismNotFoundError,
    OrganNotFoundError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
    FeatureNotFoundError,
    CellTypeNotFoundError,
    SimilarityMethodError,
)
from models.features import (
    get_features,
)
from models.measurement import (
    get_averages,
    get_fraction_detected,
    get_highest_measurement,
)
from models.similar import (
    get_similar_features,
    get_similar_celltypes,
)


def get_organisms(
    measurement_type="gene_expression",
):
    """Get a list of organisms supported, for a particular measurement type."""
    organisms = []
    for organism, approx_path in config["paths"]["compressed_atlas"].items():
        with ApproximationFile(approx_path) as db:
            if measurement_type in db:
                organisms.append(organism)
    organisms.sort()
    return organisms


def get_organs(
    organism,
    measurement_type="gene_expression",
):
    """Get a list of organs from one organism"""
    approx_path = config["paths"]["compressed_atlas"].get(organism, None)
    if approx_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        organs = list(db[measurement_type]["by_tissue"].keys())
    organs.sort()
    return organs


def get_celltypes(
    organism,
    organ,
    measurement_type="gene_expression",
):
    """Get list of celltypes within an organ"""
    approx_path = config["paths"]["compressed_atlas"].get(organism, None)
    if approx_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        if organ not in db[measurement_type]["by_tissue"]:
            raise OrganNotFoundError(f"Organ not found: {organ}")

        celltypes = db[measurement_type]["by_tissue"][organ]["celltype"][
            "index"
        ].asstr()[:]
    return celltypes


def get_celltype_abundance(
    organism,
    organ,
    measurement_type="gene_expression",
):
    """Get number of cells for each type within an organ"""
    approx_path = config["paths"]["compressed_atlas"].get(organism, None)
    if approx_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        if organ not in db[measurement_type]["by_tissue"]:
            raise OrganNotFoundError(f"Organ not found: {organ}")

        celltypes = db[measurement_type]["by_tissue"][organ]["celltype"][
            "index"
        ].asstr()[:]
        cell_numbers = db[measurement_type]["by_tissue"][organ]["celltype"][
            "cell_count"
        ][:]
    return pd.Series(cell_numbers, index=celltypes)


def get_celltypexorgan(
    organism,
    organs=None,
    measurement_type="gene_expression",
    boolean=False,
):
    """Get a presence/absence matrix for cell types in organs"""
    # Get organs
    if organs is None:
        organs = list(get_organs(
            organism=organism, measurement_type=measurement_type,
        ))

    # Get celltypes
    organs_celltypes = Counter()
    for organ in organs:
        celltypes_organ = get_celltype_abundance(
            organism=organism, organ=organ, measurement_type=measurement_type,
        )
        for celltype, abundance in celltypes_organ.items():
            organs_celltypes[(organ, celltype)] = abundance

    dtype = bool if boolean else int
    data = pd.Series(organs_celltypes).unstack(0, fill_value=0).astype(dtype)

    # Sort from the cell types with the highest abundance
    # NOTE: a double sort by this and secondarily by organ name might be
    # even better perhaps
    data = data.loc[(data != 0).sum(axis=1).sort_values(ascending=False).index]

    return data


def get_markers(
    organism,
    organ,
    cell_type,
    number,
    measurement_type="gene_expression",
):
    """Get marker features for a specific cell type in an organ."""
    # In theory, one could use various methods to find markers
    if measurement_type == "gene_expression":
        method = "fraction"
    # For ATAC-Seq, average and fraction are the same thing
    else:
        method = "average"

    approx_path = config["paths"]["compressed_atlas"].get(organism, None)
    if approx_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        if organ not in db[measurement_type]["by_tissue"]:
            raise MeasurementTypeNotFoundError(f"Organ not found: {organ}")

        # H5 group to use
        sub_db = db[measurement_type]["by_tissue"][organ]["celltype"]

        # Cell types and indices
        cell_types = sub_db["index"].asstr()[:]
        ncell_types = len(cell_types)

        if cell_type not in cell_types:
            raise CellTypeNotFoundError(f"Cell type not found: {cell_type}")

        # Matrix of measurements (rows are cell types)
        mat = sub_db[method]

        # Index cell types
        idx = list(cell_types).index(cell_type)
        idx_other = [i for i in range(ncell_types) if i != idx]
        vector = mat[idx]
        mat_other = mat[idx_other]

    # Compute difference (vector - other)
    mat_other -= vector
    mat_other *= -1

    # Find closest cell type for each feature
    closest_value = mat_other.min(axis=0)

    # Take top features
    idx_markers = np.argsort(closest_value)[-number:][::-1]

    # Sometimes there are just not enough markers, so make sure the difference
    # is positive
    idx_markers = idx_markers[closest_value[idx_markers] > 0]

    # Get the feature names
    features = get_features(
        organism,
        measurement_type,
    )[idx_markers]

    return features
