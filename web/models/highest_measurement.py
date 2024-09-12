"""Module for highest expressors"""
import numpy as np
import pandas as pd

from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    FeatureNotFoundError,
    SomeFeaturesNotFoundError,
    TooManyFeaturesError,
    OrganCellTypeError,
    OrganNotFoundError,
    NeighborhoodNotFoundError,
)
from models.features import filter_existing_features
from models.measurement import (
    get_averages,
    get_fraction_detected,
)


def get_highest_measurement(
    organism,
    feature,
    measurement_type="gene_expression",
    number=10,
    per_organ=False,
):
    """Get highest measurement cell types and averages.

    Args:
        organism: The organism of choice.
        feature: The feature (gene/peak) of choice.
        measurement_type: Whether gene_expression, chromatin_accessibility, or what else.
        number: The number of entries (cell type, organ) to return.
        per_organ: Whether to sort expression across the whole organism, or within each organ.
            If this is True, the returned list will have up to #organs x number entries.

    Returns:
        dictionary with the following key-value pairs:
           "celltypes": list of the highest measuring cell types,
           "organs": list of the corresponding organs,
           "average": numpy 1D array with the average expression
    """
    from models import get_organs, get_celltypes

    organs = get_organs(
        organism,
        measurement_type=measurement_type,
    )
    result = {
        "celltypes": [],
        "organs": [],
        "average": [],
        "fraction_detected": [],
    }
    found_once = False
    for organ in organs:
        celltypes = get_celltypes(
            organism,
            organ,
            measurement_type=measurement_type,
        )
        try:
            avg_organ = get_averages(
                organism,
                [feature],
                organ=organ,
                measurement_type=measurement_type,
            )[0]
            found_once = True
            frac_organ = get_fraction_detected(
                organism,
                [feature],
                organ=organ,
                measurement_type=measurement_type,
            )[0]
        except SomeFeaturesNotFoundError:
            # NOTE: you cannot be the highest expressor if you are zero
            continue

        if per_organ:
            # Find top expressors, per organ
            idx_top_organ = avg_organ.argsort()[::-1][:number]
            result["celltypes"].extend([celltypes[i] for i in idx_top_organ])
            result["organs"].extend([organ for i in idx_top_organ])
            result["average"].append(avg_organ[idx_top_organ])
            result["fraction_detected"].append(frac_organ[idx_top_organ])

        else:
            result["celltypes"].extend(celltypes)
            result["organs"].extend([organ for ct in celltypes])
            result["average"].append(avg_organ)
            result["fraction_detected"].append(frac_organ)

    if not found_once:
        raise FeatureNotFoundError(
            f"Feature not found: {feature}.",
            feature=feature,
        )

    result["average"] = np.concatenate(result["average"])
    result["fraction_detected"] = np.concatenate(result["fraction_detected"])

    if not per_organ:
        # Find top expressors
        idx_top = result["average"].argsort()[::-1][:number]

        # Exclude zero expressors
        idx_top = [i for i in idx_top if result["average"][i] > 0]

        result["celltypes"] = [result["celltypes"][i] for i in idx_top]
        result["organs"] = [result["organs"][i] for i in idx_top]
        result["average"] = result["average"][idx_top]
        result["fraction_detected"] = result["fraction_detected"][idx_top]

    return result


def get_highest_measurement_multiple(
    organism,
    features,
    measurement_type="gene_expression",
    number=10,
    per_organ=False,
):
    """Get highest measurement cell types and averages.

    Args:
        organism: The organism of choice.
        features: The features (genes/peaks) of choice.
        measurement_type: Whether gene_expression, chromatin_accessibility, or what else.
        number: The number of entries (cell type, organ) to return.
        per_organ: Whether to sort expression across the whole organism, or within each organ.
            If this is True, the returned list will have up to #organs x number entries.

    Returns:
        dictionary with the following key-value pairs:
           "celltypes": list of the highest measuring cell types,
           "organs": list of the corresponding organs,
           "features": list of corrected features,
           "average": numpy 2D array with the average expression
           "score": numpy 1D array of scores (highest means higher expression)
    """
    from models import get_organs, get_celltypes

    # NOTE: I tried a few versions of this, geometric average expression seems to work
    # pretty well actually... compared to a few fancier things at least
    def _score_measurements(matrix):
        mat = np.log1p(matrix)
        ## Normalse
        #mat = (matrix.T / matrix.max(axis=1)).T
        # Exponential kernel
        #mat = np.exp(mat - 1)
        return mat.mean(axis=0)

    organs = get_organs(
        organism,
        measurement_type=measurement_type,
    )
    result = {
        "celltypes": [],
        "organs": [],
        "average": [],
        "fraction_detected": [],
        "scores": [],
    }

    features_found = filter_existing_features(organism, features, measurement_type=measurement_type)
    if len(features_found) == 0:    
        raise SomeFeaturesNotFoundError(
            f"No features found: {features}.",
            features=features,
        )
    features = features_found
    result["features"] = list(features)

    for organ in organs:
        celltypes = get_celltypes(
            organism,
            organ,
            measurement_type=measurement_type,
        )

        avg_organ = get_averages(
            organism,
            features,
            organ=organ,
            measurement_type=measurement_type,
        ).T
        frac_organ = get_fraction_detected(
            organism,
            features,
            organ=organ,
            measurement_type=measurement_type,
        ).T

        if per_organ:
            # Find top expressors, per organ
            score = _score_measurements(avg_organ.T)
            result["score"].append(score)
            idx_top_organ = score.argsort()[::-1][:number]
            result["celltypes"].extend([celltypes[i] for i in idx_top_organ])
            result["organs"].extend([organ for i in idx_top_organ])
            result["average"].append(avg_organ[idx_top_organ])
            result["fraction_detected"].append(frac_organ[idx_top_organ])

        else:
            result["celltypes"].extend(celltypes)
            result["organs"].extend([organ for ct in celltypes])
            result["average"].append(avg_organ)
            result["fraction_detected"].append(frac_organ)

    result["average"] = np.vstack(result["average"]).T
    result["fraction_detected"] = np.vstack(result["fraction_detected"]).T
    if per_organ:
        result["score"] = np.concatenate(result["score"])
    else:
        # Find top expressors
        result["score"] = _score_measurements(result["average"])
        idx_top = result["score"].argsort()[::-1][:number]

        # Exclude zero expressors
        idx_top = [i for i in idx_top if result["score"][i] > 0]

        result["celltypes"] = [result["celltypes"][i] for i in idx_top]
        result["organs"] = [result["organs"][i] for i in idx_top]
        result["average"] = result["average"][:, idx_top]
        result["fraction_detected"] = result["fraction_detected"][:, idx_top]
        result["score"] = result["score"][idx_top]

    return result
