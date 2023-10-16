"""Module for utility functions"""
import re
from flask import request
from flask_restful import abort


def clean_feature_string(features, organism=None, measurement_type="gene_expression"):
    """Clean feature string and split into a list."""
    features = features.replace('"', "").replace("'", "").replace(" ", "")

    # Split a single string into a list of features
    features = features.split(",")

    # Convert everything to lowercase, the models include a back-conversion
    features = [fea.lower() for fea in features]

    return features


def clean_organ_string(organ):
    """Clean organ string."""
    organ = organ.lower()

    # NLP has issues with spaces, so accept underscores as well
    # FIXME: first fix all approximations to use proper organs with no underscores
    #organ = organ.replace("_", " ")

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


def required_parameters(*required_args):
    """Decorator that aborts if mandatory parameters are missing."""
    def inner(wrapped):
        def func(*args_inner, **kwargs_inner):
            for arg in required_args:
                if request.args.get(arg, None) is None:
                    abort(
                        400,
                        message=f"The \"{arg}\" parameter is required.",
                    )
            return wrapped(*args_inner, **kwargs_inner)
        return func
    return inner
