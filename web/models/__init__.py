"""
Data models and functions for the API
"""
import numpy as np
import h5py

from config import configuration as config
from models.exceptions import (
    OrganismNotFoundError,
    OrganNotFoundError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
    FeatureNotFoundError,
    CellTypeNotFoundError,
)
from models.features import (
    get_features,
)
from models.measurement import (
    get_averages,
    get_fraction_detected,
)


def get_organisms():
    """Get a list of organisms supported"""
    organisms = list(config["paths"]["compressed_atlas"].keys())
    organisms.sort()
    return organisms


def get_organs(
    organism,
    measurement_type="gene_expression",
):
    """Get a list of organs from one organism"""
    h5_path = config["paths"]["compressed_atlas"].get(organism, None)
    if h5_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with h5py.File(h5_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        organs = list(db[measurement_type]["by_tissue"].keys())
    organs.sort()
    return organs


def get_celltypes(organism, organ, measurement_type="gene_expression"):
    """Get list of celltypes within an organ"""
    h5_path = config["paths"]["compressed_atlas"].get(organism, None)
    if h5_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with h5py.File(h5_path) as db:
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


def get_markers(
    organism,
    organ,
    cell_type,
    number,
    measurement_type="gene_expression",
):
    """Get marker features for a specific cell type in an organ."""
    # In theory, one could use various methods to find markers
    method = "fraction"

    h5_path = config["paths"]["compressed_atlas"].get(organism, None)
    if h5_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with h5py.File(h5_path) as db:
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
