"""Module for utility functions"""

import re


def clean_feature_string(features, organism=None, measurement_type="gene_expression"):
    """Clean feature string and split into a list."""
    if features is None:
        return []

    features = features.replace('"', "").replace("'", "").replace(" ", "")

    # Split a single string into a list of features
    features = features.split(",")

    # Convert everything to lowercase, the models include a back-conversion
    features = [fea.lower() for fea in features if fea]

    return features


def clean_organ_string(organ):
    """Clean organ string."""
    organ = organ.lower()

    # NLP has issues with spaces, so accept underscores as well
    # FIXME: first fix all approximations to use proper organs with no underscores
    # organ = organ.replace("_", " ")

    return organ


def clean_celltype_string(cell_type):
    """Clean cell type string."""
    cell_type = cell_type.strip(" ")

    if cell_type.startswith("plasma  cell"):
        return "plasma"

    # B, T, NK cells are called without the "cells"
    match = re.match("([A-Z]{1,3}) cell(s?)", cell_type, flags=re.IGNORECASE)
    if match is not None:
        cell_type = match.group(1).upper()

    # NLP has issues with spaces, so accept underscores as well
    cell_type = cell_type.replace("_", " ")
    return cell_type


def clean_celltypes_string(celltypes_string):
    """Clean cell types string into multiple cell types."""
    if celltypes_string is None:
        return []
    cell_types = celltypes_string.replace('"', "").replace("'", "")
    # Split a single string into a list of cell types
    cell_types = cell_types.split(",")

    cell_types = [
        clean_celltype_string(cell_type) for cell_type in cell_types if cell_type
    ]

    return cell_types
