"""Preload features lazily

The main purpose of this is to enable fast browsing of the h5 file.
"""
import numpy as np
import pandas as pd

from config import configuration as config
from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.exceptions import (
    FeatureNotFoundError,
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    SimilarityMethodError,
)

# This dict has (organism, measurement_type) as keys and pandas series as
# values. For each series, the *index* is the array of features, the values
# are increasing integers to be used as an index in the h5 file
feature_series = {}


def load_features(organism, measurement_type="gene_expression"):
    """Preload list of features for an organism"""
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        features = db[measurement_type]["features"].asstr()[:]
    features_lower = pd.Index(features).str.lower()
    features_lower = pd.Series(
        np.arange(len(features)),
        index=features_lower,
    ).to_frame(name="index")
    features_lower["name"] = features
    feature_series[(organism, measurement_type)] = features_lower


def get_features(organism, measurement_type="gene_expression"):
    """Get list of all features in an organism"""
    if (organism, measurement_type) not in feature_series:
        load_features(organism, measurement_type)

    features = feature_series[(organism, measurement_type)].index.values
    return features


def get_feature_index(
    organism,
    feature_name,
    measurement_type="gene_expression",
):
    """Get the numeric index for a single feature in the h5 file"""
    if (organism, measurement_type) not in feature_series:
        load_features(organism, measurement_type)

    try:
        idx = feature_series[(organism, measurement_type)].at[feature_name, "index"]
    except KeyError as exc:
        print(f'{feature_name} not found')
        raise FeatureNotFoundError(
            f"Feature not found: {feature_name}",
            feature=feature_name,
        ) from exc

    return idx


def get_feature_names(
    organism,
    measurement_type="gene_expression",
):
    """Get the list of all features in an organism, with correct capitalization."""
    if (organism, measurement_type) not in feature_series:
        load_features(organism, measurement_type)

    features = feature_series[(organism, measurement_type)]["name"].values
    return features
