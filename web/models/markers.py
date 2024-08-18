import numpy as np
import pandas as pd

from models.paths import get_atlas_path
from models.utils import ApproximationFile
from models.exceptions import (
    OrganismNotFoundError,
    OrganNotFoundError,
    OneOrganError,
    MeasurementTypeNotFoundError,
    TooManyFeaturesError,
    FeatureNotFoundError,
    SomeFeaturesNotFoundError,
    FeatureSequencesNotFoundError,
    CellTypeNotFoundError,
    SimilarityMethodError,
    NeighborhoodNotFoundError,
)
from models.celltypes import (
    get_celltype_index,
)
from models.quantisation import (
    get_quantisation,
)
from models.features import (
    get_features,
    get_feature_index,
    get_feature_names,
)
from models.surface import (
    get_surface_genes,
)



def get_markers_vs_other_celltypes(
    organism,
    organ,
    cell_type,
    number,
    measurement_type="gene_expression",
    surface_only=False,
):
    """Get marker features for a specific cell type in an organ."""
    # In theory, one could use various methods to find markers
    if measurement_type == "gene_expression":
        method = "fraction"
    # For ATAC-Seq, average and fraction are the same thing
    else:
        method = "average"

    features = get_feature_names(organism, measurement_type)
    if surface_only:
        surface_genes = get_surface_genes(organism)
        surface_ser_sorted = pd.Series(features)
        surface_ser_sorted = surface_ser_sorted[surface_ser_sorted.isin(surface_genes)]

    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db['measurements']:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )

        gby = db['measurements'][measurement_type]['grouped_by']['tissue->celltype']
        if organ not in gby['values']['tissue'].asstr()[:]:
            raise OrganNotFoundError(
                f"Organ not found: {organ}",
                organ=organ,
            )

        data = db['measurements'][measurement_type]['data']['tissue->celltype'][organ]

        # Cell types and indices
        cell_types = data["obs_names"].asstr()[:]

        # If all markers for the tissue are requested, merge a recursive call and bail
        # TODO: do this explicitely, it's probably faster by a decent bit
        if cell_type == 'all':
            markers = []
            targets = []
            for ct in cell_types:
                markers_ct = list(get_markers_vs_other_celltypes(
                    organism,
                    organ,
                    ct,
                    number,
                    measurement_type=measurement_type,
                ))
                markers.extend(markers_ct)
                targets.extend([ct] * len(markers_ct))
            return markers, targets

        if cell_type not in cell_types:
            raise CellTypeNotFoundError(
                f"Cell type not found: {cell_type}",
                cell_type=cell_type,
            )

        # Matrix of measurements (rows are cell types)
        mat = data[method]
        if surface_only:
            mat = mat[:, surface_ser_sorted.index.values]

        # Index cell types
        ncell_types = len(cell_types)
        celltype_index_dict = get_celltype_index(cell_type, cell_types)
        cell_type = celltype_index_dict["celltype"]
        idx = celltype_index_dict["index"]
        idx_other = [i for i in range(ncell_types) if i != idx]

        vector = mat[idx]
        mat_other = mat[idx_other]

        # If the data is quantised, undo the quantisation to get real values
        dequantise = "quantisation" in db['measurements'][measurement_type]
        if dequantise:
            quantisation = get_quantisation(organism, measurement_type)
            vector = quantisation[vector]
            mat_other = quantisation[mat_other]

    # Compute difference (vector - other)
    mat_other -= vector
    mat_other *= -1

    # Find closest cell type for each feature
    closest_value = mat_other.min(axis=0)

    # Take top features
    idx_markers = np.argsort(closest_value)[-number:][::-1]

    # Sometimes there are just not enough markers, so make sure the difference
    # is positive
    idx_markers = idx_markers[closest_value[idx_markers] > 0]

    # Get the feature names
    if surface_only:
        markers = surface_ser_sorted.values[idx_markers]
    else:
        markers = features[idx_markers]

    return markers


def get_markers_vs_other_tissues(
    organism,
    organ,
    cell_type,
    number,
    measurement_type="gene_expression",
    surface_only=False,
):
    """Get marker features for a specific cell type in an organ."""
    # In theory, one could use various methods to find markers
    if measurement_type == "gene_expression":
        method = "fraction"
    # For ATAC-Seq, average and fraction are the same thing
    else:
        method = "average"

    features = get_feature_names(organism, measurement_type)
    if surface_only:
        surface_genes = get_surface_genes(organism)
        surface_ser_sorted = pd.Series(features)
        surface_ser_sorted = surface_ser_sorted[surface_ser_sorted.isin(surface_genes)]

    approx_path = get_atlas_path(organism)
    with ApproximationFile(approx_path) as db:
        if measurement_type not in db['measurements']:
            raise MeasurementTypeNotFoundError(
                f"Measurement type not found: {measurement_type}",
                measurement_type=measurement_type,
            )

        gby = db['measurements'][measurement_type]['grouped_by']['tissue->celltype']
        organs = gby['values']['tissue'].asstr()[:]
        if len(organs) == 1:
            raise OneOrganError("Only one organ found")
        if organ == 'all':
            markers = []
            targets = []
            for tissue in organs:
                try:
                    markers_organ = list(get_markers_vs_other_tissues(
                        organism,
                        tissue,
                        cell_type,
                        number,
                        measurement_type=measurement_type,
                    ))
                except CellTypeNotFoundError:
                    continue
                markers.extend(markers_organ)
                targets.extend([tissue] * len(markers_organ))
            return markers, targets
        if organ not in organs:
            raise OrganNotFoundError(
                f"Organ not found: {organ}",
                organ=organ,
            )

        mat = []
        organs_mat = []
        for tissue in organs:
            data_tissue = db['measurements'][measurement_type]['data']['tissue->celltype'][tissue]
            # Cell types and indices
            cell_types = list(data_tissue["obs_names"].asstr()[:])

            if cell_type not in cell_types:
                if tissue == organ:
                    raise CellTypeNotFoundError(
                        f"Cell type not found in {organ}: {cell_type}",
                        cell_type=cell_type,
                    )
                continue

            vect_tissue = data_tissue[method][cell_types.index(cell_type)]
            if surface_only:
                vect_tissue = vect_tissue[surface_ser_sorted.index.values]
            mat.append(vect_tissue)
            organs_mat.append(tissue)

        # Matrix of measurements (rows are tissues)
        mat = np.vstack(mat)

        # Index organs
        norgans = len(organs_mat)
        if norgans == 1:
            raise OneOrganError(f"Only one organ with {cell_type} found")
        idx = list(organs_mat).index(organ)
        idx_other = [i for i in range(norgans) if i != idx]
        vector = mat[idx]
        mat_other = mat[idx_other]

        # If the data is quantised, undo the quantisation to get real values
        dequantise = "quantisation" in db['measurements'][measurement_type]
        if dequantise:
            quantisation = get_quantisation(organism, measurement_type)
            vector = quantisation[vector]
            mat_other = quantisation[mat_other]

    # Compute difference (vector - other)
    mat_other -= vector
    mat_other *= -1

    # Find closest cell type for each feature
    closest_value = mat_other.min(axis=0)

    # Take top features
    idx_markers = np.argsort(closest_value)[-number:][::-1]

    # Sometimes there are just not enough markers, so make sure the difference
    # is positive
    idx_markers = idx_markers[closest_value[idx_markers] > 0]

    # Get the feature names
    if surface_only:
        markers = surface_ser_sorted.values[idx_markers]
    else:
        markers = features[idx_markers]

    return markers


