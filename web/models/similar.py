"""Similarity between features and cell types"""
import numpy as np

from models.exceptions import (
    CellTypeNotFoundError,
    SimilarityMethodError,
)
from models.features import (
    get_features,
    get_feature_names,
)
from models.measurement import get_measurement
from models.celltypes import get_celltype_index


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
    features_lowercase = get_features(
        organism,
        measurement_type=similar_type,
    )

    idx = (features_lowercase == feature_name.lower()).nonzero()[0][0]

    if method in ("correlation", "cosine"):
        if similar_type == measurement_type == 'gene_expression':
            measurement_subtype = 'fraction'
        else:
            measurement_subtype = 'average'
        fracs = get_measurement(
            organism,
            features=None,
            organ=organ,
            measurement_type=similar_type,
            measurement_subtype=measurement_subtype,
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
            features=None,
            organ=organ,
            measurement_type=similar_type,
            measurement_subtype="average",
        )
        if method == "log-euclidean":
            avgs = np.log(avgs + 1e-3)

        avg = avgs[:, idx]

        if method == "euclidean":
            delta = np.sqrt(((avgs.T - avg)**2).mean(axis=1))
        else:
            delta = (np.abs((avgs.T - avg))).mean(axis=1)

    else:
        raise SimilarityMethodError(
            f"Similarity method invalid: {method}",
            method=method,
        )

    # Take closest features
    features_all = get_feature_names(
        organism,
        measurement_type=measurement_type,
    )
    idx_max = delta.argsort()[1:number+1]
    similar = features_all[idx_max]
    delta_similar = delta[idx_max]

    return {
        'features': similar,
        'distances': delta_similar,
    }


def get_similar_celltypes(
    organism,
    organ,
    celltype,
    features,
    number=10,
    method="correlation",
    measurement_type="gene_expression",
):
    """Get similar (cell type, organ) pairs similar to the focal one.

    If methods "correlation" or "cosine" are chosen with only a single feature,
    "euclidean" will be used instead because those metrics are not defined if there
    is only one sample (i.e. feature).
    """
    from models import (
        get_organs,
        get_celltypes,
    )

    if (len(features) == 1) and (method in ("correlation", "cosine")):
        method = "euclidean"

    celltypes = []
    organs = []
    if method in ("correlation", "cosine"):
        fracs = []
        for organ_i in get_organs(organism, measurement_type):
            celltypes_i = list(get_celltypes(
                organism,
                organ_i,
                measurement_type,
            ))
            fracs_i = get_measurement(
                organism,
                features=features,
                organ=organ_i,
                measurement_type=measurement_type,
                measurement_subtype="fraction",
            )
            if organ_i == organ:
                celltype_index_dict = get_celltype_index(
                    celltype, celltypes_i,
                )
                celltype = celltype_index_dict['celltype']
                idx = celltype_index_dict['index']
                frac = fracs_i[:, idx]
            celltypes.extend(celltypes_i)
            organs.extend([organ_i for ct in celltypes_i])
            fracs.append(fracs_i)
        # Take the transpose to share code with similar features
        fracs = np.hstack(fracs)

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
        avgs = []
        for organ_i in get_organs(organism, measurement_type):
            celltypes_i = list(get_celltypes(
                organism,
                organ_i,
                measurement_type,
            ))
            avgs_i = get_measurement(
                organism,
                features=features,
                organ=organ_i,
                measurement_type=measurement_type,
                measurement_subtype="average",
            )
            if organ_i == organ:
                celltype_index_dict = get_celltype_index(
                    celltype, celltypes_i,
                )
                celltype = celltype_index_dict['celltype']
                idx = celltype_index_dict['index']
                avg = avgs_i[:, idx]
            celltypes.extend(celltypes_i)
            organs.extend([organ_i for ct in celltypes_i])
            avgs.append(avgs_i)
        # Take the transpose to share code with similar features
        avgs = np.hstack(avgs)

        if method == "log-euclidean":
            avgs = np.log(avgs + 1e-3)

        if method == "euclidean":
            delta = np.sqrt(((avgs.T - avg)**2).mean(axis=1))
        else:
            delta = (np.abs((avgs.T - avg))).mean(axis=1)

    else:
        raise SimilarityMethodError(
            f"Similarity method invalid: {method}",
            method=method,
        )

    # Take closest features
    idx_max = delta.argsort()[1:number+1]
    celltypes_similar = np.array(celltypes)[idx_max]
    organs_similar = np.array(organs)[idx_max]
    delta_similar = delta[idx_max]

    return {
        'celltypes': celltypes_similar,
        'organs': organs_similar,
        'distances': delta_similar,
        'method': method,
    }
