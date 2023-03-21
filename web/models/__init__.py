"""
Data models and functions for the API
"""
import numpy as np
import h5py

from config import configuration as config
from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
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

        celltypes = db[measurement_type]["by_tissue"][organ]["celltype"][
            "index"
        ].asstr()[:]
    return celltypes
