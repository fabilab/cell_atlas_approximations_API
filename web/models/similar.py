"""Similarity between features and cell types"""
import numpy as np

from models.exceptions import (
    CellTypeNotFoundError,
    SimilarityMethodError,
)
from models.features import get_features
from models.measurement import get_measurement


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
        raise SimilarityMethodError

    # Take closest features
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
    """Get similar (cell type, organ) pairs similar to the focal one."""
    from models import (
        get_organs,
        get_celltypes,
    )

    celltypes = []
    organs = []
    if method in ("correlation", "cosine"):
        fracs = []
        for organ_i in get_organs(organism):
            celltypes_i = list(get_celltypes(
                organism,
                organ_i,
            ))
            fracs_i = get_measurement(
                organism,
                organ_i,
                features=features,
                measurement_type=measurement_type,
                measurement_subtype="fraction",
            )
            if organ_i == organ:
                try:
                    idx = celltypes_i.index(celltype)
                except ValueError:
                    raise CellTypeNotFoundError
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
        for organ_i in get_organs(organism):
            celltypes_i = list(get_celltypes(
                organism,
                organ_i,
            ))
            avgs_i = get_measurement(
                organism,
                organ_i,
                features=features,
                measurement_type=measurement_type,
                measurement_subtype="average",
            )
            if organ_i == organ:
                try:
                    idx = celltypes_i.index(celltype)
                except ValueError:
                    raise CellTypeNotFoundError
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
        raise SimilarityMethodError

    # Take closest features
    idx_max = delta.argsort()[1:number+1]
    celltypes_similar = np.array(celltypes)[idx_max]
    organs_similar = np.array(organs)[idx_max]
    delta_similar = delta[idx_max]

    return {
        'celltypes': celltypes_similar,
        'organs': organs_similar,
        'distances': delta_similar,
    }
