"""Module for utility functions"""
import re


def clean_feature_string(features, organism=None, measurement_type="gene_expression"):
    """Clean feature string and split into a list."""
    features = features.replace('"', "").replace("'", "").replace(" ", "")

    # Split a single string into a list of features
    features = features.split(",")

    # Correct capitalization of gene names based on species
    if measurement_type == "gene_expression":
        if organism == "m_musculus":
            features = [fea.capitalize() for fea in features]
        elif organism == "h_sapiens":
            features = [fea.upper() for fea in features]
    # Peak coordinates are always lowercase
    elif measurement_type == "chromatin_accessibility":
        features = [fea.lower() for fea in features]

    return features


def clean_organ_string(organ):
    """Clean organ string."""
    organ = organ.lower()

    # NLP has issues with spaces, so accept underscores as well
    # FIXME: first fix all approximations to use proper organs with no underscores
    #organ = organ.replace("_", " ")

    if organ == 'whole':
        return organ

    # FIXME: better would be to use all lowercase
    organ = organ.capitalize()

    return organ


def clean_celltype_string(cell_type):
    """Clean cell type string."""
    # B, T, NK cells are called without the "cells"
    match = re.match('([A-Z]{1,3}) cell(s?)', cell_type, flags=re.IGNORECASE)
    if match is not None:
        cell_type = match.group(1).upper()

    # NLP has issues with spaces, so accept underscores as well
    cell_type = cell_type.replace("_", " ")
    return cell_type

