"""
Data models and functions for the API
"""

from collections import Counter
import os
import pathlib
import numpy as np
import pandas as pd

from config import configuration as config
from models.organisms import get_organisms
from models.paths import (
    get_atlas_path,
    get_interactions_path,
)
from models.utils import ApproximationFile
from models.exceptions import (
    OrganismNotFoundError,
    OrganNotFoundError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
    FeatureNotFoundError,
    SomeFeaturesNotFoundError,
    FeatureSequencesNotFoundError,
    CellTypeNotFoundError,
    SimilarityMethodError,
    NeighborhoodNotFoundError,
    FeaturesNotPairedError,
)
from models.features import (
    get_features,
    get_feature_index,
    get_feature_indices,
    get_feature_names,
)
from models.sequences import (
    get_feature_sequences,
)
from models.measurement import (
    get_averages,
    get_fraction_detected,
    get_neighborhoods,
)
from models.highest_measurement import (
    get_highest_measurement,
    get_highest_measurement_multiple,
)
from models.similar import (
    get_similar_features,
    get_similar_celltypes,
)
from models.celltypes import (
    get_celltype_index,
)
from models.quantisation import (
    get_quantisation,
)
from models.markers import (
    get_markers_vs_other_celltypes,
    get_markers_vs_other_tissues,
)
from models.interactions import (
    get_interaction_partners,
)
from models.homology import (
    get_homologs,
    get_homology_distances,
)
from models.surface import (
    get_surface_genes,
)


def get_data_sources():
    """Get a dictionary of all data sources."""
    data_sources = {}
    organisms = get_organisms()
    for organism in organisms:
        approx_path = get_atlas_path(organism)
        with ApproximationFile(approx_path) as db:
            data_source = {}
            for measurement_type in db["measurements"]:
                data_source[measurement_type] = db["measurements"][
                    measurement_type
                ].attrs["source"]
            if len(data_source) == 1:
                data_source = data_source[measurement_type]
            else:
                tmp_map = {
                    "gene_expression": "RNA",
                    "chromatin_accessibility": "ATAC",
                }
                print(data_source)
                data_source = ", ".join(
                    [
                        tmp_map[mt] + ": " + val.rstrip(".")
                        for mt, val in data_source.items()
                    ]
                )
        data_sources[organism] = data_source
    return data_sources


def get_full_atlas_files():
    """Get a hyperlink to a public cloud folder containing full cell atlases."""
    return "https://unsw-my.sharepoint.com/:f:/g/personal/z3528476_ad_unsw_edu_au/EoTk9jUCHuNCtELqBVpWZqQBDRe06EVomVU8XgteN4OTjw"


def get_organs(
    organism,
    measurement_type="gene_expression",
):
    """Get a list of organs from one organism"""
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db["measurements"]:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )
        gby = db["measurements"][measurement_type]["grouped_by"]["tissue->celltype"]
        organs = list(gby["values"]["tissue"].asstr()[:])
    organs.sort()
    return organs


def get_celltypes(
    organism,
    organ,
    measurement_type="gene_expression",
):
    """Get list of celltypes within an organ"""
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db["measurements"]:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )
        gby = db["measurements"][measurement_type]["grouped_by"]["tissue->celltype"]

        if (organ is None) or (organ == "all"):
            return gby["values"]["celltype"].asstr()[:]

        if organ not in gby["values"]["tissue"].asstr()[:]:
            raise OrganNotFoundError(
                f"Organ not found: {organ}",
                organ=organ,
            )
        data = db["measurements"][measurement_type]["data"]["tissue->celltype"][organ]
        celltypes = data["obs_names"].asstr()[:]
    return celltypes


def get_celltype_location(
    organism,
    cell_type,
    measurement_type="gene_expression",
):
    """Get a list of organs where this cell type is found."""
    organs = get_organs(organism, measurement_type=measurement_type)
    organs_found = []
    for organ in organs:
        cell_types_organ = get_celltypes(
            organism,
            organ,
            measurement_type=measurement_type,
        )
        if cell_type in cell_types_organ:
            organs_found.append(organ)
    return np.array(organs_found)


def get_celltype_abundance(
    organism,
    organ,
    measurement_type="gene_expression",
):
    """Get number of cells for each type within an organ"""
    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db["measurements"]:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )

        gby = db["measurements"][measurement_type]["grouped_by"]["tissue->celltype"]
        if organ not in gby["values"]["tissue"].asstr()[:]:
            raise OrganNotFoundError(
                f"Organ not found: {organ}",
                organ=organ,
            )

        data = db["measurements"][measurement_type]["data"]["tissue->celltype"][organ]
        celltypes = data["obs_names"].asstr()[:]
        cell_numbers = data["cell_count"][:]
    return pd.Series(cell_numbers, index=celltypes)


def get_celltypexorgan(
    organism,
    organs=None,
    measurement_type="gene_expression",
    boolean=False,
):
    """Get a presence/absence matrix for cell types in organs"""
    # Get organs
    if organs is None:
        organs = list(
            get_organs(
                organism=organism,
                measurement_type=measurement_type,
            )
        )

    # Get celltypes
    organs_celltypes = Counter()
    for organ in organs:
        celltypes_organ = get_celltype_abundance(
            organism=organism,
            organ=organ,
            measurement_type=measurement_type,
        )
        for celltype, abundance in celltypes_organ.items():
            organs_celltypes[(organ, celltype)] = abundance

    dtype = bool if boolean else int
    # Cell types are rows, organs are columns
    data = pd.Series(organs_celltypes).unstack(0, fill_value=0).astype(dtype)

    # Sort from the cell types with the highest abundance
    # NOTE: a double sort by this and secondarily by organ name might be
    # even better perhaps
    data = data.loc[(data != 0).sum(axis=1).sort_values(ascending=False).index]

    return data


def get_organxorganism(
    celltype,
    measurement_type="gene_expression",
):
    """Get a presence/absence matrix of a cell type across organs and organisms."""
    organisms = get_organisms(
        measurement_type=measurement_type,
    )

    res = {}
    for organism in organisms:
        data = get_celltypexorgan(
            organism,
            measurement_type=measurement_type,
        )
        if celltype not in data.index:
            continue
        organs = data.columns[data.loc[celltype] > 0].tolist()
        for organ in organs:
            res[(organism, organ)] = 1
    res = pd.Series(res).unstack(0, fill_value=0)

    # Exclude organism if it does not have that cell type
    res = res.loc[:, res.any(axis=0)]

    return res


def get_celltypexorganism(
    measurement_type="gene_expression",
):
    """Get a presence/absence matrix of a cell type across organs and organisms."""
    organisms = get_organisms(
        measurement_type=measurement_type,
    )

    res = {}
    for organism in organisms:
        data = get_celltypexorgan(
            organism,
            measurement_type=measurement_type,
        )
        celltypes = data.loc[(data > 0).any(axis=1)].index.tolist()
        for celltype in celltypes:
            res[(organism, celltype)] = 1
    res = pd.Series(res).unstack(0, fill_value=0)

    return res
