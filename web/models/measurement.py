"""Module for access to average and fraction_detected."""
import numpy as np
import pandas as pd

from config import configuration as config
from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.exceptions import (
    OrganismNotFoundError,
    MeasurementTypeNotFoundError,
    FeatureNotFoundError,
    SomeFeaturesNotFoundError,
    TooManyFeaturesError,
    OrganCellTypeError,
)
from models.features import (
    get_feature_index,
)
from models.celltypes import get_celltype_index


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
        approx_path = get_atlas_path(organism)
        with ApproximationFile(approx_path) as db:
            if measurement_type not in db:
                raise MeasurementTypeNotFoundError(
                    f"Measurement type not found: {measurement_type}"
                )
            if "quantisation" not in db[measurement_type]:
                raise KeyError(
                    f"No 'quantisation' key found for {organism}, {measurement_type}."
                )
            quantisations[(organism, measurement_type)] = db[measurement_type][
                "quantisation"
            ][:]
    return quantisations[(organism, measurement_type)]


def _get_sorted_feature_index(
    db,
    organism,
    organ,
    features,
    measurement_type,
    measurement_subtype,
    celltype_index=None,
    use_neighborhood=False,
):
    """Get auxiliary data structures for sorted dict of features.

    Args:
        measurement_subtype (str): "average" or "fraction".
        use_neighborhood (bool): Whether to zoom into sub-cell-type detail.
    """
    if organ not in db[measurement_type]["by_tissue"]:
        raise MeasurementTypeNotFoundError(f"Organ not found: {organ}")

    db_dataset = db[measurement_type]["by_tissue"][organ]["celltype"]
    if use_neighborhood:
        db_dataset = db_dataset["neighborhood"]
    db_dataset = db_dataset[measurement_subtype]

    if features is None:
        return db_dataset[:, :]

    features_not_found = []
    idx_series = {}
    for fea in features:
        try:
            idx = get_feature_index(organism, fea.lower(), measurement_type)
        except FeatureNotFoundError as exc:
            features_not_found.append(fea)
            continue
        idx_series[fea] = idx

    if len(features_not_found):
        raise SomeFeaturesNotFoundError(
            f"Some features not found: {features}",
            features=features_not_found,
        )

    idx_series = pd.Series(idx_series)

    # Sort for the h5 file
    idx_sorted = idx_series.sort_values()
    idx_sort_back = pd.Series(np.arange(len(features)), index=idx_sorted.index)
    idx_sort_back = idx_sort_back.loc[features].values

    # Extract data from the file and resort in the original order
    if celltype_index is not None:
        data = db_dataset[celltype_index, idx_sorted.values]
    else:
        data = db_dataset[:, idx_sorted.values].T

    data = data[idx_sort_back]
    return data


def _collate_measurement_across_organs(
    db,
    organism,
    features,
    cell_type,
    measurement_type,
    measurement_subtype,
):
    from models import get_celltype_location, get_celltypes

    organs = get_celltype_location(
        organism,
        cell_type,
        measurement_type=measurement_type,
    )
    if len(organs) == 0:
        raise CellTypeNotFoundError(
            f"Cell type not found: {cell_type}.",
        )

    avgs = []
    for organ in organs:
        celltypes_organ = list(
            get_celltypes(
                organism,
                organ,
                measurement_type=measurement_type,
            )
        )

        celltype_index_dict = get_celltype_index(cell_type, celltypes_organ)
        cell_type = celltype_index_dict["celltype"]
        celltype_index = celltype_index_dict["index"]

        avg = _get_sorted_feature_index(
            db,
            organism,
            organ,
            features,
            measurement_type,
            measurement_subtype,
            celltype_index=celltype_index,
        )
        avgs.append(avg)
    avgs = np.vstack(avgs)
    return avgs


def get_measurement(
    organism,
    features,
    measurement_type,
    measurement_subtype,
    organ=None,
    cell_type=None,
    nmax=500,
    use_neighborhood=False,
):
    """Get measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    if (features is not None) and (len(features) > nmax):
        nfeas = len(features)
        raise TooManyFeaturesError(f"Number of requested features exceeds {nmax}: {nfeas}")

    if (organ is None) and (cell_type is None):
        raise OrganCellTypeError("Either organ or cell type must be specified.")
    if (organ is not None) and (cell_type is not None):
        raise OrganCellTypeError("Only one of organ or cell type can be specified.")

    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}"
            )

        # If the data is quantised, undo the quantisation to get real values
        dequantise = "quantisation" in db[measurement_type]

        if organ is not None:
            # Get index for each feature, then sort for speed, then reorder
            result = _get_sorted_feature_index(
                db,
                organism,
                organ,
                features,
                measurement_type,
                measurement_subtype,
                use_neighborhood=use_neighborhood,
            )
        elif not use_neighborhood:
            result = _collate_measurement_across_organs(
                db,
                organism,
                features,
                cell_type,
                measurement_type,
                measurement_subtype,
            )
        else:
            raise ValueError("Neighborhoods are only defined within an organ")

    # This needs to happen outside the "with" statement since retrieving the quantisation
    # might involve opening the same file again
    if dequantise:
        quantisation = _get_quantisation(organism, measurement_type)
        result = quantisation[result]

    return result


def get_averages(
    organism,
    features,
    organ=None,
    cell_type=None,
    measurement_type="gene_expression",
    use_neighborhood=False,
):
    """Get average measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    return get_measurement(
        organism,
        features,
        measurement_type,
        organ=organ,
        cell_type=cell_type,
        measurement_subtype="average",
        use_neighborhood=use_neighborhood,
    )


def get_fraction_detected(
    organism,
    features,
    organ=None,
    cell_type=None,
    measurement_type="gene_expression",
    use_neighborhood=False,
):
    """Get fraction of detected measurements by cell type

    Returns:
        numpy 2D array where each row is a **feature**
    """
    # For ATAC-Seq, fraction detected is the same as average
    if measurement_type in ("chromatin_accessibility",):
        return get_averages(
            organism,
            features,
            organ=organ,
            cell_type=cell_type,
            measurement_type=measurement_type,
            use_neighborhood=use_neighborhood,
        )

    return get_measurement(
        organism,
        features,
        organ=organ,
        cell_type=cell_type,
        measurement_type=measurement_type,
        measurement_subtype="fraction",
        use_neighborhood=use_neighborhood,
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
                [feature],
                organ=organ,
                measurement_type=measurement_type,
            )[0]
            found_once = True
        except SomeFeaturesNotFoundError:
            avg_organ = np.zeros(len(celltypes), np.float32)
        result["celltypes"].extend(celltypes)
        result["organs"].extend([organ for ct in celltypes])
        result["average"].append(avg_organ)
    result["average"] = np.concatenate(result["average"])

    if not found_once:
        raise FeatureNotFoundError(
            f"Feature not found: {feature}.",
            feature=feature,
        )

    # Find top expressors
    idx_top = result["average"].argsort()[::-1][:number]
    result["celltypes"] = [result["celltypes"][i] for i in idx_top]
    result["organs"] = [result["organs"][i] for i in idx_top]
    result["average"] = result["average"][idx_top]

    return result


def get_neighborhoods(
    organism,
    organ,
    features,
    measurement_type="gene_expression",
    include_embedding=True,
):
    """Get data (average, fraction, coordinates) for local neighborhoods in a tissue."""

    averages = get_averages(
        organism,
        features,
        organ=organ,
        measurement_type=measurement_type,
        use_neighborhood=True,
    )
    fractions = get_fraction_detected(
        organism,
        features,
        organ=organ,
        measurement_type=measurement_type,
        use_neighborhood=True, 
    )

    # Cell types (always), coords and hulls (if requested)
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if organ not in db[measurement_type]["by_tissue"]:
            raise MeasurementTypeNotFoundError(f"Organ not found: {organ}")

        db_dataset = db[measurement_type]["by_tissue"][organ]["celltype"]["neighborhood"]
        ncells_per_cluster = db_dataset["cell_count"][:]

        if include_embedding:
            coords_centroids = db_dataset["coords_centroid"][:]
            convex_hulls = []
            for i in range(len(coords_centroids)):
                hull = db_dataset['convex_hull'][str(i)][:]
                convex_hulls.append(hull)

    result = {
        "average": averages,
        "fraction": fractions,
        "ncells": ncells_per_cluster,
    }

    if include_embedding:
        result.update({
            "coords_centroid": coords_centroids,
            "convex_hull": convex_hulls,
        })

    return result
