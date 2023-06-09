"""Module for access to average and fraction_detected"""
import numpy as np
import pandas as pd

from config import configuration as config
from models.utils import ApproximationFile
from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    FeatureNotFoundError,
    TooManyFeaturesError,
)
from models.features import (
    get_feature_index,
)


quantisations = {}


def _get_quantisation(organism, measurement_type):
    """Lazy cacher of data quantisations.

    NOTE: Data quantisation is sometimes needed to reduce file size. Even a simple 8-bit
    logarithmic quantisation of e.g. chromatin accessibility saves ~70% of space compared
    to 32-bit floats. The runtime overhead to undo the quantisation is minimal, even less
    if the quantisation vector (i.e. 256 float32 numbers) is lazily loaded into RAM via
    this function.
    """
    if (organism, measurement_type) not in quantisations:
        approx_path = config["paths"]["compressed_atlas"].get(organism, None)
        if approx_path is None:
            raise OrganismNotFoundError(f"Organism not found: {organism}")

        with ApproximationFile(approx_path) as db:
            if measurement_type not in db:
                raise MeasurementTypeNotFoundError(
                    f"Measurement type not found: {measurement_type}"
                )
            if "quantisation" not in db[measurement_type]:
                raise KeyError(
                    f"No 'quantisation' key found for {organism}, {measurement_type}."
                )
            quantisations[(organism, measurement_type)] = db[measurement_type]['quantisation'][:]
    return quantisations[(organism, measurement_type)]


def _get_sorted_feature_index(
    db_dataset,
    organism,
    features,
    measurement_type,
):
    """Get auxiliary data structures for sorted dict of features"""
    if features is None:
        return db_dataset[:, :]

    idx_series = {}
    for fea in features:
        idx = get_feature_index(organism, fea, measurement_type)
        idx_series[fea] = idx
    idx_series = pd.Series(idx_series)

    # Sort for the h5 file
    idx_sorted = idx_series.sort_values()

    # Extract data from the file
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
    nmax=50,
):
    """Get measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    if (features is not None) and (len(features) > nmax):
        nfeas = len(features)
        raise TooManyFeaturesError(
                f"Number of requested features exceeds 50: {nfeas}")

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

        # Get index for each feature, then sort for speed, then reorder
        db_dataset = db[measurement_type]["by_tissue"][organ]["celltype"][measurement_subtype]
        result = _get_sorted_feature_index(
            db_dataset,
            organism,
            features,
            measurement_type,
        )

        # If the data is quantised, undo the quantisation to get real values
        dequantise = 'quantisation' in db[measurement_type]

    # This needs to happen outside the "with" statement since retrieving the quantisation
    # might involve opening the same file again
    if dequantise:
        quantisation = _get_quantisation(organism, measurement_type)
        result = quantisation[result]

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
    # For ATAC-Seq, fraction detected is the same as average
    if measurement_type in ('chromatin_accessibility',):
        return get_averages(
            organism,
            organ,
            features,
            measurement_type,
        )

    return get_measurement(
        organism,
        organ,
        features,
        measurement_type,
        "fraction",
    )


def get_highest_measurement(
    organism,
    feature,
    measurement_type="gene_expression",
    number=10,
):
    """Get highest measurement cell types and averages.

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
                organ,
                [feature],
                measurement_type=measurement_type,
            )[0]
            found_once = True
        except FeatureNotFoundError:
            avg_organ = np.zeros(len(celltypes), np.float32)
        result["celltypes"].extend(celltypes)
        result["organs"].extend([organ for ct in celltypes])
        result["average"].append(avg_organ)
    result["average"] = np.concatenate(result["average"])

    if not found_once:
        raise FeatureNotFoundError(f"Feature not found: {feature}.")

    # Find top expressors
    idx_top = result["average"].argsort()[::-1][:number]
    result["celltypes"] = [result["celltypes"][i] for i in idx_top]
    result["organs"] = [result["organs"][i] for i in idx_top]
    result["average"] = result["average"][idx_top]

    return result
