"""Module for access to average and fraction_detected"""
import numpy as np
import pandas as pd
import h5py

from config import configuration as config
from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
)
from models.features import (
    get_feature_index,
)


def _get_sorted_feature_index(
    db_dataset,
    organism,
    features,
    measurement_type,
):
    """Get auxiliary data structures for sorted dict of features"""
    idx_series = {}
    for fea in features:
        idx = get_feature_index(organism, fea, measurement_type)
        idx_series[fea] = idx
    idx_series = pd.Series(idx_series)

    # Sort for the h5 file
    idx_sorted = idx_series.sort_values()
    data = db_dataset[:, idx_sorted.values]

    # Resort in the original order
    idx_resorted = pd.Series(np.arange(len(features)), index=idx_sorted.index)
    idx_resorted = idx_resorted.loc[features]
    data = data[:, idx_resorted.values]

    return data.T


def get_measurement(
    organism,
    organ,
    features,
    measurement_type,
    measurement_subtype,
):
    """Get measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    nfeas = len(features)
    if nfeas > 50:
        raise TooManyFeaturesError(f"Number of requested features exceeds 50: {nfeas}")

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

        # Get index for each feature, then sort for speed, then reorder
        result = _get_sorted_feature_index(
            db[measurement_type]["by_tissue"][organ]["celltype"][measurement_subtype],
            organism,
            features,
            measurement_type,
        )

    return result


def get_averages(
    organism,
    organ,
    features,
    measurement_type="gene_expression",
):
    """Get average measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    return get_measurement(
        organism,
        organ,
        features,
        measurement_type,
        "average",
    )


def get_fraction_detected(
    organism,
    organ,
    features,
    measurement_type="gene_expression",
):
    """Get fraction of detected measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    return get_measurement(
        organism,
        organ,
        features,
        measurement_type,
        "fraction",
    )
