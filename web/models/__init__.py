"""
Data models and functions for the API
"""
import h5py

from config import configuration as config
from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
)


def get_organisms():
    """Get a list of organisms supported"""
    organisms = config["paths"]["compressed_atlas"].keys()
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
        organs = db[measurement_type]["by_tissue"].keys()
    organs.sort()
    return organs
