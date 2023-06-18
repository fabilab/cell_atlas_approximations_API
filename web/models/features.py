"""Preload features lazily

The main purpose of this is to enable fast browsing of the h5 file.
"""
import numpy as np
import pandas as pd
import h5py

from config import configuration as config
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
    h5_path = config["paths"]["compressed_atlas"].get(organism, None)
    if h5_path is None:
        raise OrganismNotFoundError(f"Organism not found: {organism}")

    with h5py.File(h5_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )
        features = db[measurement_type]["features"].asstr()[:]
    features = pd.Series(np.arange(len(features)), index=features)
    feature_series[(organism, measurement_type)] = features


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
        idx = feature_series[(organism, measurement_type)].at[feature_name]
    except KeyError as exc:
        raise FeatureNotFoundError(f"Feature not found: {feature_name}") from exc

    return idx


def get_similar_features(
    organism,
    organ,
    feature_name,
    number=10,
    method="correlation",
    measurement_type="gene_expression",
    similar_type="gene_expression",
):
    """Get features similar to the focal one."""
    from models.measurement import get_measurement

    features_all = get_features(
        organism,
        measurement_type=similar_type,
    )
    idx = (features_all == feature_name).nonzero()[0][0]

    if method in ("correlation", "cosine"):
        fracs = get_measurement(
            organism,
            organ,
            features=None,
            measurement_type=similar_type,
            measurement_subtype="fraction",
        )
        frac = fracs[:, idx]

        if method == "correlation":
            # Center around 0
            dm = fracs - fracs.mean(axis=0)
            db = frac - frac.mean()
        else:
            dm = fracs
            db = frac

        # Compute covariance and then correlation
        num = dm.T @ db
        den = np.sqrt((dm**2).sum(axis=0) * (db @ db))
        corr = num / (den + 1e-9)
        delta = 1 - corr

    elif method in ("euclidean", "manhattan", "log-euclidean"):
        avgs = get_measurement(
            organism,
            organ,
            features=None,
            measurement_type=similar_type,
            measurement_subtype="fraction",
        )
        if method == "log-euclidean":
            avgs = np.log(avgs + 1e-3)

        avg = avgs[:, idx]

        if method == "euclidean":
            delta = np.sqrt(((avgs.T - avg)**2).mean(axis=1))
        else:
            delta = (np.abs((avgs.T - avg))).mean(axis=1)

    else:
        raise SimilarityMethodError

    # Take closest features
    idx_max = delta.argsort()[1:number+1]
    similar = features_all[idx_max]
    delta_similar = delta[idx_max]

    return {
        'features': similar,
        'distances': delta_similar,
    }
